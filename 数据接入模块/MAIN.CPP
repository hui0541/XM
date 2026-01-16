#include "实时推送接口_券商TCP.h"
#include "HTTP行情接口.h"
#include "行情数据适配层.h"
#include <iostream>
#include <boost/asio.hpp>

// UDP 广播器 (同前)
class UDPBroadcaster
{
public:
    UDPBroadcaster(boost::asio::io_context &ioc, int port)
        : socket_(ioc, boost::asio::ip::udp::endpoint(boost::asio::ip::udp::v4(), 0))
    {
        endpoint_ = boost::asio::ip::udp::endpoint(boost::asio::ip::udp::v4(), port);
        socket_.set_option(boost::asio::socket_base::broadcast(true));
    }
    void send(const SpeedTrader::TickData &tick)
    {
        socket_.send_to(boost::asio::buffer(&tick, sizeof(tick)), endpoint_);
    }

private:
    boost::asio::ip::udp::socket socket_;
    boost::asio::ip::udp::endpoint endpoint_;
};

int main(int argc, char *argv[])
{
    try
    {
        std::cout << ">>> 全栈极速行情网关 (TCP+HTTP) 启动..." << std::endl;

        // 核心 IO 上下文
        boost::asio::io_context ioc;

        // 1. 初始化 UDP 广播
        UDPBroadcaster broadcaster(ioc, 9999);

        // 2. 启动 TCP 实时流 (独立线程运行，不阻塞主 IO)
        SpeedTrader::TCPMarketSource tcp_source;
        if (tcp_source.init("127.0.0.1:8888"))
        {
            tcp_source.registerCallback([&broadcaster](const SpeedTrader::TickData &tick)
                                        {
                // 收到 TCP 行情 -> 广播
                broadcaster.send(tick); });
            tcp_source.start();
        }

        // 3. 演示 HTTP 快照拉取 (运行在主 IO 线程)
        // 场景：启动时先拉取一次 sh600000 的快照
        auto http_client = std::make_shared<SpeedTrader::HTTPMarketSource>(ioc);
        http_client->get("api.example.com", "80", "/market/snapshot?code=sh600000",
                         [&broadcaster](const std::string &json_body)
                         {
                             std::cout << "[HTTP] Snapshot Received: " << json_body.size() << " bytes" << std::endl;

                             // 解析并广播
                             SpeedTrader::TickData snapshot_tick;
                             if (SpeedTrader::DataAdapter::parse_json_to_tick(json_body, snapshot_tick))
                             {
                                 std::cout << "[HTTP] Snapshot Parsed: " << snapshot_tick.symbol
                                           << " Price: " << snapshot_tick.last_price << std::endl;
                                 broadcaster.send(snapshot_tick);
                             }
                         });

        // 4. 运行主 IO 循环 (处理 HTTP 和 UDP 发送)
        // TCP Source 内部有自己的线程，所以这里主要服务于 HTTP 和其他 IO
        ioc.run();
    }
    catch (std::exception &e)
    {
        std::cerr << "Fatal Error: " << e.what() << std::endl;
    }
    return 0;
}