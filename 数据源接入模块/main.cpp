#include "行情数据适配层.H"
#include <iostream>
#include <thread>
#include <vector>
#include <sw/redis++/redis++.h> // 确保安装了 redis++

// vcpkg 集成注意：
// 需要在 CMakeLists.txt 中 find_package(redis++ CONFIG REQUIRED)

using namespace sw::redis;

int main()
{
    try
    {
        // 1. 连接 Redis
        std::cout << "[MD-Engine] Connecting to Redis..." << std::endl;
        auto redis = Redis("tcp://127.0.0.1:6379");

        std::cout << "[MD-Engine] Starting Market Data Feed..." << std::endl;

        // 2. 模拟行情循环
        while (true)
        {
            // 模拟从 HTTP/Websocket 获取的原始数据
            std::string raw_msg = "{\"event\":\"trade\",\"symbol\":\"BTC-USDT\"...}";

            // 归一化处理
            auto tick = MarketFeed::DataAdaptor::normalize(raw_msg, "BINANCE");

            // 序列化
            std::string json_payload = MarketFeed::DataAdaptor::to_json(tick);

            // 发布到 Redis Channel (Pub/Sub 模式)
            // Python 端监听 'market_tick_channel'
            redis.publish("market_tick_channel", json_payload);

            // 同时推送到监控 Channel (可选)
            // redis.publish("system_monitor_channel", "{\"latency\": 12.5, \"service\": \"cpp_md\"}");

            // 控制频率：模拟 10ms 推送一次 (100 TPS)
            std::this_thread::sleep_for(std::chrono::milliseconds(10));
        }
    }
    catch (const Error &e)
    {
        std::cerr << "[Error] Redis error: " << e.what() << std::endl;
    }
    catch (const std::exception &e)
    {
        std::cerr << "[Error] System error: " << e.what() << std::endl;
    }

    return 0;
}