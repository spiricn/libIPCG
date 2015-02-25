<%namespace name="Lang" module="ipcg.LangCPP"/>

<%
from idl.Type import Type

className = 'Bn' + iface.name

interfaceClassName = 'I' + iface.name

headerGuard = className.upper() + '_H'
%>

#include "${Lang.getIncludePath(iface)}"

namespace ${namespace} {

class ${className}: public android::BnInterface<${interfaceClassName}>
{
public:
    ${className}();

    virtual ~${className}();
    
    virtual android::status_t onTransact(uint32_t code, const android::Parcel& data, android::Parcel* reply, uint32_t flags=0);
    
}; // class ${className}

}; // namespace ${namespace}
