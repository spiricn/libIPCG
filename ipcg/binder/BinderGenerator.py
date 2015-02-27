import os

from idl.Environment import Environment
from idl.Type import Type

from ipcg.binder.JavaGenerator import JavaGenerator
from ipcg.binder.NativeGenerator import NativeGenerator
from ipcg.installer.Installer import Installer


class BinderGenerator:
    def __init__(self, nativeProjDir, nativeLibraryName, javaProjDir, javaLibraryName):
        self._java = JavaGenerator()
        
        self._nativeLibraryName = nativeLibraryName
        
        self._javaLibraryName = javaLibraryName 
        
        self._native = NativeGenerator(namespace='proxy')
        
        self._env = Environment()
        
        self._nativeSourceFiles = []
        
        self._javaSourceFiles = []
    
        self._installer = Installer()
        
        self._nativeProj = self._installer.addDestination('native', nativeProjDir)
        
        self._javaProj = self._installer.addDestination('java', javaProjDir) 
        
    @property
    def env(self):
        return self._env
    
    def generate(self):
        self._installer.begin()
        
        for idlType in self._env.types:
            if idlType.id in [Type.ENUM, Type.STRUCTURE]:
                # Java AIDL                    
                self._installJava(
                    self._java.generateParcelableAIDL(idlType),
                    self._getFilePath(['src'] + idlType.module.package.path, idlType.name + '.aidl')
                )
                
                # Java parcelable function
                javaParcelableFnc = {
                    Type.ENUM : self._java.generateEnumParcelable,
                    Type.STRUCTURE : self._java.generateStructParcelable 
                }[idlType.id]
                
                # Java parcelable
                self._installJava(
                    javaParcelableFnc(idlType),
                    self._getFilePath(['src'] + idlType.module.package.path, idlType.name + '.java'),
                    addToMakeFile=True
                )
                
                # Native header function
                nativeHeaderFnc = {
                    Type.ENUM : self._native.generateEnumHeader,
                    Type.STRUCTURE : self._native.generateStructParcelableHeader 
                }[idlType.id]
                
                # Native header
                self._installNative(
                    nativeHeaderFnc(idlType),
                    self._getFilePath(['include'] + idlType.module.package.path, idlType.name) + '.h'
                )
                
                if idlType == Type.STRUCTURE:
                    # Native source
                    self._installNative(
                        self._native.generateStructParcelableSource(idlType),
                        self._getFilePath(['source'] + idlType.module.package.path, idlType.name) + '.cpp',
                        addToMakeFile=True
                    )

            elif idlType == Type.INTERFACE:
                # AIDL
                self._installJava(
                    self._java.generateInterfaceAIDL(idlType),
                    self._getFilePath(['src'] + idlType.module.package.path, idlType.name + '.aidl'),
                    addToMakeFile=True
                )
                
                # Native header
                self._installNative(
                    self._native.generateInterfaceHeader(idlType),
                    self._getFilePath(['include'] + idlType.module.package.path, 'I' + idlType.name) + '.h'
                )
                
                # Native Bn header
                self._installNative(
                    self._native.generateInterfaceBnHeader(idlType),
                    self._getFilePath(['include'] + idlType.module.package.path, 'Bn' + idlType.name[1:]) + '.h'
                )
                
                # Native Bn source
                self._installNative(
                    self._native.generateInterfaceBnSource(idlType),
                    self._getFilePath(['source'] + idlType.module.package.path, 'Bn' + idlType.name[1:]) + '.cpp',
                    addToMakeFile=True
                )
                
                # Native Bp source
                self._installNative(
                    self._native.generateInterfaceBpSource(idlType),
                    self._getFilePath(['source'] + idlType.module.package.path, 'Bp' + idlType.name[1:]) + '.cpp',
                    addToMakeFile=True
                )      
            
            else:
                raise RuntimeError('Not implemented')
            
        # Java makefile
        self._installJava(
            self._java.generateMakefile(self._javaLibraryName, self._javaSourceFiles),
            'Android.mk'
        )
        
        # Native makefile
        self._installNative(
            self._native.generateMakefile(self._nativeSourceFiles, self._nativeLibraryName),
            'Android.mk'
        )
        
        result = self._installer.commit()
        
        print('%d files installed ( %d up-to-date )' % (result.numFilesInstalled, result.numFilesUpToDate))
        
    def _getFilePath(self, package, name):
        return '/'.join(package) + '/' + name
        
    def _installJava(self, source, path, addToMakeFile=False):
        self._javaProj.install(source, path)
        
        if addToMakeFile:
            self._javaSourceFiles.append(path)

    def _installNative(self, source, path, addToMakeFile=False):
        self._nativeProj.install(source, path)
        
        if addToMakeFile:
            self._nativeSourceFiles.append(path)

