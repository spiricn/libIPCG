<%!
import ipcg.binder.LangCPP as Lang
from idl.Type import Type
%>

<%
className = 'Bp' + iface.name[1:]
%>

#include <binder/IInterface.h>
#include <binder/Parcel.h>

#define LOG_TAG "${':'.join(iface.module.package.path) + ':' + className}"

// Dependency includes
% for i in iface.dependencies:
#include "${Lang.getIncludePath(i)}"
% endfor

#ifdef LOG_TAG
#undef LOG_TAG
#endif

using namespace android;

${Lang.namespaceStart(iface.path[:-1])}

class ${className} : public BpInterface<${iface.name}> {
public:

    ${className}(const sp<IBinder>& impl) : BpInterface<${iface.name}>(impl) {
    }
                                                       
    virtual ~${className}(){
    }
    
public:
    // Methods
    
    % for method in iface.methods:
    
    ${Lang.getMethodSig(method)}{
        Parcel data;
        Parcel reply;
        
        data.writeInterfaceToken( ${iface.name}::getInterfaceDescriptor() );
        
    % for arg in method.args:
        ${Lang.getWriteExpr(arg.name, arg, '(&data)')};
    % endfor
        
        remote()->transact(${Lang.getMethodId(method)}, data, &reply);
        
        if(reply.readExceptionCode() != 0) {
            // Fail on exception
            return
    % if method.ret.type != Type.VOID: 
        ${Lang.getDefaultValue(method.ret.type)}
    % endif
        ;
        }
        
    % if method.ret.type != Type.VOID:
        ${Lang.getTypeName(method.ret)} __returnValue = ${Lang.getDefaultValue(method.ret)};
        
        ${Lang.getReadExpr('__returnValue', method.ret, 'reply')};
                           
        return __returnValue;
    % endif
    }

    % endfor

}; // class ${className}

IMPLEMENT_META_INTERFACE(${iface.name[1:]}, "${'.'.join(iface.path)}");

${Lang.namespaceEnd(iface.path[:-1])}
