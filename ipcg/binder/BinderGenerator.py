from idl.Environment import Environment
from idl.Type import Type

from ipcg.binder.JavaGenerator import JavaGenerator
from ipcg.binder.NativeGenerator import NativeGenerator
import os


class BinderGenerator:
    def __init__(self, nativeProjDir, nativeLibraryName, javaProjDir, javaLibraryName):
        self._java = JavaGenerator()
        
        self._nativeLibraryName = nativeLibraryName
        
        self._javaLibraryName = javaLibraryName 
        
        self._native = NativeGenerator(namespace='proxy')
        
        self._env = Environment()
        
        self._nativeProjDir = os.path.abspath(nativeProjDir)
        
        self._javaProjDir = os.path.abspath(javaProjDir)
    
        self._nativeSourceFiles = []
        
        self._javaSourceFiles = []
    
    @property
    def env(self):
        return self._env
    
    def generate(self):
        for idlType in self._env.types:
            if idlType.id in [Type.ENUM, Type.STRUCTURE]:
                # Java AIDL                    
                self._installJavaSource(
                    '/'.join(idlType.path) + '.aidl',
                    self._java.generateParcelableAIDL(idlType)
                )
                
                # Java parcelable function
                javaParcelableFnc = {
                    Type.ENUM : self._java.generateEnumParcelable,
                    Type.STRUCTURE : self._java.generateStructParcelable 
                }[idlType.id]
                
                # Java parcelable
                self._installJavaSource(
                    '/'.join(idlType.path) + '.java',
                    javaParcelableFnc(idlType),
                    make=True
                )
                
                # Native header function
                nativeHeaderFnc = {
                    Type.ENUM : self._native.generateEnumHeader,
                    Type.STRUCTURE : self._native.generateStructParcelableHeader 
                }[idlType.id]
                
                # Native header
                self._installNativeHeader(
                    '/'.join(idlType.path),
                    nativeHeaderFnc(idlType)
                )
                
                if idlType == Type.STRUCTURE:
                    # Native source
                    self._installNativeSource(
                        '/'.join(idlType.path),
                        self._native.generateStructParcelableSource(idlType)
                    )

            elif idlType == Type.INTERFACE:
                # AIDL
                self._installJavaSource(
                    '/'.join(idlType.path) + '.aidl',
                    self._java.generateInterfaceAIDL(idlType),
                    make=True
                )
                
                # Native header
                path = idlType.path
                
                path[-1] = 'I' + path[-1]
                
                self._installNativeHeader(
                    '/'.join(path),
                    self._native.generateInterfaceHeader(idlType)
                )
                
                # Native Bn header
                path = idlType.path
                
                path[-1] = 'Bn' + path[-1]
                
                self._installNativeHeader(
                    '/'.join(path),
                    self._native.generateInterfaceBnHeader(idlType)
                )
                
                # Native Bn source
                path = idlType.path
                
                path[-1] = 'Bn' + path[-1]
                
                self._installNativeSource(
                  '/'.join(path),
                    self._native.generateInterfaceBnSource(idlType)
                )
                
                # Native Bp source
                path = idlType.path
                
                path[-1] = 'Bp' + path[-1]
                
                self._installNativeSource(
                    '/'.join(path),
                    self._native.generateInterfaceBpSource(idlType)
                )      
            
            else:
                raise RuntimeError('Not implemented')
            
        # Java makefile
        self._installJava(
            'Android.mk',
            self._java.generateMakefile(self._javaLibraryName, self._javaSourceFiles)
        )
        
        # Native makefile
        self._installNative(
            'Android.mk',
            self._native.generateMakefile(self._nativeSourceFiles, self._nativeLibraryName)
        )
                
    def _installNativeSource(self, path, source):
        # Append extension & source directory
        path = os.path.join('source', path + '.cpp')
        
        # Replace possible windows path delimiters with unix ones
        path = path.replace('\\', '/')
        
        self._nativeSourceFiles.append(path)
        
        self._installNative(path, source)
            
    def _installNativeHeader(self, path, source):
        path += '.h'
        
        self._installNative(os.path.join('include', path), source)
    
    def _installNative(self, path, source):
        print('[native] install %r' % path)
        fullPath = os.path.join(self._nativeProjDir, path)
        
        dirPath = os.path.dirname(fullPath )
        
        if dirPath and not os.path.exists(dirPath):
            os.makedirs(dirPath)
            
        open(fullPath , 'wb').write(bytes(source, 'UTF-8'))
    
    
    def _installJavaSource(self, path, source, make=False):
        path = os.path.join('src', path)
        
        # Replace possible windows path delimiters with unix ones
        path = path.replace('\\', '/') 
        
        self._installJava(path, source)
        
        if make:
            self._javaSourceFiles.append(path)
        
    def _installJava(self, path, source):
        print('[java] install %r' % path)
        
        fullPath = os.path.join(self._javaProjDir, path)
        
        dirPath = os.path.dirname(fullPath )
        
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
            
        open(fullPath, 'wb').write(bytes(source, 'UTF-8'))
