from . import Logger
from pathlib import Path
import shutil
import zipfile

directory = Path.home() / ".pyunity"
if not directory.is_dir():
    directory.mkdir()

package = Path(__file__).resolve().parent
if not package.exists():
    package = package.parent
    if not package.is_file():
        raise Exception("Cannot find egg file")
    egg = True
else:
    egg = False

def getPath(local):
    dest = directory / local
    if dest.exists():
        return dest
    if egg:
        with zipfile.ZipFile(package) as zf:
            src = str(Path("pyunity") / local)
            if src not in zf.namelist():
                raise Exception(f"No resource at {package / src}")
            out = zf.extract(src, directory)
            shutil.move(out, dest)
            shutil.rmtree(Path(out).parent)
            Logger.LogLine(Logger.INFO, f"Loaded resource {src} to {dest}")
            return dest
    else:
        src = package / local
        if not src.exists():
            raise Exception(f"No resource at {src}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.is_file():
            shutil.copy(src, dest)
            Logger.LogLine(Logger.INFO, f"Loaded resource {src} to {dest}")
        else:
            shutil.copytree(src, dest)
        return dest
