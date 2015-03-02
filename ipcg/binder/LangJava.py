from idl.Type import Type

def getDefaultValue(itype):
    '''
    Gets a default value for given type (i.e. the value a variable should be initialized to).
    '''
    
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

def getTypeName(itype):
    '''
    Maps an IDL type ID to Java type string
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
    
    if itype.isPrimitive:
        if itype.id not in typeMap:
            raise RuntimeError('Unsupported type %d' % itype.id)
        
        else:
            return typeMap[itype.id]
    else:
        return '.'.join(itype.path)
    
def getMethodArgList(args, isAidl):
    '''
    Gets Java or AIDL method argument list string.
    '''
    
    res = ''
    
    for index, arg in enumerate(args):
        if arg.type in [Type.STRUCTURE, Type.INTERFACE,Type.ENUM] and isAidl:
            res += 'in' if arg.mod(Type.MOD_IN) else 'out' if arg.mod(Type.MOD_OUT) else 'inout'
            res += ' '
            
        res += getTypeName(arg.type) + ' ' + arg.name
        
        if index  != len(args) - 1:
            res += ', '
            
    return res

def getJavaMethodArgList(args):
    '''
    Gets Java method argument list string.
    '''
    
    return getMethodArgList(args, isAidl=False)

def getAIDLMethodArgList(args):
    '''
    Gets AIDL method argument list string.
    '''
    
    return getMethodArgList(args, isAidl=True)

def formatGetter(field):
    '''
    Format Java field getter method name for given field.
    '''
    
    prefix = 'get'
    
    if field.type == Type.BOOL:
        prefix = 'is'
        
    return prefix + field.name[0].upper() + field.name[1:]

def formatSetter(field):
    '''
    Format Java field setter method name for given field.
    '''
    
    return 'set' + field.name[0].upper() + field.name[1:]
