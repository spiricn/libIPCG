<%!
import ipcg.binder.LangCPP as Lang
from idl.Type import Type
%>

<%
className = 'Bn' + iface.name[1:]

headerGuard = className.upper() + '_H'

methodResult = '__methodResult'
%>

#include <binder/IInterface.h>
#include <binder/Parcel.h>

#include "${Lang.getIncludePath(iface, className)}"

#undef LOG_TAG
#endif

#define LOG_TAG "${namespace}_${className}"

## Start namespace
using namespace android;

${Lang.namespaceStart(iface.path[:-1])}

status_t ${className}::onTransact(uint32_t code, const android::Parcel& data, android::Parcel* reply, uint32_t flags){
    switch(code){
    % for method in iface.methods:
        case ${Lang.getMethodId(method)}:{
            ALOGD("[call begin][${method.name}]");
            
            CHECK_INTERFACE(I${iface.name}, data, reply);
            
            // Declare method arguments
        % for arg in method.args:
            ${Lang.getTypeName(arg.type)} ${arg.name} = ${Lang.getDefaultValue(arg.type)};
        % endfor
            
            // Declare return type
            
            % if method.ret.type != Type.VOID:
            ${Lang.getTypeName(method.ret.type)} ${methodResult} = ${Lang.getDefaultValue(method.ret.type)};
            % endif
            
            // Deserialize arguments
            
        % for arg in method.args:
            ${Lang.getReadExpr(arg.name, arg.type, 'data')};
        % endfor
        
            % if method.ret.type != Type.VOID:
            
            ${methodResult} = 
            
            % endif
            
            // Call method
            
            ${method.name}(
                
            % for index, arg in enumerate(method.args):
                ${arg.name}
                
                % if index < len(method.args)-1:
                ,
                % endif
            % endfor
            
            );
            
            // Write result
            reply->writeNoException();
            
            % if method.ret.type != Type.VOID:
            ${Lang.getWriteExpr(methodResult, method.ret.type, 'reply')};
            % endif
            
            ALOGD("[call end][${method.name}]");
            
            return NO_ERROR;
        }
    % endfor
        
        default:{
            return BBinder::onTransact(code, data, reply, flags);
        }
                 
    }; // switch(code)
}

${className}::${className}(){
}

${className}::~${className}(){
}

${Lang.namespaceEnd(iface.path[:-1])}

