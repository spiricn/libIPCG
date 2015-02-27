<%!
import ipcg.LangCPP as Lang
import ipcg.Utils as Utils
%>


<%
from idl.Type import Type
import ipcg.Utils
import ipcg.LangCPP as LangCPP

# Each enum field gets a prefix (consider using c++11 enum class instead ?)
enumPrefix = Utils.nameToDefine(enum.name)

# File header guard
headerGuard = LangCPP.getHeaderGuard(enum)
%>


#ifndef ${headerGuard}
#define ${headerGuard}

${Lang.namespaceStart(enum.path[:-1])}

enum ${enum.name} {
                   
% for field in enum.fields:
   ${enumPrefix}_${field.name} = ${field.value} ,
% endfor

}; // enum ${enum.name}
                        
${Lang.namespaceEnd(enum.path[:-1])}

#endif // ifndef ${headerGuard}
