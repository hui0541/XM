#pragma once
#include "行情数据适配层.h"
#include <boost/asio.hpp>
#include <thread>
#include <atomic>
#include <vector>

namespace SpeedTrader
{

    class TCPMarketSource : public IMarketDataSource
    {
    public:
        TCPMarketSource();
        virtual ~TCPMarketSource();

        bool init(const std::string &connection_url) override;
        void start() override;
        void stop() override;

    private:
        void do_connect();
        void do_read();
        void processing_loop(); // 独立的解析线程逻辑

    private:
        boost::asio::io_context io_context_;
        boost::asio::ip::tcp::socket socket_;
        boost::asio::ip::tcp::resolver resolver_;

        std::string host_;
        std::string port_;

        std::vector<char> buffer_; // 接收缓冲区
        std::atomic<bool> running_;

        std::thread io_thread_;     // IO 线程
        std::thread worker_thread_; // 数据解析工作线程

        // 极速环形队列：容量 4096，存储原始 TickData
        // 实际生产中，这里通常存储原始二进制包(char*)以进一步减少拷贝，
        // 但为演示清晰，直接存 TickData
        RingBuffer<TickData, 4096> ring_buffer_;
    };
}