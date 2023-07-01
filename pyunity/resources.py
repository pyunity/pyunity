## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from . import Logger
from .values import ABCMeta, abstractmethod
from pathlib import Path
from datetime import datetime
import shutil
import zipfile

class AssetResolver(metaclass=ABCMeta):
    def __init__(self, cache):
        self.cache = Path(cache)

    @abstractmethod
    def getSrcMtime(self, local):
        pass

    def checkCacheExists(self, local):
        dest = self.cache / local
        return dest.exists()

    def checkCache(self, local):
        if not self.checkCacheExists(local):
            return False
        dest = self.cache / local
        cacheMtime = dest.stat().st_mtime
        if cacheMtime < self.getSrcMtime(local):
            return True
        return False

    @abstractmethod
    def checkSrcExists(self, local):
        pass

    @abstractmethod
    def copyAsset(self, local):
        pass

    def preFetch(self):
        pass

    def postFetch(self):
        pass

    def getPath(self, local):
        self.preFetch()
        dest = self.cache / local
        if self.checkCache(local):
            return dest

        resolver = type(self).__name__
        if not self.checkSrcExists(local):
            raise Exception(f"No resource found at {local} with {resolver}")
        self.copyAsset(local)
        Logger.LogLine(Logger.INFO,
                       f"Loaded resource found at {local} with {resolver}")
        self.postFetch()
        return dest

class ZipAssetResolver(AssetResolver):
    def __init__(self, cache, src, prefix):
        super(ZipAssetResolver, self).__init__(cache)
        self.src = Path(src)
        self.prefix = Path(prefix)
        self.zipfile = None

    def preFetch(self):
        self.zipfile = zipfile.ZipFile(self.src)

    def postFetch(self):
        self.zipfile.close()
        self.zipfile = None

    def getSrcMtime(self, local):
        path = self.prefix / local
        ziptime = datetime(*self.zipfile.getinfo(path).date_time)
        return ziptime.timestamp()

    def checkSrcExists(self, local):
        path = self.prefix / local
        return path in self.zipfile.namelist()

    def copyAsset(self, local):
        path = self.prefix / local
        dest = self.cache / local
        out = self.zipfile.extract(path, self.cache)
        shutil.move(out, dest)
        shutil.rmtree(Path(out).parent)

class PackageAssetResolver(AssetResolver):
    def __init__(self, cache, package):
        super(PackageAssetResolver, self).__init__(cache)
        self.package = package
        self.files = []

    def postFetch(self):
        self.files = []

    def getSrcMtime(self, local):
        file = self.package / local
        return file.stat().st_mtime

    def checkSrcExists(self, local):
        file = self.package / local
        return file.exists()

    def checkCache(self, local):
        src = self.package / local
        if src.is_file():
            return super(PackageAssetResolver, self).checkCache(local)

        self.files = src.glob("**/*")
        for file in self.files:
            rel = file.relative_to(self.package)
            if not super(PackageAssetResolver, self).checkCache(rel):
                return False
        return True

    def copyAsset(self, local):
        src = self.package / local
        if src.is_file():
            dest = self.cache / local
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dest)
        else:
            for file in self.files:
                if file.is_file():
                    rel = file.relative_to(self.package)
                    dest = self.cache / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(file, dest)

directory = Path.home() / ".pyunity"
if not directory.is_dir():
    directory.mkdir()

package = Path(__file__).resolve().parent
if package.parent.name.endswith(".zip"):
    package = package.parent
    if not package.is_file():
        raise Exception("Cannot find egg file")
    resolver = ZipAssetResolver(directory, package, "pyunity")
else:
    resolver = PackageAssetResolver(directory, package)
