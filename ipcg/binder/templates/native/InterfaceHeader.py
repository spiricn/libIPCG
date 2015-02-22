<%namespace name="Lang" module="ipcg.LangCPP"/>

<%
from idl.Type import Type

className = 'I' + iface.name

headerGuard = className.upper() + '_H'
%>

#ifndef ${headerGuard}
#define ${headerGuard}

#include <binder/IInterface.h>
#include <binder/Parcel.h>

// Dependency includes
% for i in iface.dependencies:
#include "${Lang.getIncludePath(i)}"
% endfor

namespace ${namespace} {

class ${className} : public android::IInterface
{
public:
    DECLARE_META_INTERFACE( ${iface.name} );
    
public:
    // Methods
% for method in iface.methods:
    virtual ${Lang.getMethodSig(method)} = 0;
% endfor    
    
public:
    enum MethodID {         
% for index, method in enumerate(iface.methods):
        ${Lang.getMethodId(method)}
        
        % if index == 0:
        = android::IBinder::FIRST_CALL_TRANSACTION
        % endif
        ,
% endfor

        LAST_ID
    };
}; // class ${className}

}; // namespace ${namespace} 
    
#endif // ifndef ${headerGuard}
