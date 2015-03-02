from idl.Type import Type

from ipcg.binder.AGenerator import AGenerator


class NativeGenerator(AGenerator):
    '''
    Class used to generate native binder IPC code.
    '''
    
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
        
    def generateMakefile(self, sourceFiles, localModule, isStatic=True):
        '''
        Generates a makefile for native IPC static library.
        
        @param sourceFiles: List of source files built by the makefile.
        @param localModule: Name of the static library
        @param isStatic: if set to True library will be compiled as static.
        
        @return: Source code string.
        '''
        
        return self._makefile.render(sourceFiles=sourceFiles, localModule=localModule, isStatic=isStatic)
        
    def generateInterfaceBpSource(self, itype):
        '''
        Generates an interface proxy class.
        
        @param itype: IDL object of type idl.Type.INTERFACE
        
        @return: Source code string. 
        '''
        
        if itype != Type.INTERFACE:
            raise RuntimeError('Invalid argument %r' % str(itype))
        
        return self._interfaceBpSource.render(iface=itype, namespace=self._namespace)
    
    def generateInterfaceBnSource(self, itype):
        '''
        Generates an interface native class source.
        
        @param itype: IDL object of type idl.type.INTERFACE
        
        @return: Source code string.
        '''
        
        if itype != Type.INTERFACE:
            raise RuntimeError('Invalid argument %r' % str(itype))
        
        return self._interfaceBnSource.render(iface=itype, namespace=self._namespace)
    
    def generateInterfaceBnHeader(self, itype):
        '''
        Generates an interface native class header code.
        
        @param itype: IDL object of type idl.type.INTERFACE 
        
        @return: Source code string.
        '''
        
        if itype != Type.INTERFACE:
            raise RuntimeError('Invalid argument %r' % str(itype))
        
        return self._interfaceBnHeader.render(iface=itype, namespace=self._namespace)
    
    def generateInterfaceHeader(self, itype):
        '''
        Generates native interface declaration header.
        
        @param itype:  IDL object of type idl.type.INTERFACE
        
        @return: Source code string.
        '''
        
        if itype != Type.INTERFACE:
            raise RuntimeError('Invalid argument %r' % str(itype))
        
        return self._interfaceHeader.render(iface=itype, namespace=self._namespace)
    
    def generateStructParcelableHeader(self, itype):
        '''
        Generates a structure class header code.
        
        @param itype: IDL object of type idl.type.STRUCTURE
        
        @return: Source code string.
        '''
        
        if itype != Type.STRUCTURE:
            raise RuntimeError('Invalid argument %r' % str(itype))
        
        return self._structParcelableHeader.render(struct=itype, namespace=self._namespace)

    def generateStructParcelableSource(self, itype):
        '''
        Generates a parcelable structure class source code.
        
        @param itype: IDL object of type idl.type.STRUCTURE
        
        @return: Source code string.
        '''
        
        if itype != Type.STRUCTURE:
            raise RuntimeError('Invalid argument %r' % str(itype))
        
        return self._structParcelableSource.render(struct=itype, namespace=self._namespace)
    
    def generateEnumHeader(self, itype):
        '''
        Generates an enum header declaration code.
        
        @param itype: IDL object of type idl.type.ENUM
        
        @requires: Source code string.
        '''

        if itype != Type.ENUM:
            raise RuntimeError('Invalid argument %r' % str(itype))
        
        return self._enumHeader.render(enum=itype, namespace=self._namespace)
