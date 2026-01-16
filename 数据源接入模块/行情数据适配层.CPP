#include "行情数据适配层.H"
#include <chrono>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <cstring> // for strncpy

// 假设项目使用 redis++ (sw::redis)，这里暂时模拟数据生成逻辑
// 实际项目中你需要 #include <nlohmann/json.hpp>

namespace MarketFeed
{

    // 辅助函数：获取当前毫秒时间戳
    int64_t DataAdaptor::current_timestamp_ms()
    {
        auto now = std::chrono::system_clock::now();
        auto duration = now.time_since_epoch();
        return std::chrono::duration_cast<std::chrono::milliseconds>(duration).count();
    }

    MarketTick DataAdaptor::normalize(const std::string &raw_data, const std::string &source_exchange)
    {
        MarketTick tick;

        // 1. 基础元数据填充
        // 使用 strncpy 安全复制字符串，防止缓冲区溢出
        std::strncpy(tick.exchange, source_exchange.c_str(), sizeof(tick.exchange) - 1);
        tick.exchange[sizeof(tick.exchange) - 1] = '\0'; // 确保结尾

        tick.timestamp = current_timestamp_ms();

        // 2. 解析 raw_data (模拟解析 JSON)
        // 在真实的高频场景，这里会使用 simdjson 进行零拷贝解析
        // 这里为了演示，我们假设 raw_data 本身就是 Symbol 名称，或者做简单处理

        if (raw_data.empty())
        {
            std::strncpy(tick.symbol, "UNKNOWN", sizeof(tick.symbol) - 1);
        }
        else
        {
            // 简单解析模拟：如果是 JSON，这里应该用 json::parse
            std::strncpy(tick.symbol, "BTC-USDT", sizeof(tick.symbol) - 1);
        }

        // 3. 模拟生成价格数据 (随机游走，仅供测试)
        // 实际代码中，这些值来自 raw_data 的解析
        static double mock_price = 50000.0;
        mock_price += (rand() % 100 - 50) * 0.1; // 随机波动

        tick.last_price = mock_price;
        tick.volume = (rand() % 1000) / 100.0;
        tick.bid_price_1 = tick.last_price - 0.5;
        tick.ask_price_1 = tick.last_price + 0.5;
        tick.bid_volume_1 = 1.2;
        tick.ask_volume_1 = 0.8;

        return tick;
    }

    // 序列化为 JSON 字符串以便 Python 容易读取
    // 生产环境建议改为 MsgPack 二进制流
    std::string DataAdaptor::to_json(const MarketTick &tick)
    {
        std::stringstream ss;
        ss << "{"
           << "\"symbol\": \"" << tick.symbol << "\","
           << "\"exchange\": \"" << tick.exchange << "\","
           << "\"timestamp\": " << tick.timestamp << ","
           << "\"last_price\": " << std::fixed << std::setprecision(2) << tick.last_price << ","
           << "\"volume\": " << tick.volume << ","
           << "\"bid_price_1\": " << tick.bid_price_1 << ","
           << "\"ask_price_1\": " << tick.ask_price_1
           << "}";
        return ss.str();
    }

} // namespace MarketFeed