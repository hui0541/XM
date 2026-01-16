#include "实时推送接口_券商TCP.h"
#include "行情数据适配层.h"

#include <chrono>
#include <thread>

static int64_t now_ms2()
{
    using namespace std::chrono;
    return duration_cast<milliseconds>(system_clock::now().time_since_epoch()).count();
}

void 实时推送接口_券商TCP::start()
{
    if (_running.exchange(true))
        return;
    _producer = std::thread(&实时推送接口_券商TCP::producer_loop, this);
    _consumer = std::thread(&实时推送接口_券商TCP::consumer_loop, this);
}

void 实时推送接口_券商TCP::stop()
{
    _running.store(false);
    if (_producer.joinable())
        _producer.join();
    if (_consumer.joinable())
        _consumer.join();
}

void 实时推送接口_券商TCP::producer_loop()
{
    // TODO: 替换为 券商主动推送 TCP/UDP 订阅读包
    while (_running.load())
    {
        MarketTick t;
        t.code = "SH600000";
        t.last = 12.34;
        t.bid1 = 12.33;
        t.ask1 = 12.35;
        t.volume = 2000;
        t.ts_ms = now_ms2();

        t = 行情数据适配层::normalize(t);

        // spsc_queue 满了就丢（极速链路常见策略：丢旧/丢新可配置）
        _q.push(t);

        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
}

void 实时推送接口_券商TCP::consumer_loop()
{
    MarketTick t;
    while (_running.load())
    {
        while (_q.pop(t))
        {
            if (_on_tick)
                _on_tick(t);
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
    }
}
