from ipcg.binder.AGenerator import AGenerator


class NativeGenerator(AGenerator):
    def __init__(self, namespace):
        AGenerator.__init__(self)
        
        self._namespace = namespace
        
        self._structParcelableHeader = self._getTemplate('native/StructParcelableHeader.py')
        
        self._structParcelableSource = self._getTemplate('native/StructParcelableSource.py')
        
        self._enumHeader  = self._getTemplate('native/EnumHeader.py')
        
        self._interfaceBnHeader = self._getTemplate('native/InterfaceBnHeader.py')
        
        self._interfaceBnSource = self._getTemplate('native/InterfaceBnSource.py')
        
        self._interfaceBpSource = self._getTemplate('native/InterfaceBpSource.py')
        
        self._interfaceHeader = self._getTemplate('native/InterfaceHeader.py')
        
        self._makefile = self._getTemplate('native/Makefile.py')
        
    def generateMakefile(self, sourceFiles, localModule):
        return self._makefile.render(sourceFiles=sourceFiles, localModule=localModule)
        
    def generateInterfaceBpSource(self, idlType):
        return self._interfaceBpSource.render(iface=idlType, namespace=self._namespace)
    
    def generateInterfaceBnSource(self, idlType):
        return self._interfaceBnSource.render(iface=idlType, namespace=self._namespace)
    
    def generateInterfaceBnHeader(self, idlType):
        return self._interfaceBnHeader.render(iface=idlType, namespace=self._namespace)
    
    def generateStructParcelableSource(self, idlType):
        return self._structParcelableSource.render(struct=idlType, namespace=self._namespace)
    
    def generateEnumHeader(self, idlType):
        return self._enumHeader.render(enum=idlType, namespace=self._namespace)
    
    def generateInterfaceHeader(self, idlType):
        return self._interfaceHeader.render(iface=idlType, namespace=self._namespace)
    
    def generateStructParcelableHeader(self, idlType):
        return self._structParcelableHeader.render(struct=idlType, namespace=self._namespace)
