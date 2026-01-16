#include "行情数据适配层.h"
#include "MarketDataTypes.h"
#include <boost/json.hpp>
#include <iostream>
#include <string>

namespace SpeedTrader
{

    class DataAdapter
    {
    public:
        /**
         * 将 JSON 字符串解析为高性能 TickData 结构体
         * 假设输入 JSON: {"s":"sh600000", "t":1678888888000, "p": 12.54, "v": 1000}
         */
        static bool parse_json_to_tick(const std::string &json_str, TickData &out_tick)
        {
            try
            {
                // 1. 解析 JSON
                boost::json::value jv = boost::json::parse(json_str);
                boost::json::object &obj = jv.as_object();

                // 2. 填充 Symbol (使用 strncpy 防止溢出，并补 \0)
                std::string symbol = boost::json::value_to<std::string>(obj.at("s"));
                std::strncpy(out_tick.symbol, symbol.c_str(), sizeof(out_tick.symbol) - 1);

                // 3. 填充时间戳
                out_tick.timestamp = obj.at("t").as_int64();

                // 4. 价格处理 (double -> int64)
                // 注意：这里需要根据实际精度需求处理，这里简单乘 10000
                double price = 0.0;
                if (obj.at("p").is_double())
                    price = obj.at("p").as_double();
                else if (obj.at("p").is_int64())
                    price = (double)obj.at("p").as_int64();

                out_tick.last_price = static_cast<int64_t>(price * PRICE_MULTIPLIER);
                out_tick.volume = obj.at("v").as_int64();

                // 标记本地接收时间
                out_tick.local_time = std::chrono::duration_cast<std::chrono::microseconds>(
                                          std::chrono::system_clock::now().time_since_epoch())
                                          .count();

                return true;
            }
            catch (std::exception &e)
            {
                std::cerr << "[Adapter] Parse Error: " << e.what() << std::endl;
                return false;
            }
        }
    };
}