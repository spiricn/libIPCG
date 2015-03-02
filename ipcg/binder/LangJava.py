from idl.Type import Type

def getDefaultValue(var):
    '''
    Gets a default value for given type (i.e. the value a variable should be initialized to).
    '''
    
    if isinstance(var, Type):
        valueMap = {
            Type.VOID : '',
            Type.BOOL : 'false',
            Type.FLOAT32 : '-1.0f',
            Type.STRING : '""',
            Type.INT32 : '-1',
            Type.FLOAT64 : '-1.0',
            Type.INT8 : '-1',
            Type.INT64 : '-1',
            Type.ENUM : var.name + '.values()[0]',
            Type.STRUCTURE : 'new ' + var.name + '()'
        }
    
        if var.id not in valueMap:
            return 'null'
        
        else:
            return valueMap[var.id]
    else:
        if var.isArray:
            return 'new ArrayList<' + getTypeName(var.type) + '>()'
        else:
            return getDefaultValue(var.type)
    

def getTypeName(var):
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
      
def getMethodArgList(args, isAidl):
    '''
    Gets Java or AIDL method argument list string.
    '''
    
    res = ''
    
    for index, arg in enumerate(args):
        if arg.type in [Type.STRUCTURE, Type.INTERFACE,Type.ENUM] and isAidl:
            res += 'in' if arg.mod(Type.MOD_IN) else 'out' if arg.mod(Type.MOD_OUT) else 'inout'
            res += ' '
            
        res += getTypeName(arg) + ' ' + arg.name
        
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
