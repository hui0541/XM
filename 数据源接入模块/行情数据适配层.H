#pragma once
#ifndef MARKET_DATA_ADAPTER_H
#define MARKET_DATA_ADAPTER_H

#include <cstdint>
#include <string>

namespace MarketFeed
{

#pragma pack(push, 1)
    struct MarketTick
    {
        char symbol[32];
        char exchange[16];
        int64_t timestamp;
        double last_price;
        double volume;
        double bid_price_1;
        double ask_price_1;
        double bid_volume_1;
        double ask_volume_1;

        MarketTick() : timestamp(0), last_price(0.0), volume(0.0),
                       bid_price_1(0.0), ask_price_1(0.0)
        {
            symbol[0] = '\0';
            exchange[0] = '\0';
        }
    };
#pragma pack(pop)

    class DataAdaptor
    {
    public:
        static MarketTick normalize(const std::string &raw_data, const std::string &source_exchange);
        static int64_t current_timestamp_ms();

        // 新增：序列化接口
        static std::string to_json(const MarketTick &tick);
    };

}
#endif