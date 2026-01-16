import io.netty.bootstrap.Bootstrap;
import io.netty.buffer.ByteBuf;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.DatagramPacket;
import io.netty.channel.socket.nio.NioDatagramChannel;
import org.yaml.snakeyaml.Yaml;

import java.io.FileInputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;

/**
 * 对应文件：ClickHouse写入服务.java
 * 职责：
 * 1. 启动 Netty UDP Server 接收 C++ 广播
 * 2. 解析二进制 Tick 数据
 * 3. 写入 Redis 缓存
 * 4. 批量写入 ClickHouse
 */
public class ClickHouse写入服务 {

    // ==========================================
    // 内部类：Tick数据结构 (对应 C++ alignas(64))
    // ==========================================
    public static class TickData {
        public String symbol;
        public long timestamp;
        public long localTime;
        public double lastPrice;
        public long volume;
        public double turnover;
        public long openInterest;
        public double[] bidPrice = new double[5];
        public long[] bidVolume = new long[5];
        public double[] askPrice = new double[5];
        public long[] askVolume = new long[5];

        // 从 Netty ByteBuf 解析
        public static TickData fromByteBuf(ByteBuf buf) {
            if (buf.readableBytes() < 224)
                return null; // 基础长度校验

            TickData t = new TickData();

            // 1. Symbol (16 bytes)
            byte[] sBytes = new byte[16];
            buf.readBytes(sBytes);
            int len = 0;
            while (len < 16 && sBytes[len] != 0)
                len++;
            t.symbol = new String(sBytes, 0, len, StandardCharsets.UTF_8);

            // 2. 基础字段 (Little Endian)
            t.timestamp = buf.readLongLE();
            t.localTime = buf.readLongLE();
            t.lastPrice = buf.readLongLE() / 10000.0;
            t.volume = buf.readLongLE();
            t.turnover = buf.readLongLE();
            t.openInterest = buf.readLongLE();

            // 3. 五档
            for (int i = 0; i < 5; i++)
                t.bidPrice[i] = buf.readLongLE() / 10000.0;
            for (int i = 0; i < 5; i++)
                t.bidVolume[i] = buf.readLongLE();
            for (int i = 0; i < 5; i++)
                t.askPrice[i] = buf.readLongLE() / 10000.0;
            for (int i = 0; i < 5; i++)
                t.askVolume[i] = buf.readLongLE();

            return t;
        }
    }

    // ==========================================
    // 全局变量
    // ==========================================
    private static Redis实时缓存 redisService;
    private static BlockingQueue<TickData> dbQueue = new LinkedBlockingQueue<>(100000);
    private static volatile boolean running = true;
    private static Map<String, Object> config;

    // ==========================================
    // 主入口
    // ==========================================
    public static void main(String[] args) {
        System.out.println(">>> 启动 [数据存储模块] Java核心 ...");

        try {
            // 1. 加载配置
            loadConfig();

            // 2. 初始化 Redis
            Map<String, Object> redisCfg = (Map<String, Object>) config.get("redis");
            redisService = new Redis实时缓存(
                    (String) redisCfg.get("host"),
                    (Integer) redisCfg.get("port"),
                    (String) redisCfg.get("password"),
                    (Integer) redisCfg.get("pool_max_total"));

            // 3. 启动 ClickHouse 写入线程
            Thread writerThread = new Thread(new BatchWriterTask(), "CH-Writer");
            writerThread.start();

            // 4. 启动 Netty UDP 接收
            startUdpServer();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void loadConfig() throws Exception {
        Yaml yaml = new Yaml();
        try (InputStream in = new FileInputStream("数据库连接配置.yaml")) {
            config = yaml.load(in);
            System.out.println("[Config] 配置加载成功");
        }
    }

    // ==========================================
    // Netty UDP 监听逻辑
    // ==========================================
    private static void startUdpServer() throws InterruptedException {
        Map<String, Object> listenCfg = (Map<String, Object>) config.get("listen");
        int port = (Integer) listenCfg.get("port");

        EventLoopGroup group = new NioEventLoopGroup(2);
        try {
            Bootstrap b = new Bootstrap();
            b.group(group)
                    .channel(NioDatagramChannel.class)
                    .option(ChannelOption.SO_BROADCAST, true)
                    .option(ChannelOption.SO_RCVBUF, (Integer) listenCfg.get("buffer_size"))
                    .handler(new SimpleChannelInboundHandler<DatagramPacket>() {
                        @Override
                        protected void channelRead0(ChannelHandlerContext ctx, DatagramPacket packet) {
                            ByteBuf content = packet.content();
                            TickData tick = TickData.fromByteBuf(content);
                            if (tick != null) {
                                // A. 放入队列待写入 ClickHouse
                                if (!dbQueue.offer(tick)) {
                                    System.err.println("[Warn] DB队列已满，丢弃数据: " + tick.symbol);
                                }
                                // B. 更新 Redis
                                redisService.updateSnapshot(tick);
                            }
                        }
                    });

            System.out.println("[Netty] UDP监听启动 @ Port " + port);
            b.bind(port).sync().channel().closeFuture().await();
        } finally {
            group.shutdownGracefully();
        }
    }

    // ==========================================
    // ClickHouse 批量写入任务
    // ==========================================
    static class BatchWriterTask implements Runnable {
        @Override
        public void run() {
            Map<String, Object> chCfg = (Map<String, Object>) config.get("clickhouse");
            String url = (String) chCfg.get("url");
            int batchSize = (Integer) chCfg.get("batch_size");
            int flushMs = (Integer) chCfg.get("flush_interval_ms");

            List<TickData> batch = new ArrayList<>(batchSize);
            long lastFlush = System.currentTimeMillis();

            System.out.println("[ClickHouse] 批量写入线程已就绪 -> " + url);

            while (running) {
                try {
                    TickData tick = dbQueue.poll(100, TimeUnit.MILLISECONDS);
                    if (tick != null) batch.add(tick);

                    long now = System.currentTimeMillis();
                    if (!batch.isEmpty() && (batch.size() >= batchSize || now - lastFlush >= flushMs)) {
                        doFlush(batch, url);
                        batch.clear();
                        lastFlush = now;
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }

        private void doFlush(List<TickData> list, String url) {
            String sql = "INSERT INTO market_ticks (symbol, timestamp, local_time, last_price, volume, turnover, open_interest, bid_price, bid_volume, ask_price, ask_volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
            
            try (Connection conn = DriverManager.getConnection(url);
                 PreparedStatement ps = conn.prepareStatement(sql)) {
                
                for (TickData t : list) {
                    ps.setString(1, t.symbol);
                    ps.setLong(2, t.timestamp); // JDBC驱动会自动处理 DateTime64
                    ps.setLong(3, t.localTime);
                    ps.setDouble(4, t.lastPrice);
                    ps.setLong(5, t.volume);
                    ps.setDouble(6, t.turnover);
                    ps.setLong(7, t.openInterest);
                    
                    // 数组转换
                    ps.setArray(8, conn.createArrayOf("Float64", toObjDouble(t.bidPrice)));
                    ps.setArray(9, conn.createArrayOf("Int64", toObjLong(t.bidVolume)));
                    ps.setArray(10, conn.createArrayOf("Float64", toObjDouble(t.askPrice)));
                    ps.setArray(11, conn.createArrayOf("Int64", toObjLong(t.askVolume)));
                    
                    ps.addBatch();
                }
                ps.executeBatch();
                // System.out.println("[CH] 成功落库: " + list.size()); // 高频时建议注释掉
                
            } catch (SQLException e) {
                System.err.println("[CH] 写入失败: " + e.getMessage());
            }
        }

        // 辅助转换
        private Double[] toObjDouble(double[] arr) {
            Double[] res = new Double[arr.length];
            for(int i=0; i<arr.length; i++) res[i] = arr[i];
            return res;
        }
        private Long[] toObjLong(long[] arr) {
            Long[] res = new Long[arr.length];
            for(int i=0; i<arr.length; i++) res[i] = arr[i];
            return res;
        }
    }
}```

---

###💡如何编译与运行（重要）

因为我们没有使用 Maven 结构，
而是直接使用 Java 文件，
所以编译命令需要手动指定 Classpath。

**1.

准备依赖包 (.jar)**
请确保 `数据存储模块/lib` 目录下有以下 Jar 包（或同等依赖）：
* `netty-all-4.1.x.jar`
* `jedis-4.x.jar`
* `clickhouse-jdbc-0.4.x.jar`
* `snakeyaml-1.33.jar`
* `slf4j-api.jar` & `slf4j-simple.jar`

**2.

编译命令 (Windows CMD)**
```cmd
cd 数据存储模块
javac -cp "lib/*;." -encoding UTF-8 Redis实时缓存.java ClickHouse写入服务.java
```

**3. 运行命令**
```cmd
java -cp "lib/*;." ClickHouse写入服务