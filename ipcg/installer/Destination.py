import os

from ipcg.installer.FileUtils import FileUtils
from ipcg.installer.Intermediate import Intermediate


class Destination:
    def __init__(self, parent, name, path):
        self._path = path
        self._name = name
        self._parent = parent
        
    @property
    def intermediatesDir(self):
        return os.path.join(self._parent.buildDir, self._name + '_intermediates')
    
    @property
    def installedDir(self):
        return os.path.join(self._parent.buildDir, self._name + '_installed')

    @property
    def name(self):
        return self._name
    
    @property
    def path(self):
        return self._path
    
    def install(self, source, path):
        return self._parent._installSource(self, source, path)
        
    @property
    def intermediates(self):
        res = []
        for root, dirs, files in os.walk(self.intermediatesDir):
            for i in files:
                relativePath = FileUtils.getRelPath(self.intermediatesDir, os.path.join(root, i))
                
                fullSourcePath = os.path.join(root, i)
                
                fullDestinationPath = os.path.join(self._path, relativePath)
                
                res.append( Intermediate(
                                fullSourcePath,
                                fullDestinationPath
                ))
                
        return res
