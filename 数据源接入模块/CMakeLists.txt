cmake_minimum_required(VERSION 3.20)
project(AStockFastDataFeed LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(nlohmann_json CONFIG REQUIRED)
find_package(redis++ CONFIG REQUIRED)
find_package(Boost REQUIRED) # boost-lockfree 属于 Boost 体系

add_executable(market_feed_demo
    main.cpp
    HTTP行情接口.cpp
    实时推送接口_券商TCP.cpp
    行情数据适配层.cpp
)

# 最终输出 exe 名可中文（内部 target 名必须英文）
set_target_properties(market_feed_demo PROPERTIES OUTPUT_NAME "行情接入_demo")

target_include_directories(market_feed_demo PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_link_libraries(market_feed_demo PRIVATE
    nlohmann_json::nlohmann_json
    redis++::redis++
    Boost::boost
)
