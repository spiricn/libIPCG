<%!
import ipcg.generator.binder.native.NativeUtils as NativeUtils
from idl.Type import Type
%>

<%
className = 'Bn' + iface.name[1:]

headerGuard = 'BN_' + NativeUtils.getHeaderGuard(iface)
%>

#ifndef ${headerGuard}
#define ${headerGuard}

#include "${NativeUtils.getIncludePath(iface)}"

${NativeUtils.namespaceStart(iface.path[:-1])}

class ${className}: public android::BnInterface<${iface.name}>
{
public:
    ${className}();

    virtual ~${className}();
    
    virtual android::status_t onTransact(uint32_t code, const android::Parcel& data, android::Parcel* reply, uint32_t flags=0);
    
}; // class ${className}

${NativeUtils.namespaceEnd(iface.path[:-1])}

#endif // ${headerGuard}
