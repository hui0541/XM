#ifndef MARKET_ADAPTER_H
#define MARKET_ADAPTER_H

#include <string>
#include <unordered_map>
#include <mutex>
#include "实时推送接口_券商TCP.h"

struct MarketEnv
{
    int up_count = 0;        // 涨家数
    int down_count = 0;      // 跌家数
    int limit_up = 0;        // 涨停家数
    double total_volume = 0; // 全市场成交额
};

class MarketDataAdapter
{
public:
    static void processAndPush(const TickData &tick);
    static void calculateGlobalEnv(); // 定时生成环境因子包
private:
    static std::unordered_map<std::string, double> last_prices; // 缓存各股最新价
    static std::mutex mtx;
};

#endif