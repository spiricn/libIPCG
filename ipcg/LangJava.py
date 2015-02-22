from idl.Type import Type


def getInvalidJavaValue(context, itype):
    valueMap = {
        Type.VOID : '',
        Type.BOOL : 'false',
        Type.FLOAT32 : '-1.0f',
        Type.STRING : '""',
        Type.INT32 : '-1',
        Type.FLOAT64 : '-1.0',
        Type.INT8 : '-1',
        Type.INT64 : '-1',
        Type.ENUM : itype.name + '.values()[0]',
        Type.STRUCTURE : 'new ' + itype.name + '()'
    }
    
    if itype.id not in valueMap:
        return 'null'
    
    else:
        return valueMap[itype.id]

def getJavaType(context, idlType):
    '''
    Maps an IDL type ID to AIDL type string
    '''

    typeMap = {
        Type.VOID : 'void',
        Type.BOOL : 'boolean',
        Type.FLOAT32 : 'float',
        Type.STRING : 'String',
        Type.INT32 : 'int',
        Type.FLOAT64 : 'double',
        Type.INT8 : 'byte',
        Type.INT64 : 'long',
    }
    
    if idlType.isPrimitive:
        if idlType.id not in typeMap:
            raise RuntimeError('Unsupported type %d' % idlType.id)
        
        else:
            return typeMap[idlType.id]
    else:
        return idlType.name
    
def getJavaMethodArgList(context, args):
    res = ''
    
    for index, arg in enumerate(args):
        res += getJavaType(context, arg.type) + ' ' + arg.name
        
        if index  != len(args) - 1:
            res += ', '
            
    return res

def getAIDLMethodArgList(context, args):
    res = ''
    
    for index, arg in enumerate(args):
        if arg.type in [Type.STRUCTURE, Type.INTERFACE]:
            res += 'in' if arg.mod(Type.MOD_IN) else 'out' if arg.mod(Type.MOD_OUT) else 'inout'
            res += ' '
            
        res += getJavaType(context, arg.type) + ' ' + arg.name
        
        if index  != len(args) - 1:
            res += ', '
            
    return res
