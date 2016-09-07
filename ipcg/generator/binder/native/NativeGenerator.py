import os

from idl.Type import Type

from ipcg.AGenerator import AGenerator


class NativeGenerator(AGenerator):
    '''
    Class used to generate native binder IPC code.
    '''

    TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

    def __init__(self, namespace, libraryInclude, libraryName):
        AGenerator.__init__(self, NativeGenerator.TEMPLATES_DIR)

        self._namespace = namespace

        self._libraryInclude = libraryInclude

        self._libraryName = libraryName

        # Template used to generate structure class parcelable header files
        self._structParcelableHeader = self._getTemplate('StructParcelableHeader.py')

        # Template used to generate structure class parcelable source files
        self._structParcelableSource = self._getTemplate('StructParcelableSource.py')

        # Template used to generate enumeration header files
        self._enumHeader = self._getTemplate('EnumHeader.py')

        # Template used to generate interface native header files
        self._interfaceBnHeader = self._getTemplate('InterfaceBnHeader.py')

        # Template used to generate interface native source files
        self._interfaceBnSource = self._getTemplate('InterfaceBnSource.py')

        # Template used to generate interface proxy soruce files
        self._interfaceBpSource = self._getTemplate('InterfaceBpSource.py')

        # Template used to generate interface header files
        self._interfaceHeader = self._getTemplate('InterfaceHeader.py')

        # Template used to generate project Android.mk file
        self._makefile = self._getTemplate('Makefile.py')

    def generateMakefile(self, sourceFiles, localModule, isStatic=True):
        '''
        Generates a makefile for native IPC static library.

        @param sourceFiles: List of source files built by the makefile.
        @param localModule: Name of the static library
        @param isStatic: if set to True library will be compiled as static.

        @return: Source code string.
        '''

        return self._makefile.render(sourceFiles=sourceFiles, localModule=localModule, isStatic=isStatic, libraryInclude=self._libraryInclude, libraryName=self._libraryName)

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
