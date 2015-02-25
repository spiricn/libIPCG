import pickle
import os
import shutil

from ipcg.installer.Destination import Destination
from ipcg.installer.FileUtils import FileUtils


class Installer:
    class Statistics:
        def __init__(self, installed, upToDate):
            self.numFilesInstalled = installed
            self.numFilesUpToDate = upToDate
            
    STATE_IDLE, \
    STATE_TRANSACTION, \
     = range(2)
     
    BUILD_LIST_FILE_NAME = 'build_list'
    
    def __init__(self, buildDir='.build'):
        self._destinations = {}
        
        self._buildDir = os.path.abspath(buildDir)
        
        self._state = Installer.STATE_IDLE
        
        self._buildList = {}
        
    def addDestination(self, name, path):
        if self._state != Installer.STATE_IDLE:
            raise RuntimeError('May not add destinations while transaction is in progress')
            
        if not name in self._destinations:
            self._destinations[name] = Destination(self, name, path)
            
            return self._destinations[name]
        
        else:
            raise RuntimeError('Destination %r already exists' % name)

    def _installSource(self, dest, source, path):
        if self._state != Installer.STATE_TRANSACTION:
            raise RuntimeError('Transaction must be active to install a file')
        
        return FileUtils.installSource(source, os.path.join(dest.intermediatesDir, path))
        
    @property
    def buildDir(self):
        return self._buildDir
            
    def begin(self):
        if self._state != Installer.STATE_IDLE:
            raise RuntimeError('May not start transaction while another transaction is in progress')
            
        # Create / clear intermediates
        for name, dest in self._destinations.items():
            if os.path.exists(dest.intermediatesDir):
                shutil.rmtree(dest.intermediatesDir)
                
            FileUtils.makeTree(dest.intermediatesDir)
            
        self._state = Installer.STATE_TRANSACTION
        
    @property
    def _buildListPath(self):
        return os.path.join(self._buildDir, Installer.BUILD_LIST_FILE_NAME)
    
    def clean(self):
        if self._state != Installer.STATE_IDLE:
            raise RuntimeError("May not call clean() while transaction is in progress")
        
        buildList = self._readBuildList()
        
        if not buildList:
            return
        
        for i in buildList:
            print('Clean %r' % i)
            if os.path.exists(i):
                FileUtils.delete(i)
            
        FileUtils.delete(self._buildListPath)
        
    def _readBuildList(self):
        if os.path.exists(self._buildListPath):        
            with open(self._buildListPath, 'rb') as fileObj:
                return pickle.load(fileObj)
                
        return None
                
    def commit(self):
        if self._state != Installer.STATE_TRANSACTION:
            raise RuntimeError('Must call begin() before claling commit()')
        
        numInstalled = 0
        numUpToDate = 0
        
        # Load old build list
        oldBuildList = self._readBuildList()
        
        buildList = []
        
        for name, dest in self._destinations.items():
            for i in dest.intermediates:
                if i.install():
                    numInstalled += 1
                else:
                    numUpToDate += 1
                
                buildList.append(i.dest)

        # Delete all files not in new build list
        if oldBuildList:
            for i in oldBuildList:
                if i not in buildList:
                    print('Deleting generated file %r' % i)
                    FileUtils.delete(i)
                
        # Save new build list
        with open(self._buildListPath, 'wb') as fileObj:
            pickle.dump(buildList, fileObj)
            
        self._state = Installer.STATE_IDLE
        
        return Installer.Statistics(numInstalled, numUpToDate)

