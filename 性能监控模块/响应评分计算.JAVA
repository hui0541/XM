import java.util.HashMap;
import java.util.Map;

/**
 * 对应文件：响应评分计算.java
 * 职责：核心算法层，计算链路延迟与系统评分
 */
public class 响应评分计算 {

    // 延迟阈值 (单位: 微秒 us)
    private static final long THRESHOLD_MARKET_US = 5000;   // 行情传输 < 5ms
    private static final long THRESHOLD_STRATEGY_US = 2000; // 策略计算 < 2ms
    private static final long THRESHOLD_TRADE_US = 5000;    // 交易网关 < 5ms
    private static final long THRESHOLD_TOTAL_US = 20000;   // 全链路 < 20ms

    @lombok.Data
    public static class LatencyResult {
        long marketLatency;   // 行情 -> 策略
        long strategyLatency; // 策略内部耗时
        long tradeLatency;    // 策略 -> 报单
        long totalLatency;    // 端到端
        double score;         // 系统评分 0-100
        String bottleneck;    // 瓶颈环节
    }

    /**
     * 计算单次交易链路的性能指标
     * @param timestamps Map<Stage, TimestampNS>
     */
    public static LatencyResult calculate(Map<Integer, Long> timestamps) {
        LatencyResult result = new LatencyResult();
        
        // 获取关键时间点 (需与 C++ 头文件中的 Enum 对应)
        long t1 = timestamps.getOrDefault(100, 0L); // Market Recv
        long t2 = timestamps.getOrDefault(200, 0L); // Strategy In
        long t3 = timestamps.getOrDefault(201, 0L); // Strategy Out
        long t4 = timestamps.getOrDefault(300, 0L); // Order Send

        // 至少要有首尾才能计算
        if (t1 == 0 || t4 == 0) return null;

        // 计算分段耗时 (转为微秒)
        result.marketLatency = (t2 > t1) ? (t2 - t1) / 1000 : 0;
        result.strategyLatency = (t3 > t2) ? (t3 - t2) / 1000 : 0;
        result.tradeLatency = (t4 > t3) ? (t4 - t3) / 1000 : 0;
        result.totalLatency = (t4 - t1) / 1000;

        // 计算评分与瓶颈
        result.score = 100.0;
        String bottleneck = "None";
        long maxLat = 0;

        // 1. 行情传输评分
        if (result.marketLatency > THRESHOLD_MARKET_US) {
            double penalty = (result.marketLatency - THRESHOLD_MARKET_US) / 100.0;
            result.score -= Math.min(20, penalty);
            if (result.marketLatency > maxLat) { maxLat = result.marketLatency; bottleneck = "Market-Net"; }
        }

        // 2. 策略计算评分 (权重最高)
        if (result.strategyLatency > THRESHOLD_STRATEGY_US) {
            double penalty = (result.strategyLatency - THRESHOLD_STRATEGY_US) / 50.0;
            result.score -= Math.min(40, penalty);
            if (result.strategyLatency > maxLat) { maxLat = result.strategyLatency; bottleneck = "Strategy-Algo"; }
        }

        // 3. 交易网关评分
        if (result.tradeLatency > THRESHOLD_TRADE_US) {
            double penalty = (result.tradeLatency - THRESHOLD_TRADE_US) / 100.0;
            result.score -= Math.min(20, penalty);
            if (result.tradeLatency > maxLat) { maxLat = result.tradeLatency; bottleneck = "Trade-Gateway"; }
        }
        
        // 4. 总延迟惩罚
        if (result.totalLatency > THRESHOLD_TOTAL_US) {
            result.score -= 10;
        }

        result.score = Math.max(0, result.score);
        result.bottleneck = bottleneck;
        
        return result;
    }
}