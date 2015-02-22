LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_CFLAGS += -DANDROID_BUILD=1

ifeq "$(KITKAT)" "YES"
LOCAL_CFLAGS += -DKITKAT
endif

ifeq "$(LOLLIPOP)" "YES"
LOCAL_CFLAGS += -DLOLLIPOP
endif

LOCAL_SRC_FILES += \
% for file in sourceFiles:
    ${file} \
% endfor 

LOCAL_C_INCLUDES += $(LOCAL_PATH)/include

LOCAL_SHARED_LIBRARIES := \
        libcutils \
        libutils \
        libbinder

LOCAL_MODULE:= ${localModule}

LOCAL_MODULE_TAGS := optional

LOCAL_PRELINK_MODULE := false

include $(BUILD_STATIC_LIBRARY)
