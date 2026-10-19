cmake_minimum_required(VERSION 3.16)

# Use the windres that belongs to the compiler we are building with. Without
# this, PATH decides, and with MSYS2 on the PATH its windres gets picked up:
# it fails with "preprocessing failed" on the resource file of a MinGW 13.1
# build. Must happen before project(), which is where CMake locks it in.
if(CMAKE_CXX_COMPILER)
    get_filename_component(_compiler_dir "${CMAKE_CXX_COMPILER}" DIRECTORY)
    if(EXISTS "${_compiler_dir}/windres.exe")
        set(CMAKE_RC_COMPILER "${_compiler_dir}/windres.exe" CACHE FILEPATH "Resource compiler" FORCE)
    endif()
endif()

project(ver_2 VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD_REQUIRED ON)
# The project builds against the Qt that comes with MSYS2 (ucrt64). The
# official Qt 6.9.3 variant - no ICU, smaller deployment - lives in the
# backup folder; the two installations must not be mixed.
set(CMAKE_PREFIX_PATH "C:/msys64/ucrt64")

# Default to a debug build: this folder is the development setup. The release
# build (official Qt, stripped, about 22 MB packaged) is made from the backup
# folder. A build type given on the command line or by the IDE still wins.
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build type" FORCE)
endif()

# Keep the release binary small: drop unused sections and strip the symbol
# table at link time. Remove the -s if you ever need crash backtraces or want
# to debug this binary with gdb.
if(CMAKE_BUILD_TYPE STREQUAL "Release" OR CMAKE_BUILD_TYPE STREQUAL "MinSizeRel")
    add_compile_options(-ffunction-sections -fdata-sections)
    add_link_options(-Wl,--gc-sections -s)
endif()

find_package(Qt6 REQUIRED COMPONENTS Quick Gui)

qt_standard_project_setup()

qt_add_executable(ver_2
    main.cpp
    graphs/icon/0-icon.rc
)

set_property(TARGET ver_2 PROPERTY WIN32_EXECUTABLE TRUE)

qt_add_qml_module(ver_2
    URI MyWindow
    VERSION 1.0
    QML_FILES
        MainWindow.qml
        MyWindow/DragWindow.qml
    RESOURCES
        graphs/dynamic_graphs/1-zhuzhunian-fighting.gif
        graphs/dynamic_graphs/3-ri'chang-bye.gif
        graphs/cursor/2-mouse_ico_fixed.cur
        graphs/icon/0-icon.ico
)

set_target_properties(ver_2 PROPERTIES
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    MACOSX_BUNDLE TRUE
)

target_link_libraries(ver_2
    PRIVATE Qt6::Gui Qt6::Quick
)

include(GNUInstallDirs)
install(TARGETS ver_2
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
