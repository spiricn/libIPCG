package ${'.'.join(iface.module.package.path)};

<%namespace name="Lang" module="ipcg.LangJava"/>

<%

from idl.Type import Type

%>

% for i in iface.dependencies:
import ${'.'.join(i.module.package.path) + '.' + i.name};
% endfor
interface ${iface.name} {

% for method in iface.methods:
    ${Lang.getJavaType(method.ret.type)} ${method.name} ( ${Lang.getAIDLMethodArgList(method.args)} );

% endfor                         
} // ${iface.name}

