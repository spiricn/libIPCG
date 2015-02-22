<%namespace name="Lang" module="ipcg.LangCPP"/>

<%

from idl.Type import Type

headerGuard = struct.name.upper() + '_H'

%>
#ifndef ${headerGuard}
#define ${headerGuard}

// Dependency includes
% for i in struct.dependencies:
#include "${Lang.getIncludePath(i)}"
% endfor
#include <binder/Parcel.h>

namespace ${namespace} {
                 
class ${struct.name} : public android::LightRefBase<${struct.name}> {
public:
    // Default constructor
    ${struct.name}();
    
    // Destructor
    virtual ~${struct.name}();
    
    // Object deserialization
    static android::sp<${struct.name}> readFromParcel(const android::Parcel &data);

    // Object serialization
    android::status_t writeToParcel(android::Parcel* data) const;
    
    // Field getters
% for field in struct.fields:
    ${Lang.getTypeName(field.type)} get${field.name}() const;
% endfor
    
    // Field setters
% for field in struct.fields:
    void set${field.name}(const ${Lang.getTypeName(field.type)}& value);
% endfor

private:
    // Member fields
% for field in struct.fields:
    ${Lang.getTypeName(field.type)} ${field.name};
% endfor
    
private:
    friend class android::LightRefBase<${struct.name}>;
    
}; // ${struct.name}
                 
}; // namespace ${namespace}

#endif // ${headerGuard}
 