<%!
import ipcg.binder.native.NativeUtils as Lang
from idl.Type import Type
%>

<%
className = 'Bn' + iface.name[1:]

headerGuard = 'BN_' + Lang.getHeaderGuard(iface)
%>

#ifndef ${headerGuard}
#define ${headerGuard}

#include "${Lang.getIncludePath(iface)}"

${Lang.namespaceStart(iface.path[:-1])}

class ${className}: public android::BnInterface<${iface.name}>
{
public:
    ${className}();

    virtual ~${className}();
    
    virtual android::status_t onTransact(uint32_t code, const android::Parcel& data, android::Parcel* reply, uint32_t flags=0);
    
}; // class ${className}

${Lang.namespaceEnd(iface.path[:-1])}

#endif // ${headerGuard}
