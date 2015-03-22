from idl.Type import Type

from ipcg.binder.AGenerator import AGenerator


class JavaGenerator(AGenerator):
    '''
    Class used to generate Java binder IPC code.
    '''
    
    TEMPLATES_DIR = 'java/templates'
    
    def __init__(self):
        AGenerator.__init__(self, JavaGenerator.TEMPLATES_DIR)

        # Template used to generate structure java parcelable files        
        self._structParcelable = self._getTemplate('StructParcelable.py')
        
        # Template used to generate enumeration java parcelable files
        self._enumParcelable = self._getTemplate('EnumParcelable.py')
        
        # Template used to generate AIDL interface files
        self._interfaceAIDL = self._getTemplate('InterfaceAIDL.py')
        
        # Template used to generate AIDL parcelable files
        self._parcelableAIDL = self._getTemplate('ParcelableAIDL.py')
        
        # Template used to generate project Android.mk file
        self._makefile = self._getTemplate('Makefile.py')
        
    def generateMakefile(self, localModule, sourceFiles, isStatic=True):
        '''
        Generates a make file for the Java IPC library project.
        
        @param localModule: Name of the static Java library
        @param sourceFiles: List of source files built by the make file.
        @param isStatic: if set to True library will be compiled as static.
        
        @return: Source code string.
        '''
        
        return self._makefile.render(localModule=localModule, sourceFiles=sourceFiles, isStatic=isStatic)
    
    def generateStructParcelable(self, itype):
        '''
        Generates a parcelable structure class.
        
        @param itype:  IDL object of type idl.Type.STRUCTURE
        
        @return: Source code string.
        '''
        
        if itype != Type.STRUCTURE:
            raise RuntimeError('Invalid argument %r' % str(itype))
        
        return self._structParcelable.render(struct=itype)
    
    def generateEnumParcelable(self, itype):
        '''
        Generates a parcelable enum class.
        
        @param itype:  IDL object of type idl.Type.ENUM
        
        @return: Source code string.
        '''
        
        if itype != Type.ENUM:
            raise RuntimeError('Invalid argument %r' % str(itype))
        
        return self._enumParcelable.render(enum=itype)
    
    def generateInterfaceAIDL(self, itype):
        '''
        Generates an interface AIDL declaration.
        
        @param itype: IDL object of type idl.Type.INTERFACE
        
        @return: Source code string.
        '''
        
        if itype != Type.INTERFACE:
            raise RuntimeError('Invalid argument %r' % str(itype))
        
        return self._interfaceAIDL.render(iface=itype)
    
    def generateParcelableAIDL(self, itype):
        '''
        Generates a parcelable AIDL declaration.
        
        @param itype:  IDL object of type idl.Type.STRUCTURE or idl.Type.ENUM 
        
        @return: Source code string.
        '''
        
        if itype not in [Type.STRUCTURE, Type.ENUM]:
            raise RuntimeError('Invalid argument %r' % str(itype))
        
        return self._parcelableAIDL.render(type=itype)
