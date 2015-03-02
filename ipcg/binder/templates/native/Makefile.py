LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

## Source files compiled by this makefile
LOCAL_SRC_FILES += \
% for file in sourceFiles:
    ${file} \
% endfor 

LOCAL_C_INCLUDES += $(LOCAL_PATH)/include

LOCAL_SHARED_LIBRARIES := \
        libcutils \
        libutils \
        libbinder

## Librfary name
LOCAL_MODULE:= ${localModule}

LOCAL_MODULE_TAGS := optional

LOCAL_PRELINK_MODULE := false


% if isStatic:

include $(BUILD_STATIC_LIBRARY)

%else:

include $(BUILD_SHARED_LIBRARY)

% endif
