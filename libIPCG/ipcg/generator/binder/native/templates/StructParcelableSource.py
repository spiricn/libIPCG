<%!
from idl.Type import Type
import ipcg.generator.binder.native.NativeUtils as NativeUtils
import ipcg.generator.binder.native.Format as Format
import ipcg.generator.binder.native.NativeParcelSerialization as NativeParcelSerialization
import ipcg.generator.binder.native.NativeParcelDeserialization as NativeParcelDeserialization
%>

#include "${NativeUtils.getIncludePath(struct)}"

#include <utils/Log.h>

#ifdef LOG_TAG
#undef LOG_TAG
#endif

#define LOG_TAG "${':'.join(struct.path)}"

using namespace android;

${NativeUtils.namespaceStart(struct.path[:-1])}

// Constructor
${struct.name}::${struct.name}(){
    // Member initialization
% for field in struct.fields:
    this->${field.name} = ${NativeUtils.getDefaultValue(field)};
% endfor
}

// Copy constructor
${struct.name}::${struct.name}(const ${struct.name}& other){
                                                            
% for field in struct.fields:
    % if field.type.isPrimitive or field.type == Type.ENUM:
        this->${field.name} = other.${field.name};
    % elif field.isArray:
        #warning "Array copy not implemented"
    % elif field.type == Type.STRUCTURE:
        if(other.${field.name}.get()){
            this->${field.name} = new ${NativeUtils.getTypeClass(field)}(*other.${field.name}.get());
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
    // TODO Delete non-null arrays
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
    ${NativeParcelDeserialization.getReadExpr('res->' + field.name, field, 'data')};
% endfor

    return res;
}

// Serialization
status_t ${struct.name}::writeToParcel(Parcel* data) const{
    // Write 1 to indicate we have valid data in the parcel
    data->writeInt32(1);
    
% for field in struct.fields:
    ${NativeParcelSerialization.getWriteExpr('this->' + field.name, field, 'data')};
% endfor
    
    return NO_ERROR;
}

// Field getters
% for field in struct.fields:
${NativeUtils.getTypeName(field)} ${struct.name}::${Format.getFieldGetterName(field)}() const{
    return this->${field.name};
}
% endfor

// Field setters
% for field in struct.fields:

## Array field setters not supported for now
% if not field.isArray:
${struct.name}* ${struct.name}::${Format.getFieldSetterName(field)}(const ${NativeUtils.getTypeName(field)}& value){
    this->${field.name} = value;
    
    return this;
}
% endif
% endfor

${NativeUtils.namespaceEnd(struct.path[:-1])}
