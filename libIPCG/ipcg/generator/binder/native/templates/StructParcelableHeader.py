<%!
import ipcg.generator.binder.native.NativeUtils as NativeUtils
import ipcg.generator.binder.native.Format as Format
%>

<%
headerGuard = struct.name.upper() + '_H'
%>

#ifndef ${headerGuard}
#define ${headerGuard}

// Dependency includes
% for i in struct.dependencies:
// ${i.name}
#include "${NativeUtils.getIncludePath(i)}"
% endfor
#include <binder/Parcel.h>
#include <utils/Vector.h>

${NativeUtils.namespaceStart(struct.path[:-1])}
                 
class ${struct.name} : public android::LightRefBase<${struct.name}> {
public:
    // Default constructor
    ${struct.name}();
    
    // Copy constructor
    ${struct.name}(const ${struct.name}& other);
    
    // Destructor
    virtual ~${struct.name}();
    
    // Object deserialization
    static android::sp<${struct.name}> readFromParcel(const android::Parcel& data);

    // Object serialization
    android::status_t writeToParcel(android::Parcel* data) const;
    
    // Field getters
% for field in struct.fields:
    ${NativeUtils.getTypeClassInstance(field)} ${Format.getFieldGetterName(field)}() const;
% endfor
    
    // Field setters
% for field in struct.fields:
    ${struct.name}* ${Format.getFieldSetterName(field)}(const ${NativeUtils.getTypeClassInstance(field)}& value);
% endfor

private:
    // Member fields
% for field in struct.fields:
    ${NativeUtils.getTypeClassInstance(field)} ${field.name};
% endfor
    
private:
    friend class android::LightRefBase<${struct.name}>;
    
}; // ${struct.name}
                 
${NativeUtils.namespaceEnd(struct.path[:-1])}


#endif // ${headerGuard}
 