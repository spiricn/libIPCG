from idl.Type import Type

from ipcg import Utils


def getDefaultValue(itype):
    '''
    Gets a default value for given type (i.e. the value a variable should be initialized to).
    '''
    
    if itype.isPrimitive:
        # Primitive values
        return {
            Type.VOID : '',
            Type.BOOL : 'false',
            Type.FLOAT32 : '-1.0f',
            Type.STRING : 'android::String16("")',
            Type.INT32 : '-1',
            Type.FLOAT64 : '-1.0',
            Type.INT8 : '-1',
            Type.INT64 : '-1',
        }[itype.id]

    elif itype == Type.ENUM:
        # Enumeration
        return 'static_cast<' + getTypeClass(itype) + '>(' + str(itype.fields[0].value) + ')'
    
    elif itype == Type.STRUCTURE:
        # Structure
        return 'new ' + getTypeClass(itype) + '()'
        
    else:
        return 'NULL'

def getTypeClass(idlType):
    '''
    Gets a class name with namespace of given type (e.g. com::example::test::MyInterface)
    '''
    
    if idlType.id in [Type.INTERFACE, Type.STRUCTURE, Type.ENUM]:
        return '::'.join(idlType.path) 
    else:
        raise RuntimeError('Invalid type %s' % str(idlType))

def getTypeName(idlType):
    '''
    Maps an IDL type ID to C++ type string
    '''

    typeMap = {
        Type.VOID : 'void',
        Type.BOOL : 'bool',
        Type.FLOAT32 : 'float',
        Type.INT32 : 'int32_t',
        Type.FLOAT64 : 'double',
        Type.INT8 : 'int8_t',
        Type.INT64 : 'int64_t',
        Type.STRING : 'android::String16'
    }
    
    if idlType.id in typeMap:
        return typeMap[idlType.id]
            
    elif idlType == Type.ENUM:
        return getTypeClass(idlType)
    
    else:
        return 'android::sp<' + getTypeClass(idlType) + '>'
    
def getArgList(args):
    '''
    Get a method argument list string.
    '''
    
    res = ''
    
    for index, arg in enumerate(args):
        res += getTypeName(arg.type) + ' ' + arg.name
        
        if index  != len(args) - 1:
            res += ', '
            
    return res

def getMethodSig(method):
    '''
    Gets a method signature string (i.e. returnType + name + argList)
    '''
    
    return getTypeName(method.ret.type) + ' ' + method.name + '(' + getArgList(method.args) + ')' 

def getMethodId(method):
    '''
    Gets a method ID enumeration name (used by Bn and Bp itnerface classes)
    '''
    
    return 'METHOD_ID_' + method.name.upper()


def getReadExpr(varName, varType, parcelName):
    '''
    Creates a parcel deserialization expression with given variable name and parcel name
    '''
    
    if varType.isPrimitive:
        if varType == Type.BOOL:
            return varName + ' = ' + parcelName + '.readInt32() ? true : false'
        
        elif varType == Type.INT32:
            return varName + ' = ' + parcelName + '.readInt32()'
        
        elif varType == Type.INT64:
            return varName + ' = ' + parcelName + '.readInt64()'
        
        elif varType == Type.FLOAT32:
            return varName + ' = ' + parcelName + '.readFloat()'
        
        elif varType == Type.FLOAT64:
            return varName + ' = ' + parcelName + '.readDouble()'
        
        elif varType == Type.STRING:
            return varName + ' = ' + parcelName + '.readString16()'
        
        else:
            return '#error Deserialization of type ' + varType.name + ' not implemented'
        
    elif varType == Type.ENUM:
        return varName + ' = static_cast<' + getTypeClass(varType) + '>(' + parcelName + '.readInt32())'
    
    elif varType == Type.STRUCTURE:
        return varName + ' = ' + getTypeClass(varType) + '::readFromParcel(' + parcelName + ')'
    
    elif varType == Type.INTERFACE:
        res = ''
        
        
        res += 'sp<IBinder> ' + varName + '_binder = ' + parcelName + '.readStrongBinder();\n'
        
        res += 'if (' + varName + '_binder != NULL){ ' + varName + '= interface_cast<' + varType.name + '>(' + varName + '_binder); } else {' + varName + ' = NULL; }'
        
        return res
    
    else:
        return '#error Deserialization of type ' + varType.name + ' not implemented'

def getWriteExpr(varName, varType, parcelName):
    '''
    Creates a parcel serialization expression with given variable name and parcel name
    '''
    
    if varType.isPrimitive:
        if varType == Type.BOOL:
            return parcelName + '->writeInt32(' + varName + ' ? 1 : 0)'
        
        elif varType == Type.INT32:
            return parcelName + '->writeInt32(' + varName + ')'
        
        elif varType == Type.INT64:
            return parcelName + '->writeInt64(' + varName + ')'
        
        elif varType == Type.FLOAT32:
            return parcelName + '->writeFloat(' + varName + ')'
        
        elif varType == Type.FLOAT64:
            return parcelName + '->writeDouble(' + varName + ')'
        
        elif varType == Type.STRING:
            return parcelName + '->writeString16(' + varName + ')'
        
        else:
            return '#error Deserialization of type ' + varType.name + ' not implemented' 
        
    elif varType == Type.ENUM:
        return parcelName + '->writeInt32(static_cast<int>(' + varName + ' ))'
    
    elif varType == Type.STRUCTURE:
        return 'if (' + varName + '.get() == NULL ) { ' + parcelName + '->writeInt32(0); } else { ' + varName + '->writeToParcel(' + parcelName + '); }'
    
    elif varType == Type.INTERFACE:
        return 'if ( ' + varName + '== NULL) {'  + parcelName + '->writeStrongBinder(NULL); } else { ' + parcelName + '->writeStrongBinder(' + varName + '->asBinder()); }' 
    
    else:
        return '#error Deserialization of type ' + varType.name + ' not implemented'
    
def getIncludePath(idlType, name=None):
    path = idlType.module.package.path
    path.append(idlType.name if not name else name)
    
    if idlType == Type.INTERFACE and not name:
        path[-1] = 'I' + path[-1]
        
    return '/'.join(path) + '.h'

def namespaceStart(namespace):
    res = '// namespace %s\n' % ('::'.join(namespace))
    
    for i in namespace:
        res += 'namespace ' + i + '{'
        
    return res
    
def namespaceEnd(namespace):
    '''
    Creates a namespace start expression for given type (uses type package as namespace)
    '''
    
    return '%s // namespace %s' % ('}' * len(namespace), '::'.join(namespace))

def getHeaderGuard(idlType):
    '''
    Creates a header guard expression for given type.
    Uses a combination of package + type name.
    '''
    
    sufix = Utils.nameToDefine(idlType.name)
    
    prefix = '_'.join( [i.upper() for i in idlType.path[:-1]] )
    
    return '_' + prefix + '_' + sufix + '_H_'
    
def formatGetter(field):
    '''
    Creates a structure getter method name.
    '''
    
    prefix = 'get'
    
    if field.type == Type.BOOL:
        prefix = 'is'
        
    return prefix + field.name[0].upper() + field.name[1:]

def formatSetter(field):
    '''
    Creates a structure setter method name.
    '''
    
    return 'set' + field.name[0].upper() + field.name[1:]
