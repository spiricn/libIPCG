<%!
import ipcg.lang.Java as Lang
from idl.Type import Type
%>

## Package declaration
package ${'.'.join(enum.module.package.path)};

## Generic imports
import android.os.Parcel;
import android.os.Parcelable;

## Class definition
public enum ${enum.name} implements Parcelable {
                        
## Enum fields
% for index, field in enumerate(enum.fields):
    ${field.name}(${field.value})
    % if index < len(enum.fields) - 1:
    ,
    % endif
% endfor
    ;

    ## Value constructor
    ${enum.name}(int value){
        mValue = value;
    } 
                        
    ## Value getter
    public int getValue(){
        return mValue;
    }
    
    public static ${enum.name} getFromValue(int value){
        for( ${enum.name} i : values()){
            if(i.getValue() == value){
                return i;
            }
        }
        
        return null;
    }
    
    @Override
    public int describeContents() {
        return 0;
    }
    
    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeInt(getValue());
    }
    
    public ${enum.name} readFromParcel(Parcel in) {
        return ${enum.name}.getFromValue(in.readInt());
    }
     
    public static final Parcelable.Creator<${enum.name}> CREATOR = new Parcelable.Creator<${enum.name}>() {
        public ${enum.name} createFromParcel(Parcel in) {
            return ${enum.name}.getFromValue(in.readInt());
        }

        public ${enum.name}[] newArray(int size) {
            return new ${enum.name} [size];
        }
    };

    private int mValue;

} // ${enum.name}
