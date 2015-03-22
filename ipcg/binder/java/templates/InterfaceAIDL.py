<%!
import ipcg.lang.AIDL as Lang
from idl.Type import Type
%>

## Package declaration
package ${'.'.join(iface.module.package.path)};

## Import dependencies
% for i in iface.dependencies:
import ${'.'.join(i.module.package.path) + '.' + i.name};
% endfor

## Interface declaration
interface ${iface.name} {

% for method in iface.methods:
    ## Method declaration
    ${Lang.getTypeName(method.ret)} ${method.name} ( ${Lang.getMethodArgList(method.args)} );

% endfor                         
} // ${iface.name}
