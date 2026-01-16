cmake_minimum_required(VERSION 3.14)
project(SpeedTrader_MarketEngine)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -Wall -pthread")

# 寻找 Boost 库 (System, Thread, Json)
# 注意：Boost.Beast 和 Boost.HeaderOnly 不需要编译成 .lib，直接 include 即可
find_package(Boost REQUIRED COMPONENTS system thread json)

include_directories(.)

# 源文件列表
set(SOURCES 
    main.cpp 
    实时推送接口_券商TCP.cpp 
    HTTP行情接口.cpp
    行情数据适配层.cpp
)

add_executable(MarketEngine ${SOURCES})

# 链接库
target_link_libraries(MarketEngine 
    Boost::system 
    Boost::thread 
    Boost::json
)

if(WIN32)
    target_link_libraries(MarketEngine ws2_32 mswsock)
endif()