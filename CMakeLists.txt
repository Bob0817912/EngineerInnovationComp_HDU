CMAKE_MINIMUM_REQUIRED(VERSION 3.15)

project(gx)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CXX_STANDARD 20)

add_compile_definitions(INFO_LEVEL=3 BOOST_BIND_GLOBAL_PLACEHOLDERS NO_SERIAL)
add_compile_options(-g)

set(OPENCV_DIR ${CMAKE_SOURCE_DIR}/3rd-party/opencv)

find_package(OpenCV REQUIRED
PATHS ${OPENCV_DIR}
NO_DEFAULT_PATH
)

include_directories(
    include
    ${OpenCV_INCLUDE_DIRS}
)
link_directories(
    ${OPENCV_DIR}/lib
)

add_library(Info SHARED
    src/Info.cpp
)

add_library(Camera SHARED
    src/Camera.cpp
    src/Info.cpp
)

add_library(Detector SHARED
    src/Detector.cpp
    src/Info.cpp
)

add_library(Serial SHARED
    src/Serial.cpp
)

add_library(Application SHARED
    src/Application.cpp
    src/Info.cpp
    src/Camera.cpp
    src/Detector.cpp
    src/Serial.cpp
)

add_executable(main 
    src/main.cpp
)

target_link_libraries(Camera 
    ${OpenCV_LIBS}
    Info
)

target_link_libraries(Detector
    ${OpenCV_LIBS}
    Info
)

target_link_libraries(Application
    Camera
    Detector
    Serial
    Info
)

target_link_libraries(main
    -lpthread
    Application
)
