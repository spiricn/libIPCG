from idl.Type import Type

from ipcg.lang.Java import getTypeName, getDefaultValue


def getReadExpr(varName, var, parcelName):
    '''
    Creates a parcel deserialization expression with given variable name and parcel name
    '''
    
    if isinstance(var, Type):
        if var.isPrimitive:
            if var == Type.BOOL:
                return varName + ' = ' + parcelName + '.readInt() == 1 ? true : false'
            
            elif var == Type.INT32:
                return varName + ' = ' + parcelName + '.readInt()'
            
            elif var == Type.INT64:
                return varName + ' = ' + parcelName + '.readLong()'
            
            elif var == Type.FLOAT32:
                return varName + ' = ' + parcelName + '.readFloat()'
            
            elif var == Type.FLOAT64:
                return varName + ' = ' + parcelName + '.readDouble()'
            
            elif var == Type.STRING:
                return varName + ' = ' + parcelName + '.readString()'
            
            else:
                return '#error Deserialization of type ' + var.name + ' not implemented'
            
        elif var.id in [Type.ENUM, Type.STRUCTURE]:
            return varName + ' = ' +  getTypeName(var) + '.CREATOR.createFromParcel(' + parcelName + ')'
        
        else:
            return '#error Deserialization of type ' + var.name + ' not implemented'
        
    else:
        if var.isArray:
            arraySizeVar = '__arraySize_' + var.name
            
            res = ''
            
            res += 'int ' + arraySizeVar + ' = ' + parcelName + '.readInt();' + '\n'
            
            res += 'for(int i=0; i<' + arraySizeVar + '; i++){' + '\n'
            
            
            tmpVarName = '__tmpVar_' + var.name
            
            res += getTypeName(var.type) + ' ' + tmpVarName + ' = ' + getDefaultValue(var.type) + ';' + '\n'
            
            res += getReadExpr(tmpVarName, var.type, parcelName) + ';' + '\n'
            
            res += varName + '.add('+ tmpVarName + ');\n'
            
            res += '}' + '\n' 
            
            
            
            return res
        
        else:
            return getReadExpr(varName, var.type, parcelName)

def getWriteExpr(varName, var, parcelName):
    '''
    Creates a parcel serialization expression with given variable name and parcel name
    '''
    
    if isinstance(var, Type):
        if var.isPrimitive:
            # Primitive type
            
            if var == Type.BOOL:
                return parcelName + '.writeInt(' + varName + ' ? 1 : 0)'
            
            elif var == Type.INT32:
                return parcelName + '.writeInt(' + varName + ')'
            
            elif var == Type.INT64:
                return parcelName + '.writeLong(' + varName + ')'
            
            elif var == Type.FLOAT32:
                return parcelName + '.writeFloat(' + varName + ')'
            
            elif var == Type.FLOAT64:
                return parcelName + '.writeDouble(' + varName + ')'
            
            elif var == Type.STRING:
                return parcelName + '.writeString(' + varName + ')'
            
            else:
                return '#error Deserialization of type ' + var.name + ' not implemented' 
            
        elif var.id in [Type.ENUM, Type.STRUCTURE]:
            # Structure or enumeration
            return varName + '.writeToParcel(' + parcelName + ', flags)'
    
        else:
            return '#error Deserialization of type ' + var.name + ' not implemented'
        
    else:
        if var.isArray:
            # Array
            res = ''
            
            res += parcelName + '.writeInt(' + varName + '.size() );' + '\n'
            
            res += 'for(' + getTypeName(var.type) + ' i : ' + varName + '){\n'
            
            res += '\t\t' + getWriteExpr('i', var.type, parcelName) + ';' + '\n'
            res += '}\n'
            
            return res
    
        else:
            return getWriteExpr(varName, var.type, parcelName)

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
