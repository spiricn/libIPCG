from idl.Type import Type


def getDefaultValue(var):
    '''
    Gets a default value for given type (i.e. the value a variable should be initialized to by default).
    '''
    
    if isinstance(var, Type):
        valueMap = {
            Type.VOID : '',
            Type.BOOL8 : 'false',
            Type.FLOAT32 : '-1.0f',
            Type.STRING : '""',
            Type.INT32 : '-1',
            Type.FLOAT64 : '-1.0',
            Type.INT8 : '-1',
            Type.INT64 : '-1',
            Type.ENUM : 'null',
            Type.STRUCTURE : 'null',
        }
    
        if var.id not in valueMap:
            return 'null'
        
        elif var.id in valueMap:
            return valueMap[var.id]
        
        else:
            raise NotImplementedError('Default value for %r not implemented' % var.name)
        
    elif var.isArray:
        return 'new ArrayList<' + getTypeName(var.type) + '>()'
    
    else:
        return getDefaultValue(var.type)
        
def getTypeName(var):
    '''
    Maps an IDL type ID to Java type string
    '''

    typeMap = {
        Type.VOID : 'void',
        Type.BOOL8 : 'boolean',
        Type.FLOAT32 : 'float',
        Type.STRING : 'String',
        Type.INT32 : 'int',
        Type.FLOAT64 : 'double',
        Type.INT8 : 'byte',
        Type.INT64 : 'long',
    }
    
    if isinstance(var, Type):
        if var.isPrimitive:
            if var.id in typeMap:
                return typeMap[var.id]
            
            else:
                raise RuntimeError('Not implemented')
                
        else:
            return '.'.join(var.path)
        
    elif var.isArray:
        return 'List<' + getTypeName(var.type) + '>'

    else:
        return getTypeName(var.type)

def getMethodArgList(args):
    '''
    Gets Java method argument list string.
    '''
    
    res = ''
    
    for index, arg in enumerate(args):
        res += getTypeName(arg) + ' ' + arg.name
        
        if index  != len(args) - 1:
            res += ', '
            
    return res

def getMethodSig(method):
    '''
    Gets Java method signature (i.e. return type + name + argument list )
    '''
    
    return getTypeName(method.ret) + ' ' + method.name + '(' + getMethodArgList(method.args) + ')'
