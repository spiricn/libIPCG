from idl.Type import Type
from idl.Variable import Variable

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
            
    if isinstance(var, Type) and var.id in [Type.ENUM, Type.STRUCTURE, Type.INTERFACE]:
        # Parcelable class deserializatoin
        return getWriteExprParcelable(varName, var, parcelName)
        
    elif isinstance(var, Variable) and var.isArray:
        # Array deserialization
        return getWriteExprArray(varName, var, parcelName)
          
    elif isinstance(var, Variable) and not var.isArray:
        # Variable deserialization (i.e. either primitive or parcelable)
        return getWriteExpr(varName, var.type, parcelName)
    
    else:
        raise NotImplementedError('Serialization of type %r not yet implemented', var.name)
    
def getWriteExprPrimitive(varName, typeObj, parcelName):
    if typeObj == Type.BOOL:
        return parcelName + '->writeInt32(' + varName + ' ? 1 : 0)'
    
    elif typeObj == Type.INT32:
        return parcelName + '->writeInt32(' + varName + ')'
    
    elif typeObj == Type.INT64:
        return parcelName + '->writeInt64(' + varName + ')'
    
    elif typeObj == Type.FLOAT32:
        return parcelName + '->writeFloat(' + varName + ')'
    
    elif typeObj == Type.FLOAT64:
        return parcelName + '->writeDouble(' + varName + ')'
    
    elif typeObj == Type.STRING:
        return parcelName + '->writeString16(' + varName + ')'
    
    else:
        raise NotImplementedError('Deserialization of type %r not implemented' % typeObj.name)
                
def getWriteExprParcelable(varName, typeObj, parcelName):
    if typeObj == Type.ENUM:
        return parcelName + '->writeInt32(static_cast<int>(' + varName + ' ))'
    
    elif typeObj == Type.STRUCTURE:
        return 'if (' + varName + '.get() == NULL ) { ' + parcelName + '->writeInt32(0); } else { ' + varName + '->writeToParcel(' + parcelName + '); }'
    
    elif typeObj == Type.INTERFACE:
        return 'if ( ' + varName + '== NULL) {'  + parcelName + '->writeStrongBinder(NULL); } else { ' + parcelName + '->writeStrongBinder(' + varName + '->asBinder()); }'
     
def getWriteExprArray(varName, var, parcelName):
    res = ''
    
    # TODO NULL arrays support
    
    res += parcelName + '->writeInt32(' + varName + '->size() );' + '\n'
    
    res += 'for(size_t i=0; i<' + varName + '->size(); i++){' + '\n'
    
    elemName = '(' + varName + '->itemAt(i))'
    
    res += getWriteExpr(elemName, var.type, parcelName) + ';\n'
    
    res += '}' + '\n'
    
    return res
