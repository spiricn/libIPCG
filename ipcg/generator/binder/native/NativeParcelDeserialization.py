from idl.Type import Type
from idl.Variable import Variable

from ipcg.generator.binder.native.NativeUtils import getTypeName, \
    getDefaultValue


def getReadExpr(varName, var, parcelName):
    '''
    Creates a parcel deserialization expression with given variable name and parcel name

    @param varName: Name of the variable to be deserialized
    @param var: Object of type idl.Type or idl.Variable
    @param parcelName: Name of the parcel variable
    '''

    if isinstance(var, Type) and var.isPrimitive:
        # Primitive deserialization
        return getReadExprPrimitive(varName, var, parcelName)

    if isinstance(var, Type) and var.id in [Type.ENUM, Type.STRUCTURE, Type.INTERFACE]:
        # Parcelable class deserializatoin
        return getReadExprParcelable(varName, var, parcelName)

    elif isinstance(var, Variable) and var.isArray:
        # Array deserialization
        return getReadExprArray(varName, var, parcelName)

    elif isinstance(var, Variable) and not var.isArray:
        # Variable deserialization (i.e. either primitive or parcelable)
        return getReadExpr(varName, var.type, parcelName)

    else:
        raise NotImplementedError('Deserialization of type %r not yet implemented', var.name)

def getReadExprPrimitive(varName, typeObj, parcelName):
    '''
    Create an expression for deserializing a primitive type from a parcel

    @param varName: Name of the variable to be deserialized
    @param typeObj: Object of type idl.Type
    @param parcelName: Name of the parcel variable
    '''

    if typeObj == Type.BOOL:
        return varName + ' = ' + parcelName + '.readInt32() ? true : false'

    elif typeObj == Type.INT32:
        return varName + ' = ' + parcelName + '.readInt32()'

    elif typeObj == Type.INT64:
        return varName + ' = ' + parcelName + '.readInt64()'

    elif typeObj == Type.FLOAT32:
        return varName + ' = ' + parcelName + '.readFloat()'

    elif typeObj == Type.FLOAT64:
        return varName + ' = ' + parcelName + '.readDouble()'

    elif typeObj == Type.STRING:
        return varName + ' = ' + parcelName + '.readString16()'

    else:
        raise NotImplementedError('Deserialization of type %r not implemented' % typeObj.name)

def getReadExprParcelable(varName, typeObj, parcelName):
    '''
    Create an expression for deserializing parcelable class from a parcel

    @param varName: Name of the variable to be deserialized
    @param typeObj: Object of type idl.Type
    @param parcelName: Name of the parcel variable
    '''

    if typeObj == Type.ENUM:
        return varName + ' = static_cast<' + getTypeName(typeObj) + '>(' + parcelName + '.readInt32())'

    elif typeObj == Type.STRUCTURE:
        return varName + ' = ' + getTypeName(typeObj) + '::readFromParcel(' + parcelName + ')'

    elif typeObj == Type.INTERFACE:
        res = ''


        res += 'sp<IBinder> ' + varName + '_binder = ' + parcelName + '.readStrongBinder();\n'

        res += 'if (' + varName + '_binder != NULL){ ' + varName + '= interface_cast<' + typeObj.name + '>(' + varName + '_binder); } else {' + varName + ' = NULL; }'

        return res

    else:
        raise NotImplementedError('Deserialization of type %r not implemented' % typeObj.name)

def getReadExprArray(varName, var, parcelName):
    '''
    Create an expression for deserializing an array from a parcel

    @param varName: Name of the variable to be deserialized
    @param var: Object of type idl.Variable
    @param parcelName: Name of the parcel variable
    '''


    res = ''

    res += '{' + '\n'

    # TODO NULL arrays support
    res += 'int __arraySize = ' + parcelName + '.readInt32();' + '\n'

    res += 'for(int i=0; i<__arraySize; i++){' + '\n'

    res += getTypeName(var.type) + ' __tmpElem = ' + getDefaultValue(var.type) + ';\n'

    res += getReadExpr('__tmpElem', var.type, parcelName) + ';\n'

    res += varName + '->push_back(__tmpElem);' + '\n'

    res += '}\n'

    res += '}' + '\n'


    return res

