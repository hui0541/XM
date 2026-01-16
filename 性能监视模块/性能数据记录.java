package com.trading.monitor;

import redis.clients.jedis.Jedis;
import java.util.Map;

public class PerformanceRecorder {
    private Jedis redis = new Jedis("localhost", 6379);

    /**
     * 记录链路各环节耗时，生成的 trace_id 贯穿 C++/Python/Java
     */
    public void recordLatency(String traceId, String stepName, long latencyUs) {
        // 使用 Redis Hash 存储链路数据
        redis.hset("trace:" + traceId, stepName, String.valueOf(latencyUs));
        // 设置 10 分钟过期，防止内存溢出
        redis.expire("trace:" + traceId, 600);

        // 如果耗时超过阈值(如 1ms)，推送实时告警
        if (latencyUs > 1000) {
            redis.publish("performance_alerts", "Slow step: " + stepName + " latency: " + latencyUs + "us");
        }
    }
}