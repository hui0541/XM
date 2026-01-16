#include "实时推送接口_券商TCP.h"
#include <iostream>
#include <chrono>

namespace SpeedTrader
{

    TCPMarketSource::TCPMarketSource()
        : socket_(io_context_), resolver_(io_context_), running_(false)
    {
        // 预分配网络接收 Buffer，避免动态扩容
        buffer_.resize(8192);
    }

    TCPMarketSource::~TCPMarketSource()
    {
        stop();
    }

    bool TCPMarketSource::init(const std::string &connection_url)
    {
        // 简单的 URL 解析，假设格式 host:port
        auto pos = connection_url.find(':');
        if (pos == std::string::npos)
            return false;

        host_ = connection_url.substr(0, pos);
        port_ = connection_url.substr(pos + 1);
        return true;
    }

    void TCPMarketSource::start()
    {
        if (running_)
            return;
        running_ = true;

        // 1. 启动解析线程（消费者）
        worker_thread_ = std::thread(&TCPMarketSource::processing_loop, this);

        // 2. 启动网络连接（生产者）
        do_connect();

        // 3. 启动 IO 线程
        io_thread_ = std::thread([this]()
                                 {
            // 防止 IO 线程因异常退出
            boost::asio::io_context::work idle_work(io_context_);
            try {
                io_context_.run();
            } catch (std::exception& e) {
                std::cerr << "[IO-Fatal] " << e.what() << std::endl;
            } });

        std::cout << "[TCP] Market Source Started on " << host_ << ":" << port_ << std::endl;
    }

    void TCPMarketSource::stop()
    {
        running_ = false;
        io_context_.stop();
        if (io_thread_.joinable())
            io_thread_.join();
        if (worker_thread_.joinable())
            worker_thread_.join();
    }

    void TCPMarketSource::do_connect()
    {
        auto endpoints = resolver_.resolve(host_, port_);
        boost::asio::async_connect(socket_, endpoints,
                                   [this](boost::system::error_code ec, boost::asio::ip::tcp::endpoint)
                                   {
                                       if (!ec)
                                       {
                                           std::cout << "[TCP] Connected." << std::endl;
                                           do_read();
                                       }
                                       else
                                       {
                                           // 重连逻辑应该放在这里 (简略)
                                           std::cerr << "[TCP] Connect failed: " << ec.message() << std::endl;
                                           std::this_thread::sleep_for(std::chrono::seconds(1));
                                           do_connect();
                                       }
                                   });
    }

    void TCPMarketSource::do_read()
    {
        socket_.async_read_some(boost::asio::buffer(buffer_),
                                [this](boost::system::error_code ec, std::size_t length)
                                {
                                    if (!ec)
                                    {
                                        // ---------------------------------------------------
                                        // 模拟协议解析 (HOT PATH)
                                        // 假设收到的就是一个完整的 TickData 二进制流
                                        // 实际场景需处理粘包/半包 (使用 Circular Buffer)
                                        // ---------------------------------------------------

                                        if (length >= sizeof(TickData))
                                        {
                                            TickData *raw_tick = reinterpret_cast<TickData *>(buffer_.data());

                                            // 标记本地接收时间 (Latency Measurement)
                                            raw_tick->local_time = std::chrono::duration_cast<std::chrono::microseconds>(
                                                                       std::chrono::system_clock::now().time_since_epoch())
                                                                       .count();

                                            // 写入无锁队列 (生产者)
                                            // 如果队列满，选择丢弃最旧行情还是阻塞？
                                            // 极速交易通常选择：丢弃 (drop) 或 覆盖，因为旧行情无价值。
                                            // 这里为演示简单，若满则丢弃
                                            if (!ring_buffer_.push(*raw_tick))
                                            {
                                                std::cerr << "[Warn] RingBuffer Full, Tick Dropped!" << std::endl;
                                            }
                                        }

                                        do_read(); // 继续读取
                                    }
                                    else
                                    {
                                        socket_.close();
                                        do_connect(); // 断线重连
                                    }
                                });
    }

    void TCPMarketSource::processing_loop()
    {
        // 绑定 CPU 核心，减少上下文切换 (Linux专用，Windows需用SetThreadAffinityMask)
        // 略: 跨平台实现代码较多

        TickData tick;
        while (running_)
        {
            // 从无锁队列弹出 (消费者)
            // Busy loop 模式：CPU 100% 但延迟最低
            // 也可以用 std::this_thread::yield() 稍微让出
            while (ring_buffer_.pop(tick))
            {

                // 执行回调 (推送到 Python 策略 或 Java 存储)
                if (callback_)
                {
                    callback_(tick);
                }
            }
            // 队列空时短暂休眠，避免空转烧毁 CPU
            std::this_thread::sleep_for(std::chrono::microseconds(1));
        }
    }
}