import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;
import redis.clients.jedis.Pipeline;
import java.util.HashMap;
import java.util.Map;

/**
 * 对应文件：Redis实时缓存.java
 * 职责：负责最新的 Tick 快照更新，供 Python 策略和 UI 实时读取
 */
public class Redis实时缓存 {

    private final JedisPool jedisPool;

    public Redis实时缓存(String host, int port, String password, int maxTotal) {
        JedisPoolConfig poolConfig = new JedisPoolConfig();
        poolConfig.setMaxTotal(maxTotal);
        poolConfig.setMaxIdle(10);
        poolConfig.setTestOnBorrow(false); // 高性能模式关闭借用检查

        if (password != null && !password.isEmpty()) {
            this.jedisPool = new JedisPool(poolConfig, host, port, 2000, password);
        } else {
            this.jedisPool = new JedisPool(poolConfig, host, port, 2000);
        }
        System.out.println("[Redis] 连接池已初始化: " + host + ":" + port);
    }

    /**
     * 更新行情快照 (使用 Pipeline 减少网络往返)
     */
    public void updateSnapshot(ClickHouse写入服务.TickData tick) {
        try (Jedis jedis = jedisPool.getResource()) {
            String key = "quote:" + tick.symbol;

            Pipeline p = jedis.pipelined();

            // 使用 Hash 存储字段
            Map<String, String> fields = new HashMap<>();
            fields.put("p", String.valueOf(tick.lastPrice)); // price
            fields.put("v", String.valueOf(tick.volume)); // volume
            fields.put("t", String.valueOf(tick.timestamp)); // time

            p.hset(key, fields);
            p.expire(key, 86400); // 1天过期

            // 如果需要，这里可以 publish 给 WebSocket
            // p.publish("market_stream", tick.symbol + "," + tick.lastPrice);

            p.sync();
        } catch (Exception e) {
            System.err.println("[Redis] 更新失败: " + e.getMessage());
        }
    }

    public void close() {
        if (jedisPool != null)
            jedisPool.close();
    }
}