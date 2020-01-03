## 命令行方式   
```
g++ -std=c++11 -lopencv_core -lopencv_dnn -lopencv_highgui -lopencv_imgcodecs -lopencv_imgproc -lopencv_objdetect -lopencv_video -lopencv_videoio src1.cpp src2.cpp src3.cpp src4.cpp -o output-excutable 
```

## CMakeLists   
```
cmake_minimum_required(VERSION 3.0)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)
SET(CMAKE_CXX_COMPLIER "/usr/bin/g++")
project (dimples)
set (OpenCV_DIR "/usr/local/Cellar/opencv/4.1.0_2/include/opencv4")
find_package(OpenCV REQUIRED)
include_directories( ${OpenCV_INCLUDE_DIRS})
add_executable(dimples dimples.cpp WienerFilter.cpp)
target_link_libraries(dimples ${OpenCV_LIBS})
```
