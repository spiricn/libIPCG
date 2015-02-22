package com.example.test;

<%namespace name="Lang" module="ipcg.LangJava"/>

<%

from idl.Type import Type

%>

% for i in iface.dependencies:
import ${'.'.join(i.path)};
% endfor
interface ${iface.name} {

% for method in iface.methods:
    ${Lang.getJavaType(method.ret.type)} ${method.name} ( ${Lang.getAIDLMethodArgList(method.args)} );

% endfor                         
} // ${iface.name}

