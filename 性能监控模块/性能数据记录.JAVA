import io.netty.bootstrap.Bootstrap;
import io.netty.buffer.ByteBuf;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.DatagramPacket;
import io.netty.channel.socket.nio.NioDatagramChannel;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

/**
 * 对应文件：性能数据记录.java
 * 职责：
 * 1. 监听 UDP 9998 接收全链路埋点
 * 2. 聚合 Trace ID
 * 3. 调用评分计算
 * 4. 结果落库/推送 UI
 */
public class 性能数据记录 {

    private static final int MONITOR_PORT = 9998;
    
    // 暂存链路数据: <TraceID, <Stage, Timestamp>>
    // 生产环境应使用带过期时间的 Cache (如 Caffeine) 防止内存泄漏
    private static final Map<Long, Map<Integer, Long>> traceBuffer = new ConcurrentHashMap<>();
    
    // 模拟 Redis 推送接口 (实际应引用 Redis 模块)
    private static void pushToRedis(long traceId, 响应评分计算.LatencyResult result) {
        // 模拟推送 JSON 到 Redis PubSub
        // key: monitor:live
        // payload: { "trace_id": ..., "score": 95.5, "e2e_us": 4500 }
        System.out.printf("[Monitor-UI] 推送评分: ID=%d 分数=%.1f 耗时=%dus 瓶颈=%s%n", 
            traceId, result.getScore(), result.getTotalLatency(), result.getBottleneck());
    }

    public static void main(String[] args) {
        System.out.println(">>> 性能监控分析服务启动 (Port " + MONITOR_PORT + ")...");
        
        // 启动清理线程 (简单的 GC 逻辑)
        ScheduledExecutorService cleaner = Executors.newSingleThreadScheduledExecutor();
        cleaner.scheduleAtFixedRate(() -> {
            if (traceBuffer.size() > 10000) traceBuffer.clear(); // 极简暴力清理
        }, 1, 1, TimeUnit.MINUTES);

        // 启动 Netty 监听
        EventLoopGroup group = new NioEventLoopGroup(1);
        try {
            Bootstrap b = new Bootstrap();
            b.group(group)
             .channel(NioDatagramChannel.class)
             .option(ChannelOption.SO_BROADCAST, true)
             .handler(new SimpleChannelInboundHandler<DatagramPacket>() {
                 @Override
                 protected void channelRead0(ChannelHandlerContext ctx, DatagramPacket packet) {
                     ByteBuf buf = packet.content();
                     
                     // 解析二进制包 (需与 C++ 结构体严格对齐)
                     if (buf.readableBytes() < 32) return;
                     
                     long traceId = buf.readLongLE();
                     long timestamp = buf.readLongLE();
                     int stage = buf.readUnsignedShortLE();
                     int nodeId = buf.readUnsignedShortLE();
                     long extra = buf.readUnsignedIntLE();

                     processMetric(traceId, stage, timestamp);
                 }
             });

            b.bind(MONITOR_PORT).sync().channel().closeFuture().await();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            group.shutdownGracefully();
        }
    }

    private static void processMetric(long traceId, int stage, long timestamp) {
        // 1. 聚合数据
        traceBuffer.putIfAbsent(traceId, new ConcurrentHashMap<>());
        Map<Integer, Long> chain = traceBuffer.get(traceId);
        chain.put(stage, timestamp);

        // 2. 检查链路是否闭环 (假设 300 是最后一个必经环节)
        // 实际逻辑可能更复杂，比如超时触发计算
        if (stage == 300) { // STAGE_ORDER_SEND
            响应评分计算.LatencyResult result = 响应评分计算.calculate(chain);
            
            if (result != null) {
                // 3. 实时推送给 UI
                pushToRedis(traceId, result);
                
                // 4. (可选) 写入 ClickHouse 性能表
                // dbWriter.insertPerfLog(result);
                
                // 5. 移除缓存
                traceBuffer.remove(traceId);
            }
        }
    }
}