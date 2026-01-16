#pragma once
#include "行情数据适配层.h"

#include <functional>
#include <thread>
#include <atomic>
#include <boost/lockfree/spsc_queue.hpp>

class 实时推送接口_券商TCP
{
public:
    using TickCallback = std::function<void(const MarketTick &)>;

    void set_on_tick(TickCallback cb) { _on_tick = std::move(cb); }

    void start();
    void stop();

private:
    void producer_loop(); // 模拟推送线程
    void consumer_loop(); // 消费线程（后续这里把数据喂给策略/落库）

    std::atomic<bool> _running{false};
    std::thread _producer;
    std::thread _consumer;
    TickCallback _on_tick;

    // 单生产者单消费者队列（极速链路）
    boost::lockfree::spsc_queue<MarketTick, boost::lockfree::capacity<8192>> _q;
};
