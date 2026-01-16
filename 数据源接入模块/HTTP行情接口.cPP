#include "HTTP行情接口.h"
#include "行情数据适配层.h"

#include <chrono>
#include <thread>

static int64_t now_ms()
{
    using namespace std::chrono;
    return duration_cast<milliseconds>(system_clock::now().time_since_epoch()).count();
}

void HTTP行情接口::start()
{
    if (_running.exchange(true))
        return;
    _th = std::thread(&HTTP行情接口::run_loop, this);
}

void HTTP行情接口::stop()
{
    _running.store(false);
    if (_th.joinable())
        _th.join();
}

void HTTP行情接口::run_loop()
{
    // TODO: 这里替换为 通达信/券商 HTTP/WebSocket 拉取/订阅
    while (_running.load())
    {
        MarketTick t;
        t.code = "SZ000001";
        t.last = 10.01;
        t.bid1 = 10.00;
        t.ask1 = 10.02;
        t.volume = 1000;
        t.ts_ms = now_ms();

        t = 行情数据适配层::normalize(t);

        if (_on_tick)
            _on_tick(t);

        std::this_thread::sleep_for(std::chrono::milliseconds(200));
    }
}
