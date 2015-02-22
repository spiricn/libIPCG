<%namespace name="Lang" module="ipcg.LangCPP"/>

<%
from idl.Type import Type

className = 'Bp' + iface.name

%>

#include <binder/IInterface.h>
#include <binder/Parcel.h>

#include "${Lang.getIncludePath(iface)}"

// Dependency includes
% for i in iface.dependencies:
#include "${Lang.getIncludePath(i)}"
% endfor

#ifdef LOG_TAG
#undef LOG_TAG
#endif

#define LOG_TAG "${namespace}_${className}"

using namespace android;

namespace ${namespace} {

class ${className} : public BpInterface<I${iface.name}> {
public:

    ${className}(const sp<IBinder>& impl) : BpInterface<I${iface.name}>(impl) {
    }
                                                       
    virtual ~${className}(){
    }
    
public:
    // Methods
    
    % for method in iface.methods:
    
    ${Lang.getMethodSig(method)}{
        Parcel data;
        Parcel reply;
        
        data.writeInterfaceToken( I${iface.name}::getInterfaceDescriptor() );
        
        % for arg in method.args:
        ${Lang.getWriteExpr(arg.name, arg.type, '(&data)')};
        % endfor
        
        remote()->transact(${Lang.getMethodId(method)}, data, &reply);
        
        if(reply.readExceptionCode() != 0) {
            // Fail on exception
            return
        % if method.ret.type != Type.VOID: 
        ${Lang.getInvalidValue(method.ret.type)}
        % endif
        ;
        }
        
        % if method.ret.type != Type.VOID:
        ${Lang.getTypeName(method.ret.type)} __returnValue = ${Lang.getInvalidValue(method.ret.type)};
        
        ${Lang.getReadExpr('__returnValue', method.ret.type, 'reply')};
                           
        return __returnValue;
        % endif
    }

    % endfor

}; // class ${className}

IMPLEMENT_META_INTERFACE(${iface.name}, "${'.'.join(iface.path)}");

}; // ${namespace}
