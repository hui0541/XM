public class MarketBreaker {
    // 稳定性增强：环境断路器
    public boolean shouldHaltTrading(double currentSentiment) {
        if (currentSentiment < 15.0) {
            // 极度恐慌环境，自动触发全系统停止交易指令
            System.err.println("[CRITICAL] 市场极度恐慌，触发自动熔断！");
            return true;
        }
        return false;
    }
}