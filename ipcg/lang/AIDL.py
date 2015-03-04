from idl.Type import Type


def getTypeName(var):
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
    
    if isinstance(var, Type):
        if var.isPrimitive:
            if var.id not in typeMap:
                raise RuntimeError('Unsupported type %d' % var.id)
            
            else:
                return typeMap[var.id]
        else:
            return '.'.join(var.path)
    else:
        if var.isArray:
            return 'List<' + getTypeName(var.type) + '>'
    
        else:
            return getTypeName(var.type)
        
def getMethodArgList(args):
    '''
    Gets AIDL method argument list string.
    '''
    
    res = ''
    
    for index, arg in enumerate(args):
        if arg.type in [Type.STRUCTURE, Type.INTERFACE,Type.ENUM]:
            res += 'in' if arg.mod(Type.MOD_IN) else 'out' if arg.mod(Type.MOD_OUT) else 'inout'
            res += ' '
            
        res += getTypeName(arg) + ' ' + arg.name
        
        if index  != len(args) - 1:
            res += ', '
            
    return res

def getMethodSig(method):
    '''
    Gets AIDL method signature (i.e. return type + name + argument list )
    '''
    
    return getTypeName(method.ret) + ' ' + method.name + '(' + getMethodArgList(method.args) + ')'
