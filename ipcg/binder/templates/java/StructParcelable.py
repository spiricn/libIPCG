package ${'.'.join(struct.module.package.path)};

<%namespace name="Lang" module="ipcg.LangJava"/>

<%

from idl.Type import Type

%>

import android.os.Parcel;
import android.os.Parcelable;

public class ${struct.name} implements Parcelable {
%if struct.fields:
    public ${struct.name} (${Lang.getJavaMethodArgList(struct.fields)}) {
    % for arg in struct.fields:
        this.${arg.name} = ${arg.name};
    %endfor
    }
% endif
    
    public ${struct.name} () {
    % for arg in struct.fields:
        this.${arg.name} = ${Lang.getInvalidJavaValue(arg.type)};
    %endfor
    }
    
    @Override
    public int describeContents() {
        return 0;
    }
    
    // Field setters
    % for field in struct.fields:
    public ${struct.name} ${Lang.formatSetter(field)} (${Lang.getJavaType(field.type)} ${field.name}) {
        this.${field.name} = ${field.name};
        
        return this;
    }
    %endfor

    // Field getters
    % for field in struct.fields:
    public ${Lang.getJavaType(field.type)} ${Lang.formatGetter(field)} () {
        return this.${field.name};
    }
    %endfor    
    
    @Override
    public void writeToParcel(Parcel dest, int flags) {
        % for field in struct.fields:
        
            % if field.type.isPrimitive:
                % if field.type.id == Type.BOOL:
        dest.writeInt(this.${field.name} ? 1 : 0);
                % elif field.type.id == Type.INT32:
        dest.writeInt(this.${field.name});
                % elif field.type.id == Type.INT64:
        dest.writeLong(this.${field.name});
                % elif field.type.id == Type.STRING:
        dest.writeString(this.${field.name});
                % elif field.type.id == Type.FLOAT64:
        dest.writeDouble(this.${field.name});
                % elif field.type.id == Type.FLOAT32:
        dest.writeFloat(this.${field.name});
                % else:
                Unsupported primitive ${field.type.name} for field ${field.name}
                % endif
            % elif field.type in [Type.STRUCTURE, Type.ENUM]:
        ${field.name}.writeToParcel(dest, flags);
            % else:
                Unsupported type ${field.type.name} for field ${field.name}
            % endif
        %endfor
    }
    
    public ${struct.name} readFromParcel(Parcel in) {
        % for field in struct.fields:
        
            % if field.type.isPrimitive:
                % if field.type.id == Type.BOOL:
        this.${field.name} = in.readByte() == 0 ? false : true;
                % elif field.type.id == Type.INT32:
        this.${field.name} = in.readInt();
                % elif field.type.id == Type.INT64:
        this.${field.name} = in.readLong();
                % elif field.type.id == Type.STRING:
        this.${field.name} = in.readString();
                % elif field.type.id == Type.FLOAT64:
        this.${field.name} = in.readDouble();
                % elif field.type.id == Type.FLOAT32:
        this.${field.name} = in.readFloat();
                % else:
                Unsupported primitive '$field.type.name' for field $field.name
                % endif
            % elif field.type in [Type.STRUCTURE, Type.ENUM]:
        this.${field.name} = ${field.type.name}.CREATOR.createFromParcel(in);
            % else:
                Unsupported type '$field.type.name' for field $field.name
            % endif
        %endfor
        
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
        String res = "{ ${struct.name}: [";
        
    % for field in struct.fields:
        
        res += "${field.name}=" + this.${field.name} + ",";
        
    % endfor
        
        return res + "] }";
    }

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
    
% for field in struct.fields:
    private ${Lang.getJavaType(field.type)} ${field.name}; 
%endfor

} //  ${struct.name}
