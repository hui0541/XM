#pragma once
#include "行情数据适配层.h"
#include <functional>
#include <thread>
#include <atomic>

class HTTP行情接口
{
public:
    using TickCallback = std::function<void(const MarketTick &)>;

    void set_on_tick(TickCallback cb) { _on_tick = std::move(cb); }

    void start();
    void stop();

private:
    void run_loop();

    std::atomic<bool> _running{false};
    std::thread _th;
    TickCallback _on_tick;
};
