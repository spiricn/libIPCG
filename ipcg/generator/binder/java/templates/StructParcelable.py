<%!
from idl.Type import Type
import ipcg.generator.binder.java.JavaUtils as JavaUtils
import ipcg.generator.binder.java.Format as Format
import ipcg.generator.binder.java.JavaParcelSerialization as JavaParcelSerialization
import ipcg.generator.binder.java.JavaParcelDeserialization as JavaParcelDeserialization
%>

## Package declaration
package ${'.'.join(struct.module.package.path)};

## Generic imports
import android.os.Parcel;
import android.os.Parcelable;
import java.util.ArrayList;
import java.util.List;

## Class definition
public class ${struct.name} implements Parcelable {
                                                   
    ## Argument constructor
%if struct.fields:
    public ${struct.name} (${JavaUtils.getMethodArgList(struct.fields)}) {
    % for arg in struct.fields:
        this.${arg.name} = ${arg.name};
    %endfor
    }
% endif
    
    ## Default constructor
    public ${struct.name} () {
    % for arg in struct.fields:
        this.${arg.name} = ${JavaUtils.getDefaultValue(arg)};
    %endfor
    }
    
    @Override
    public int describeContents() {
        return 0;
    }
    
    ## Field setters
% for field in struct.fields:
    public ${struct.name} ${Format.getFieldSetterName(field)} (${JavaUtils.getTypeName(field)} ${field.name}) {
        this.${field.name} = ${field.name};
        
        return this;
    }
    %endfor

    ## Field getters
% for field in struct.fields:
    public ${JavaUtils.getTypeName(field)} ${Format.getFieldGetterName(field)} () {
        return this.${field.name};
    }
%endfor    
    
    ## Serialization
    @Override
    public void writeToParcel(Parcel dest, int flags) {
    % for field in struct.fields:
        ${JavaParcelSerialization.getWriteExpr('this.' + field.name, field, 'dest')};
    % endfor
    }
    
    ## Deserialization
    public ${struct.name} readFromParcel(Parcel in) {
    % for field in struct.fields:
        ${JavaParcelDeserialization.getReadExpr('this.' + field.name, field, 'in')};
    % endfor
    
        return this;
    }
    
    public static final Parcelable.Creator<${struct.name}> CREATOR = new Parcelable.Creator<${struct.name}>() {
        public ${struct.name} createFromParcel(Parcel in) {
            return new ${struct.name}().readFromParcel(in);
        }

        public ${struct.name}[] newArray(int size) {
            return new ${struct.name} [size];
        }
    };
    
    @Override
    public String toString(){
        String res = "{ ${struct.name}(" + this.hashCode() + "): [";
        
    % for field in struct.fields:
        
        res += "${field.name}=" + this.${field.name} + ",";
        
    % endfor
        
        return res + "] }";
    }

    ## Equals operator
    @Override
    public boolean equals(Object object){
        if(!(object instanceof ${struct.name})){
            return false;
        }
        
        ${struct.name} other = (${struct.name})object;
        
% for field in struct.fields:
    % if field.type in [Type.STRING, Type.STRUCTURE]:
    
        if(!this.${field.name}.equals(other.${field.name})){
            return false;
        }
        
    % elif field.type.isPrimitive or field.type == Type.ENUM:
    
        if(this.${field.name} != other.${field.name}){
            return false;
        }
        
    % else:
    
            Comparison not implemented for type ${field.type.name}
            
    % endif
% endfor
        
        return true;
    }
    
    ## Member fields declaration
% for field in struct.fields:
    private ${JavaUtils.getTypeName(field)} ${field.name}; 
%endfor

} //  ${struct.name}
