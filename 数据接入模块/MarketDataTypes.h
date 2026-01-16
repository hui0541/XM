#pragma once
#include <cstdint>
#include <cstring>
#include <atomic>

// 命名空间封装，防止符号冲突
namespace SpeedTrader
{

    // 价格乘数，将 double 转换为 int64 计算以避免浮点误差，除以 10000 还原
    constexpr double PRICE_MULTIPLIER = 10000.0;

    // ---------------------------------------------------------
    // 核心行情结构体
    // 优化：alignas(64) 确保结构体占据完整的 Cache Line，
    // 避免多核 CPU 并发访问数组相邻元素时的缓存失效（伪共享）。
    // ---------------------------------------------------------
    struct alignas(64) TickData
    {
        char symbol[16];    // 股票代码 (e.g., "sh600000\0")
        int64_t timestamp;  // 交易所时间戳 (毫秒/纳秒)
        int64_t local_time; // 本地接收时间 (用于延迟监控)

        int64_t last_price; // 最新价 (x10000)
        int64_t volume;     // 成交量
        int64_t turnover;   // 成交额

        int64_t open_interest; // 持仓量 (期货用)

        // 五档行情 (Ask/Bid)
        int64_t bid_price[5];
        int64_t bid_volume[5];
        int64_t ask_price[5];
        int64_t ask_volume[5];

        // 构造函数初始化
        TickData()
        {
            std::memset(this, 0, sizeof(TickData));
        }
    };

    // 简单的无锁环形缓冲区模板 (SPSC)
    // 用于在 IO 线程和 解析线程 之间传递数据
    template <typename T, size_t Capacity>
    class RingBuffer
    {
    public:
        RingBuffer() : head_(0), tail_(0) {}

        bool push(const T &item)
        {
            const size_t current_tail = tail_.load(std::memory_order_relaxed);
            const size_t next_tail = (current_tail + 1) % Capacity;

            if (next_tail != head_.load(std::memory_order_acquire))
            {
                data_[current_tail] = item;
                tail_.store(next_tail, std::memory_order_release);
                return true;
            }
            return false; // 队列满
        }

        bool pop(T &item)
        {
            const size_t current_head = head_.load(std::memory_order_relaxed);

            if (current_head == tail_.load(std::memory_order_acquire))
            {
                return false; // 队列空
            }

            item = data_[current_head];
            head_.store((current_head + 1) % Capacity, std::memory_order_release);
            return true;
        }

    private:
        T data_[Capacity];
        std::atomic<size_t> head_;
        std::atomic<size_t> tail_;
    };
}