from ipcg.binder.AGenerator import AGenerator

class JavaGenerator(AGenerator):
    def __init__(self):
        AGenerator.__init__(self)
        
        self._structParcelable = self._getTemplate('java/StructParcelable.py')
        
        self._enumParcelable = self._getTemplate('java/EnumParcelable.py')
        
        self._interfaceAIDL = self._getTemplate('java/InterfaceAIDL.py')
        
        self._parcelableAIDL = self._getTemplate('java/ParcelableAIDL.py')
        
        self._makefile = self._getTemplate('java/Makefile.py')
        
    def generateMakefile(self, localModule, sourceFiles):
        return self._makefile.render(localModule=localModule, sourceFiles=sourceFiles)
    
    def generateStructParcelable(self, idlType):
        return self._structParcelable.render(struct=idlType)
    
    def generateEnumParcelable(self, idlType):
        return self._enumParcelable.render(enum=idlType)
    
    def generateInterfaceAIDL(self, idlType):
        return self._interfaceAIDL.render(iface=idlType)
    
    def generateParcelableAIDL(self, idlType):
        return self._parcelableAIDL.render(type=idlType)
