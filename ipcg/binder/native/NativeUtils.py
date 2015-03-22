from idl.Type import Type

from ipcg import Utils


def getDefaultValue(var):
    '''
    Gets a default value for given type (i.e. the value a variable should be initialized to).
    '''
    
    if isinstance(var, Type):
        if var.isPrimitive:
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
            }[var.id]
    
        elif var == Type.ENUM:
            # Enumeration
            return 'static_cast<' + getTypeClass(var) + '>(' + str(var.fields[0].value) + ')'
        
        elif var == Type.STRUCTURE:
            # Structure
            return 'new ' + getTypeClass(var) + '()'
            
        else:
            return 'NULL'
    
    else:
        if var.isArray:
            return 'new android::Vector<' + getTypeClass(var.type) + '>()'
        
        else:
            return getDefaultValue(var.type)

def getTypeClass(var):
    '''
    Gets a class name with namespace of given type (e.g. com::example::test::MyInterface)
    '''
    
    if isinstance(var, Type):
        if var.id in [Type.INTERFACE, Type.STRUCTURE, Type.ENUM]:
            return '::'.join(var.path) 
        else:
            raise RuntimeError('Invalid type %s' % str(var))
    else:
        if var.isArray:
            # TODO
            pass
        
        else:
            return getTypeClass(var.type)

def getTypeName(var):
    '''
    Maps an IDL type ID to C++ type string
    '''

    if isinstance(var, Type):
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
        
        if var.id in typeMap:
            return typeMap[var.id]
                
        elif var == Type.ENUM:
            return getTypeClass(var)
        
        else:
            return 'android::sp<' + getTypeClass(var) + '>'
        
    else:
        if var.isArray:
            return 'android::sp<android::Vector<' + getTypeClass(var.type)  + '> >'
        
        else:
            return getTypeName(var.type)
    
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

