from idl.Type import Type


def getInvalidValue(context, itype):
    valueMap = {
        Type.VOID : '',
        Type.BOOL : 'false',
        Type.FLOAT32 : '-1.0f',
        Type.STRING : 'android::String16("")',
        Type.INT32 : '-1',
        Type.FLOAT64 : '-1.0',
        Type.INT8 : '-1',
        Type.INT64 : '-1',
        Type.ENUM : 'static_cast<' + itype.name + '>(0)',
        Type.STRUCTURE : 'new ' + itype.name + '()',
    }
    
    if itype.id not in valueMap:
        return 'NULL'
    
    else:
        return valueMap[itype.id]

def getTypeName(context, idlType):
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
        Type.STRING : 'android::String16',
        Type.INTERFACE : 'android::sp<I%s>' % idlType.name
    }
    
    if idlType.id in typeMap:
        return typeMap[idlType.id]
            
    elif idlType == Type.ENUM:
        return idlType.name
    else:
        return 'android::sp<%s>' % idlType.name
    
def getArgList(context, args):
    res = ''
    
    for index, arg in enumerate(args):
        res += getTypeName(context, arg.type) + ' ' + arg.name
        
        if index  != len(args) - 1:
            res += ', '
            
    return res

def getMethodSig(context, method):
    return getTypeName(context, method.ret.type) + ' ' + method.name + '(' + getArgList(context, method.args) + ')' 

def getMethodId(context, method):
    return 'METHOD_ID_' + method.name.upper()


def getReadExpr(context, varName, varType, parcelName):
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
        return varName + ' = static_cast<' + varType.name + '>(' + parcelName + '.readInt32())'
    
    elif varType == Type.STRUCTURE:
        return varName + ' = ' + varType.name + '::readFromParcel(' + parcelName + ')'
    
    elif varType == Type.INTERFACE:
        res = ''
        
        
        res += 'sp<IBinder> ' + varName + '_binder = ' + parcelName + '.readStrongBinder();\n'
        
        res += 'if (' + varName + '_binder != NULL) ' + varName + '= interface_cast<I' + varType.name + '>(' + varName + '_binder); else ' + varName + ' = NULL;'
        
        return res
    
    else:
        return '#error Deserialization of type ' + varType.name + ' not implemented'

def getWriteExpr(context, varName, varType, parcelName):
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
        return 'if (' + varName + '.get() == NULL ) ' + parcelName + '->writeInt32(0); else ' + varName + '->writeToParcel(' + parcelName + ')'
    
    elif varType == Type.INTERFACE:
        return 'if ( ' + varName + '== NULL) '  + parcelName + '->writeStrongBinder(NULL); else ' + parcelName + '->writeStrongBinder(' + varName + '->asBinder());' 
    
    else:
        return '#error Deserialization of type ' + varType.name + ' not implemented'
    
def getIncludePath(context, idlType):
    path = idlType.path
    
    if idlType == Type.INTERFACE:
        path[-1] = 'I' + path[-1]
        
    return '/'.join(path) + '.h'
