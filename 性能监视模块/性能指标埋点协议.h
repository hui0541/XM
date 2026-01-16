#ifndef PERF_PROTOCOL_H
#define PERF_PROTOCOL_H

#include <chrono>
#include <string>

// 使用 Windows 高精度计时器 (QueryPerformanceCounter)
#define PERF_START(name) auto start_##name = std::chrono::high_resolution_clock::now();

#define PERF_END(name, trace_id)                                                                                   \
    auto end_##name = std::chrono::high_resolution_clock::now();                                                   \
    long long duration = std::chrono::duration_cast<std::chrono::microseconds>(end_##name - start_##name).count(); \
    save_to_perf_queue(trace_id, #name, duration);

// 模拟发送到性能监控队列
inline void save_to_perf_queue(const std::string &tid, const std::string &step, long long us)
{
    // redisCommand(ctx, "LPUSH perf_logs '%s:%s:%lld'", tid.c_str(), step.c_str(), us);
}

#endif