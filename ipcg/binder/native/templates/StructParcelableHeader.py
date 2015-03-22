<%!
import ipcg.binder.native.NativeUtils as Lang
import ipcg.Utils as Utils
%>

<%
headerGuard = struct.name.upper() + '_H'
%>

#ifndef ${headerGuard}
#define ${headerGuard}

// Dependency includes
% for i in struct.dependencies:
// ${i.name}
#include "${Lang.getIncludePath(i)}"
% endfor
#include <binder/Parcel.h>
#include <utils/Vector.h>

${Lang.namespaceStart(struct.path[:-1])}
                 
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
    ${Lang.getTypeName(field)} ${Lang.formatGetter(field)}() const;
% endfor
    
    // Field setters
% for field in struct.fields:
    ${struct.name}* ${Lang.formatSetter(field)}(const ${Lang.getTypeName(field)}& value);
% endfor

    bool operator==(const ${Lang.getTypeClass(struct)}& other) const;
    
    bool operator!=(const ${Lang.getTypeClass(struct)}& other) const;

private:
    // Member fields
% for field in struct.fields:
    ${Lang.getTypeName(field)} ${field.name};
% endfor
    
private:
    friend class android::LightRefBase<${struct.name}>;
    
}; // ${struct.name}
                 
${Lang.namespaceEnd(struct.path[:-1])}


#endif // ${headerGuard}
 