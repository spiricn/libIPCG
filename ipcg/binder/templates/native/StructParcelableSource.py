<%namespace name="Lang" module="ipcg.LangCPP"/>

<%

from idl.Type import Type

%>

#include "${Lang.getIncludePath(struct)}"

#include <utils/Log.h>

#ifdef LOG_TAG
#undef LOG_TAG
#endif

#define LOG_TAG "${namespace}_${struct.name}"

using namespace android;

namespace ${namespace} {

// Constructor
${struct.name}::${struct.name}(){
    // Member initialization
% for field in struct.fields:
    this->${field.name} = ${Lang.getInvalidValue(field.type)};
% endfor
}

// Destructor                       
${struct.name}::~${struct.name}(){                                
}

// Deserialization
sp<${struct.name}> ${struct.name}::readFromParcel(const Parcel &data){
    // Check if there is valid data in the parcel
    if(data.readInt32() == 0){
        // No data
        return NULL;
    }
    
    ${struct.name}* res = new ${struct.name};
    
% for field in struct.fields:
    ${Lang.getReadExpr('res->' + field.name, field.type, 'data')};
% endfor

    return res;
}

// Serialization
status_t ${struct.name}::writeToParcel(Parcel* data) const{
    // Write 1 to indicate we have valid data in the parcel
    data->writeInt32(1);
    
% for field in struct.fields:
    ${Lang.getWriteExpr('this->' + field.name, field.type, 'data')};
% endfor
    
    return NO_ERROR;
}

// Field getters
% for field in struct.fields:
${Lang.getTypeName(field.type)} ${struct.name}::get${field.name}() const{
    return this->${field.name};
}
% endfor

// Field setters
% for field in struct.fields:
void ${struct.name}::set${field.name}(const ${Lang.getTypeName(field.type)}& value){
    this->${field.name} = value;
}
% endfor

}; // namespace ${namespace}
