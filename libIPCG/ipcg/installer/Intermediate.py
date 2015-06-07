from ipcg.utils.FileUtils import FileUtils


class Intermediate:
    def __init__(self, source, dest):
        self._source = FileUtils.normalizePath(source)
        self._dest = FileUtils.normalizePath(dest)

    @property
    def source(self):
        return self._source

    @property
    def dest(self):
        return self._dest

    def install(self):
        return FileUtils.installFile(self._source, self._dest)
