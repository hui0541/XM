#include "行情数据适配层.H"
#include <chrono>
#include <iostream>
#include <algorithm>
// 假设项目中有引入 nlohmann/json，这在现代 C++ 项目中很常见
// 如果没有，你需要添加: #include <nlohmann/json.hpp>
// using json = nlohmann::json;

// 模拟的 JSON 解析，实际生产环境请使用 simdjson 或 rapidjson 以获得极致性能
namespace MarketFeed
{

    MarketTick DataAdaptor::normalize(const std::string &raw_data, const std::string &source_exchange)
    {
        MarketTick tick;

        // 性能检查：如果数据为空，直接返回空对象
        if (raw_data.empty())
        {
            return tick;
        }

        try
        {
            // [模拟解析逻辑]
            // 在实际代码中，这里会根据 source_exchange 进行不同的字段映射
            // 示例：假设 raw_data 是简化的 JSON 格式

            // 1. 设置交易所
            std::strncpy(tick.exchange, source_exchange.c_str(), sizeof(tick.exchange) - 1);

            // 2. 设置时间戳 (如果是实时行情，通常用本机时间作为接收时间)
            tick.timestamp = current_timestamp_ms();

            // 3. 模拟字段提取 (TODO: 替换为真实的 JSON 解析)
            // 假设 raw_data 包含 "BTC-USDT"
            std::strncpy(tick.symbol, "BTC-USDT", sizeof(tick.symbol) - 1);
            tick.last_price = 98000.50; // 示例值
            tick.volume = 1.25;
            tick.bid_price_1 = 98000.00;
            tick.ask_price_1 = 98001.00;

            // 日志：低延迟场景下应减少 I/O，或使用异步日志
            // std::cout << "Normalized Tick: " << tick.symbol << " @ " << tick.last_price << std::endl;
        }
        catch (const std::exception &e)
        {
            std::cerr << "Error normalizing data: " << e.what() << std::endl;
        }

        return tick;
    }

    int64_t DataAdaptor::current_timestamp_ms()
    {
        auto now = std::chrono::system_clock::now();
        return std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count();
    }

} // namespace MarketFeed