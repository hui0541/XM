package com.trading.storage;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

public class RedisCache {
    private static final JedisPool pool;

    static {
        JedisPoolConfig config = new JedisPoolConfig();
        config.setMaxTotal(128); // 高并发配置
        config.setMaxIdle(64);
        pool = new JedisPool(config, "localhost", 6379);
    }

    /**
     * 为策略提供极速的热数据读取
     */
    public String getMarketEnv() {
        try (Jedis jedis = pool.getResource()) {
            return jedis.get("global_market_env");
        }
    }

    /**
     * 写入性能监控指标
     */
    public void recordMetric(String traceId, String metric) {
        try (Jedis jedis = pool.getResource()) {
            jedis.hset("metrics:" + traceId, "data", metric);
            jedis.expire("metrics:" + traceId, 3600); // 1小时自动过期
        }
    }
}