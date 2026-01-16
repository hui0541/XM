#include "HTTP行情接口.h"
#include <iostream>

namespace SpeedTrader
{

    HTTPMarketSource::HTTPMarketSource(net::io_context &ioc)
        : resolver_(net::make_strand(ioc)), stream_(net::make_strand(ioc))
    {
    }

    void HTTPMarketSource::get(const std::string &host, const std::string &port, const std::string &target, HttpCallback cb)
    {
        user_callback_ = cb;

        // 设置 HTTP 请求头
        req_.version(11); // HTTP 1.1
        req_.method(http::verb::get);
        req_.target(target);
        req_.set(http::field::host, host);
        req_.set(http::field::user_agent, BOOST_BEAST_VERSION_STRING);

        // 开始解析域名
        resolver_.async_resolve(host, port,
                                beast::bind_front_handler(&HTTPMarketSource::on_resolve, shared_from_this()));
    }

    void HTTPMarketSource::on_resolve(beast::error_code ec, tcp::resolver::results_type results)
    {
        if (ec)
            return std::cerr << "[HTTP] Resolve failed: " << ec.message() << std::endl, void();

        // 设置超时
        stream_.expires_after(std::chrono::seconds(5));

        // 连接
        stream_.async_connect(results,
                              beast::bind_front_handler(&HTTPMarketSource::on_connect, shared_from_this()));
    }

    void HTTPMarketSource::on_connect(beast::error_code ec, tcp::resolver::results_type::endpoint_type)
    {
        if (ec)
            return std::cerr << "[HTTP] Connect failed: " << ec.message() << std::endl, void();

        stream_.expires_after(std::chrono::seconds(5));

        // 发送请求
        http::async_write(stream_, req_,
                          beast::bind_front_handler(&HTTPMarketSource::on_write, shared_from_this()));
    }

    void HTTPMarketSource::on_write(beast::error_code ec, std::size_t bytes_transferred)
    {
        boost::ignore_unused(bytes_transferred);
        if (ec)
            return std::cerr << "[HTTP] Write failed: " << ec.message() << std::endl, void();

        // 接收响应
        http::async_read(stream_, buffer_, res_,
                         beast::bind_front_handler(&HTTPMarketSource::on_read, shared_from_this()));
    }

    void HTTPMarketSource::on_read(beast::error_code ec, std::size_t bytes_transferred)
    {
        boost::ignore_unused(bytes_transferred);
        if (ec)
            return std::cerr << "[HTTP] Read failed: " << ec.message() << std::endl, void();

        // 成功，回调数据
        if (user_callback_)
        {
            user_callback_(res_.body());
        }

        // 优雅关闭
        beast::error_code ec_close;
        stream_.socket().shutdown(tcp::socket::shutdown_both, ec_close);
    }
}