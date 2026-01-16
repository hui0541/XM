#pragma once
#include <cstdint>

namespace SpeedTrader
{

    // 埋点阶段定义 (用于标识时间戳属于哪个环节)
    enum MetricStage : uint16_t
    {
        STAGE_MARKET_RECV = 100,  // C++ 网关收到行情
        STAGE_STRATEGY_IN = 200,  // Python 策略收到数据
        STAGE_STRATEGY_OUT = 201, // Python 策略发出信号
        STAGE_ORDER_SEND = 300,   // Java 网关发出报单
        STAGE_ORDER_ACK = 301,    // Java 网关收到回报
        STAGE_MATCHED = 400       // 成交
    };

    // ---------------------------------------------------------
    // 性能埋点数据包 (Alignas 8, 总大小 32 字节)
    // 设计为极简结构，通过 UDP 旁路发送给监控服务
    // ---------------------------------------------------------
    struct alignas(8) PerfMetricPacket
    {
        int64_t trace_id;  // 链路追踪ID (通常由行情的时间戳+代码Hash生成)
        int64_t timestamp; // 当前埋点时间 (纳秒)
        uint16_t stage;    // 当前阶段 (MetricStage)
        uint16_t node_id;  // 节点ID (用于区分多服务器)
        uint32_t extra;    // 预留/附加信息 (如 延迟值)

        // 构造函数
        PerfMetricPacket() : trace_id(0), timestamp(0), stage(0), node_id(0), extra(0) {}
    };

}