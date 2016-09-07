from idl.Type import Type

def nameToDefine(name):
    return name + '_TODO________'

def getTypeClass(var):
    if isinstance(var, Type) and var.isPrimitive:
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

        else:
            # TODO
            raise NotImplementedError()

    elif isinstance(var, Type) and var.id in [Type.ENUM, Type.STRUCTURE, Type.INTERFACE]:
        return '::'.join(var.path)

    elif var.isArray:
        # TODO
        raise NotImplementedError()

    else:
        return getTypeClass(var.type)

def getTypeClassInstance(var):
    '''
    Maps an IDL type ID to C++ type string
    '''

    if isinstance(var, Type) and var.isPrimitive:
        return getTypeClass(var)

    elif isinstance(var, Type) and var.id in [Type.ENUM, Type.STRUCTURE, Type.INTERFACE]:
        typeClass = getTypeClass(var)

        if var.id in [Type.STRUCTURE, Type.INTERFACE]:
            # Use smart pointers only for structures and interfaces
            return 'android::sp<' + typeClass + '>'

        else:
            return typeClass

    elif var.isArray:
        # TODO
        raise NotImplementedError()

    else:
        return getTypeClassInstance(var.type)

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
            # TODO
            raise NotImplementedError()

        else:
            return getDefaultValue(var.type)



def getArgList(args):
    '''
    Get a method argument list string.
    '''

    res = ''

    for index, arg in enumerate(args):
        res += getTypeClassInstance(arg.type) + ' ' + arg.name

        if index != len(args) - 1:
            res += ', '

    return res

def getMethodSig(method):
    '''
    Gets a method signature string (i.e. returnType + name + argList)
    '''

    return getTypeClassInstance(method.ret.type) + ' ' + method.name + '(' + getArgList(method.args) + ')'

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

    sufix = nameToDefine(idlType.name)

    prefix = '_'.join([i.upper() for i in idlType.path[:-1]])

    return '_' + prefix + '_' + sufix + '_H_'

