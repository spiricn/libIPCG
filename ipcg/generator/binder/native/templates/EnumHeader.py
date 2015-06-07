<%!
import ipcg.generator.binder.native.NativeUtils as NativeUtils
from idl.Type import Type
%>

<%
# Each enum field gets a prefix (consider using c++11 enum class instead ?)
enumPrefix = NativeUtils.nameToDefine(enum.name)

# File header guard
headerGuard = NativeUtils.getHeaderGuard(enum)
%>

#ifndef ${headerGuard}
#define ${headerGuard}

${NativeUtils.namespaceStart(enum.path[:-1])}

enum ${enum.name} {
                   
   ## Enum fields 
% for field in enum.fields:
   ${enumPrefix}_${field.name} = ${field.value} ,
% endfor

}; // enum ${enum.name}
                        
${NativeUtils.namespaceEnd(enum.path[:-1])}

#endif // ifndef ${headerGuard}
