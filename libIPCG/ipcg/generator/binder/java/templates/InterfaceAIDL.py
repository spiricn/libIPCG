<%!
import ipcg.generator.binder.java.AIDLUtils as AIDLUtils
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
    ${AIDLUtils.getTypeName(method.ret)} ${method.name} (${AIDLUtils.getMethodArgList(method.args)});

% endfor                         
} // ${iface.name}
