import filecmp
import os
import shutil


class FileUtils:
    @staticmethod
    def getRelPath(base, path):
        base = FileUtils.normalizePath(base)
        path = FileUtils.normalizePath(path)
        
        if not path.startswith(base):
            raise RuntimeError('%r not a base of %r' % (base, path))
        
        res = path[len(base):]
        
        if res.startswith('/'):
            res = res[1:]
            
        return res
    
    @staticmethod
    def normalizePath(path):
        return os.path.abspath(path).replace(os.sep, '/')
    
    @staticmethod
    def copy(source, destination):
        shutil.copy(source, destination)
        
    @staticmethod
    def installFile(source, destination):
        if os.path.exists(destination) and FileUtils.compare(source, destination):
            # No need to install (files already same)
            return False
            
        FileUtils.makeTree(os.path.dirname(destination))
        
        FileUtils.copy(source, destination)

        return True
    
    @staticmethod
    def delete(path):
        os.remove(path)
    
    @staticmethod
    def compare(file1, file2):
        return filecmp.cmp(file1, file2)

    @staticmethod
    def installSource(source, path):
        fullPath = os.path.abspath(path)
        
        dirPath = os.path.dirname(fullPath)
        
        FileUtils.makeTree(dirPath)
        
        with open(fullPath, 'wb') as fileObj:
            # TODO Fix this
            try:
                fileObj.write(bytes(source, 'UTF-8'))
            except TypeError:                
                fileObj.write(source)
            
        return True
            
    @staticmethod
    def makeTree(path):
        if not os.path.exists(path):
            os.makedirs(path)
