from idl.Type import Type
from idl.Variable import Variable

from ipcg.generator.binder.java.JavaUtils import getTypeName


def getWriteExpr(varName, var, parcelName):
    '''
    Creates a parcel serialization expression with given variable name and parcel name
    
    @param varName: Name of the variable to be serialized
    @param var: Object of type idl.Type or idl.Variable
    @param parcelName: Name of the parcel variable
    '''
    
    if isinstance(var, Type) and var.isPrimitive:
        # Primitive deserialization
        return getWriteExprPrimitive(varName, var, parcelName)
            
    if isinstance(var, Type) and var.id in [Type.ENUM, Type.STRUCTURE]:
        # Parcelable class deserializatoin
        return getWriteExprParcelable(varName, var, parcelName)
        
    elif isinstance(var, Variable) and var.isArray:
        # Array deserialization
        return getWriteExprArray(varName, var, parcelName)
          
    elif isinstance(var, Variable) and not var.isArray:
        # Variable deserialization (i.e. either primitive or parcelable)
        return getWriteExpr(varName, var.type, parcelName)
    
    else:
        # TODO Add interface support
        raise NotImplementedError('Serialization of type %r not yet implemented', var.name)
        
def getWriteExprPrimitive(varName, typeObj, parcelName):
    '''
    Create an expression for serializing a primitive type to a parcel
    
    @param varName: Name of the variable to be serialized
    @param typeObj: Object of type idl.Type 
    @param parcelName: Name of the parcel variable
    '''
    
    if typeObj == Type.BOOL:
        return parcelName + '.writeInt(' + varName + ' ? 1 : 0)'
    
    elif typeObj == Type.INT32:
        return parcelName + '.writeInt(' + varName + ')'
    
    elif typeObj == Type.INT64:
        return parcelName + '.writeLong(' + varName + ')'
    
    elif typeObj == Type.FLOAT32:
        return parcelName + '.writeFloat(' + varName + ')'
    
    elif typeObj == Type.FLOAT64:
        return parcelName + '.writeDouble(' + varName + ')'
    
    elif typeObj == Type.STRING:
        return parcelName + '.writeString(' + varName + ')'
    
    else:
        raise RuntimeError('Deserialization of type %r not implemented' % typeObj.name)
    
def getWriteExprParcelable(varName, typeObj, parcelName):
    '''
    Create an expression for serializing parcelable class to a parcel
    
    @param varName: Name of the variable to be serialized
    @param typeObj: Object of type idl.Type 
    @param parcelName: Name of the parcel variable
    '''
    
    res = ''
    
    res += 'if(' + varName + ' != null){'
    
    res += parcelName + '.writeInt(1);' + '\n'
    
    res += varName + '.writeToParcel(' + parcelName + ', flags);' + '\n'
    
    res += '} else {' + '\n'
    
    res += parcelName + '.writeInt(0);' + '\n'
    
    res += '}' + '\n'
    
    
    return res

def getWriteExprArray(varName, var, parcelName):
    '''
    Create an expression for serializing an array to a parcel
    
    @param varName: Name of the variable to be serialized
    @param var: Object of type idl.Variable 
    @param parcelName: Name of the parcel variable
    '''

    # TODO NULL arrays support

    res = ''
    
    res += parcelName + '.writeInt(' + varName + '.size() );' + '\n'
    
    res += 'for(' + getTypeName(var.type) + ' i : ' + varName + '){\n'
    
    res += '\t\t' + getWriteExpr('i', var.type, parcelName) + ';' + '\n'
    res += '}\n'
    
    return res
