#pragma once
#ifndef MARKET_DATA_ADAPTER_H
#define MARKET_DATA_ADAPTER_H

#include <cstdint>
#include <cstring>
#include <string>
#include <vector>

// 定义命名空间，防止符号冲突
namespace MarketFeed
{

    // 交易方向枚举
    enum class Direction : int8_t
    {
        NONE = 0,
        BUY = 1,
        SELL = 2
    };

// 极致优化的 Tick 结构体 - 内存对齐
// 使用 pragma pack 确保跨语言/跨进程通信时的二进制兼容性
#pragma pack(push, 1)
    struct MarketTick
    {
        char symbol[32];     // 交易对名称，定长 char 数组优于 std::string
        char exchange[16];   // 交易所代码
        int64_t timestamp;   // 毫秒级时间戳
        double last_price;   // 最新成交价
        double volume;       // 成交量
        double bid_price_1;  // 买一价
        double ask_price_1;  // 卖一价
        double bid_volume_1; // 买一量
        double ask_volume_1; // 卖一量

        // 构造函数初始化，避免脏数据
        MarketTick() : timestamp(0), last_price(0.0), volume(0.0),
                       bid_price_1(0.0), ask_price_1(0.0),
                       bid_volume_1(0.0), ask_volume_1(0.0)
        {
            std::memset(symbol, 0, sizeof(symbol));
            std::memset(exchange, 0, sizeof(exchange));
        }
    };
#pragma pack(pop)

    class DataAdaptor
    {
    public:
        DataAdaptor() = default;
        ~DataAdaptor() = default;

        // 核心适配接口：将原始 JSON/HTTP 字符串转换为标准 Tick
        // 这里传入 string_view 避免拷贝 (需 C++17，如下层不支持可改为 const string&)
        static MarketTick normalize(const std::string &raw_data, const std::string &source_exchange);

        // 辅助工具：快速时间戳获取
        static int64_t current_timestamp_ms();
    };

} // namespace MarketFeed

#endif // MARKET_DATA_ADAPTER_H