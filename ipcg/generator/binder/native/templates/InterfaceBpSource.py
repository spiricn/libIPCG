<%!
import ipcg.generator.binder.native.NativeUtils as NativeUtils
from idl.Type import Type
import ipcg.generator.binder.native.NativeParcelSerialization as NativeParcelSerialization
import ipcg.generator.binder.native.NativeParcelDeserialization as NativeParcelDeserialization

%>

<%
className = 'Bp' + iface.name[1:]
%>

#include <binder/IInterface.h>
#include <binder/Parcel.h>

#include "${NativeUtils.getIncludePath(iface)}"

#ifdef LOG_TAG
#undef LOG_TAG
#endif

#define LOG_TAG "${':'.join(iface.module.package.path) + ':' + className}"

// Dependency includes
% for i in iface.dependencies:
#include "${NativeUtils.getIncludePath(i)}"
% endfor

using namespace android;

${NativeUtils.namespaceStart(iface.path[:-1])}

class ${className} : public BpInterface<${iface.name}> {
public:

    ${className}(const sp<IBinder>& impl) : BpInterface<${iface.name}>(impl) {
    }
                                                       
    virtual ~${className}(){
    }
    
public:
    // Methods
    
    % for method in iface.methods:
    
    ${NativeUtils.getMethodSig(method)}{
        Parcel data;
        Parcel reply;
        
        data.writeInterfaceToken( ${iface.name}::getInterfaceDescriptor() );
        
    % for arg in method.args:
        ${NativeParcelSerialization.getWriteExpr(arg.name, arg, '(&data)')};
    % endfor
        
        remote()->transact(${NativeUtils.getMethodId(method)}, data, &reply);
        
        if(reply.readExceptionCode() != 0) {
            // Fail on exception
            return
    % if method.ret.type != Type.VOID: 
        ${NativeUtils.getDefaultValue(method.ret.type)}
    % endif
        ;
        }
        
    % if method.ret.type != Type.VOID:
        ${NativeUtils.getTypeName(method.ret)} __returnValue = ${NativeUtils.getDefaultValue(method.ret)};
        
        ${NativeParcelDeserialization.getReadExpr('__returnValue', method.ret, 'reply')};
                           
        return __returnValue;
    % endif
    }

    % endfor

}; // class ${className}

IMPLEMENT_META_INTERFACE(${iface.name[1:]}, "${'.'.join(iface.path)}");

${NativeUtils.namespaceEnd(iface.path[:-1])}
