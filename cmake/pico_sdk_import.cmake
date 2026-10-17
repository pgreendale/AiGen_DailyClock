if(NOT PICO_SDK_PATH AND DEFINED ENV{PICO_SDK_PATH})
    set(PICO_SDK_PATH "$ENV{PICO_SDK_PATH}")
endif()
if(NOT EXISTS "${PICO_SDK_PATH}/external/pico_sdk_import.cmake")
    message(FATAL_ERROR "Pico SDK not found. Import this folder in the Pico extension, set PICO_SDK_PATH, or run tools/build.ps1.")
endif()
include("${PICO_SDK_PATH}/external/pico_sdk_import.cmake")

