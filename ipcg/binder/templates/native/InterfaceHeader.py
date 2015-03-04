<%!
import ipcg.binder.NativeUtils as Lang
from idl.Type import Type
%>

<%
headerGuard = iface.name.upper() + '_H'
%>

#ifndef ${headerGuard}
#define ${headerGuard}

#include <binder/IInterface.h>
#include <binder/Parcel.h>

// Dependency includes
% for i in iface.dependencies:
#include "${Lang.getIncludePath(i)}"
% endfor

${Lang.namespaceStart(iface.path[:-1])}

class ${iface.name} : public android::IInterface
{
public:
    DECLARE_META_INTERFACE( ${iface.name[1:]} );
    
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
}; // class ${iface.name}

${Lang.namespaceEnd(iface.path[:-1])}
    
#endif // ifndef ${headerGuard}
