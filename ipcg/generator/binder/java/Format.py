from idl.Type import Type


def getFieldGetterName(field):
    '''
    Get Java field getter method name for given field.
    
    @param field: Object of type idl.Variable
    '''
    
    prefix = 'get'
    
    if field.type == Type.BOOL8:
        prefix = 'is'
        
    return prefix + field.name[0].upper() + field.name[1:]

def getFieldSetterName(field):
    '''
    Get Java field setter method name for given field.
    
    @param field: Object of type idl.Variable
    '''
    
    return 'set' + field.name[0].upper() + field.name[1:]
