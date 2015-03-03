<%!
from idl.Type import Type
import ipcg.binder.LangCPP as Lang
%>

#include "${Lang.getIncludePath(struct)}"

#include <utils/Log.h>

#ifdef LOG_TAG
#undef LOG_TAG
#endif

#define LOG_TAG "${namespace}_${struct.name}"

using namespace android;

${Lang.namespaceStart(struct.path[:-1])}

// Constructor
${struct.name}::${struct.name}(){
    // Member initialization
% for field in struct.fields:
    this->${field.name} = ${Lang.getDefaultValue(field)};
% endfor
}

// Copy constructor
${struct.name}::${struct.name}(const ${struct.name}& other){
                                                            
% for field in struct.fields:
    % if field.type.isPrimitive or field.type == Type.ENUM:
        this->${field.name} = other.${field.name};
    % elif field.type == Type.STRUCTURE:
        if(other.${field.name}.get()){
            this->${field.name} = new ${Lang.getTypeClass(field)}(*other.${field.name}.get());
        }
        else{
             this->${field.name} = NULL;
        }
    % else:
    #error Field '${field.type.name}' type copy not supported
    % endif
% endfor
}

// Destructor                       
${struct.name}::~${struct.name}(){                                
}

// Deserialization
sp<${struct.name}> ${struct.name}::readFromParcel(const Parcel& data){
    // Check if there is valid data in the parcel
    if(data.readInt32() == 0){
        // No data
        return NULL;
    }
    
    ${struct.name}* res = new ${struct.name};
    
% for field in struct.fields:
    ${Lang.getReadExpr('res->' + field.name, field, 'data')};
% endfor

    return res;
}

// Serialization
status_t ${struct.name}::writeToParcel(Parcel* data) const{
    // Write 1 to indicate we have valid data in the parcel
    data->writeInt32(1);
    
% for field in struct.fields:
    ${Lang.getWriteExpr('this->' + field.name, field, 'data')};
% endfor
    
    return NO_ERROR;
}

// Field getters
% for field in struct.fields:
${Lang.getTypeName(field)} ${struct.name}::${Lang.formatGetter(field)}() const{
    return this->${field.name};
}
% endfor

// Field setters
% for field in struct.fields:
${struct.name}* ${struct.name}::${Lang.formatSetter(field)}(const ${Lang.getTypeName(field)}& value){
    this->${field.name} = value;
    
    return this;
}
% endfor

bool ${struct.name}::operator==(const ${Lang.getTypeClass(struct)}& other) const{
                                                                                                                                             
% for field in struct.fields:
    % if field.type.isPrimitive or field.type == Type.ENUM:
        if(this->${field.name} != other.${field.name}){
            return false;
        }
    % elif field.type == Type.STRUCTURE:
        if(this->${field.name}.get() && other.${field.name}.get()){
            if(*this->${field.name}.get() != *other.${field.name}.get()){
                return false;
            }
        }
        else if(this->${field.name}.get() != other.${field.name}.get()){
             return false;
        }
    % else:
    #error Field '${field.type.name}' type copy not supported
    % endif
% endfor

    return true;
}


bool ${struct.name}::operator!=(const ${Lang.getTypeClass(struct)}& other) const{
    return !(*this == other);
}

${Lang.namespaceEnd(struct.path[:-1])}
