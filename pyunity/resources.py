## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from . import Logger
from pathlib import Path
from datetime import datetime
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
    if egg:
        with zipfile.ZipFile(package) as zf:
            src = str(Path("pyunity") / local)
            if src not in zf.namelist():
                raise Exception(f"No resource at {package / src}")
            if dest.exists():
                ziptime = datetime(*zf.getinfo(src).date_time)
                if ziptime.timestamp() != dest.stat().st_mtime:
                    return dest
            out = zf.extract(src, directory)
            shutil.move(out, dest)
            shutil.rmtree(Path(out).parent)
            Logger.LogLine(Logger.INFO, f"Loaded resource {src} to {dest}")
            return dest
    else:
        src = package / local
        if not src.exists():
            raise Exception(f"No resource at {src}")
        if src.is_file():
            if dest.exists() and src.stat().st_mtime < dest.stat().st_mtime:
                return dest
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dest)
        else:
            for file in src.glob("**/*"):
                if file.is_dir():
                    continue
                rel = file.relative_to(src)
                filedest = dest / rel
                if filedest.exists():
                    if src.stat().st_mtime < filedest.stat().st_mtime:
                        continue
                filedest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(file, filedest)
        Logger.LogLine(Logger.INFO, f"Loaded resource {src} to {dest}")
        return dest
