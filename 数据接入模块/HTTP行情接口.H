#pragma once
#include "行情数据适配层.h"
#include <boost/beast/core.hpp>
#include <boost/beast/http.hpp>
#include <boost/beast/version.hpp>
#include <boost/asio/strand.hpp>
#include <memory>
#include <string>
#include <functional>

namespace SpeedTrader
{

    namespace beast = boost::beast;
    namespace http = beast::http;
    namespace net = boost::asio;
    using tcp = boost::asio::ip::tcp;

    // HTTP 请求回调：成功返回 Body，失败返回空字符串
    using HttpCallback = std::function<void(const std::string &response_body)>;

    class HTTPMarketSource : public std::enable_shared_from_this<HTTPMarketSource>
    {
    public:
        // 使用 shared_ptr 管理生命周期，防止异步回调时对象已销毁
        explicit HTTPMarketSource(net::io_context &ioc);

        // 异步发送 GET 请求
        // host: api.broker.com, target: /v1/market/snapshot?code=sh600000
        void get(const std::string &host, const std::string &port, const std::string &target, HttpCallback cb);

    private:
        void on_resolve(beast::error_code ec, tcp::resolver::results_type results);
        void on_connect(beast::error_code ec, tcp::resolver::results_type::endpoint_type);
        void on_write(beast::error_code ec, std::size_t bytes_transferred);
        void on_read(beast::error_code ec, std::size_t bytes_transferred);

    private:
        tcp::resolver resolver_;
        beast::tcp_stream stream_;
        beast::flat_buffer buffer_; // 接收缓冲区
        http::request<http::empty_body> req_;
        http::response<http::string_body> res_;

        HttpCallback user_callback_;
    };
}