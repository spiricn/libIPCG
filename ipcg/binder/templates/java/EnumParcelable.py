package ${'.'.join(enum.module.package.path)};


<%namespace name="LangJava" module="ipcg.LangJava"/>

<%

from idl.Type import Type

%>


import android.os.Parcel;
import android.os.Parcelable;

public enum ${enum.name} implements Parcelable {
                        
% for index, field in enumerate(enum.fields):
    ${field.name}(${field.value})
    % if index < len(enum.fields) - 1:
    ,
    % endif
% endfor
    ;

    ${enum.name}(int value){
        mValue = value;
    } 
                        
    public int getValue(){
        return mValue;
    }
    
    @Override
    public int describeContents() {
        return 0;
    }
    
    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeInt(ordinal());
    }
    
    public ${enum.name} readFromParcel(Parcel in) {
        return values()[in.readInt()];
    }
     
    public static final Parcelable.Creator<${enum.name}> CREATOR = new Parcelable.Creator<${enum.name}>() {
        public ${enum.name} createFromParcel(Parcel in) {
            return ${enum.name}.values()[in.readInt()];
        }

        public ${enum.name}[] newArray(int size) {
            return new ${enum.name} [size];
        }
    };
                        
    private int mValue;
} // ${enum.name}
