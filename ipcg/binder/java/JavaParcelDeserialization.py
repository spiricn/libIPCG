from idl.Type import Type
from idl.Variable import Variable
from ipcg.lang.Java import getTypeName, getDefaultValue

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
            
    if isinstance(var, Type) and var.id in [Type.ENUM, Type.STRUCTURE]:
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
        # TODO Use byte for boolean ?
        return varName + ' = ' + parcelName + '.readInt() == 1 ? true : false'
    
    elif typeObj == Type.INT32:
        return varName + ' = ' + parcelName + '.readInt()'
    
    elif typeObj == Type.INT64:
        return varName + ' = ' + parcelName + '.readLong()'
    
    elif typeObj == Type.FLOAT32:
        return varName + ' = ' + parcelName + '.readFloat()'
    
    elif typeObj == Type.FLOAT64:
        return varName + ' = ' + parcelName + '.readDouble()'
    
    elif typeObj == Type.STRING:
        return varName + ' = ' + parcelName + '.readString()'
    
    else:
        raise NotImplementedError('Deserialization of primitive type %r not yet implemented' % typeObj.name)
    
def getReadExprParcelable(varName, typeObj, parcelName):
    '''
    Create an expression for deserializing parcelable class from a parcel
    
    @param varName: Name of the variable to be deserialized
    @param typeObj: Object of type idl.Type 
    @param parcelName: Name of the parcel variable
    '''
    
    res = ''
    
    res += 'if(' + parcelName + '.readInt() == 1){' + '\n'
    
    res += varName + ' = ' + getTypeName(typeObj) + '.CREATOR.createFromParcel(' + parcelName + ');' + '\n'
    
    res += '} else{' + '\n'
    
    res += varName + ' = null;' + '\n'
    
    res += '}' + '\n'
    
    return res

def getReadExprArray(varName, var, parcelName):
    '''
    Create an expression for deserializing an array from a parcel
    
    @param varName: Name of the variable to be deserialized
    @param var: Object of type idl.Variable 
    @param parcelName: Name of the parcel variable
    '''
    
    arraySizeVar = '__arraySize_' + var.name
    
    res = ''
    
    res += varName + ' = new ArrayList<' + getTypeName(var.type) + '>();\n'
    
    res += 'int ' + arraySizeVar + ' = ' + parcelName + '.readInt();' + '\n'
    
    res += 'for(int i=0; i<' + arraySizeVar + '; i++){' + '\n'
    
    
    tmpVarName = '__tmpVar_' + var.name
    
    res += getTypeName(var.type) + ' ' + tmpVarName + ' = ' + getDefaultValue(var.type) + ';' + '\n'
    
    res += getReadExpr(tmpVarName, var.type, parcelName) + ';' + '\n'
    
    res += varName + '.add(' + tmpVarName + ');\n'
    
    res += '}' + '\n' 
    
    
    return res
