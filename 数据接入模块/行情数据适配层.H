#pragma once
#include "MarketDataTypes.h"
#include <functional>
#include <string>

namespace SpeedTrader
{

    // 回调函数类型定义：当收到并解析完 Tick 后调用
    using OnTickCallback = std::function<void(const TickData &)>;

    class IMarketDataSource
    {
    public:
        virtual ~IMarketDataSource() = default;

        // 初始化连接
        virtual bool init(const std::string &config_str) = 0;

        // 开始接收
        virtual void start() = 0;

        // 停止接收
        virtual void stop() = 0;

        // 注册回调
        void registerCallback(OnTickCallback cb)
        {
            callback_ = cb;
        }

    protected:
        OnTickCallback callback_;
    };
}