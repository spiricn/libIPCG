<%namespace name="Lang" module="ipcg.LangCPP"/>

<%namespace name="Utils" module="ipcg.Utils"/>

<%
from idl.Type import Type
import ipcg.Utils

enumPrefix = Utils.nameToDefine(enum.name)

headerGuard = enum.name.upper() + '_H'

%>

#ifndef ${headerGuard}
#define ${headerGuard}

namespace ${namespace} {

enum ${enum.name} {
                   
% for field in enum.fields:
   ${enumPrefix}_${field.name} = ${field.value} ,
% endfor

}; // enum ${enum.name}
                        
}; // namespace ${namespace}

#endif // ifndef ${headerGuard}
