#include "HTTP行情接口.h"
#include "实时推送接口_券商TCP.h"
#include "行情数据适配层.h"

#include <iostream>
#include <atomic>
#include <thread>
#include <chrono>

int main()
{
    std::atomic<bool> running{true};

    // HTTP 模拟（后续接入通达信/券商API）
    HTTP行情接口 http;
    http.set_on_tick([](const MarketTick &t)
                     {
        // 这里只打印，后续改为推送到策略/Java落库/Redis等
        std::cout << "[HTTP] " << t.code << " last=" << t.last << " ts=" << t.ts_ms << "\n"; });

    // TCP推送模拟（后续接入券商主动推送）
    实时推送接口_券商TCP tcp;
    tcp.set_on_tick([](const MarketTick &t)
                    { std::cout << "[TCP] " << t.code << " last=" << t.last << " ts=" << t.ts_ms << "\n"; });

    http.start();
    tcp.start();

    std::this_thread::sleep_for(std::chrono::seconds(3));

    http.stop();
    tcp.stop();

    std::cout << "OK\n";
    return 0;
}
