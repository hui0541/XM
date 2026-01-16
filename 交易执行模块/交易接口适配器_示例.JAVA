import java.util.UUID;
import java.util.concurrent.*;

/**
 * 对应文件：交易接口适配器_示例.java
 * 职责：模拟券商柜台，提供仿真环境
 */
public class 交易接口适配器_示例 implements 券商交易接口 {
    
    private TradeCallback callback;
    private final ScheduledExecutorService simulator = Executors.newScheduledThreadPool(2);

    @Override
    public void init(String config) {
        System.out.println("[券商适配器] 模拟柜台连接成功: " + config);
    }

    @Override
    public void setCallback(TradeCallback callback) {
        this.callback = callback;
    }

    @Override
    public String insertOrder(OrderRequest req) {
        // 1. 生成模拟订单号
        String orderId = "ORD-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 4);
        System.out.println("[券商适配器] 收到报单: " + req.symbol + " " + (req.direction>0?"买":"卖") + " " + req.quantity + "@" + req.price);
        
        // 2. 模拟网络延迟 (5ms) 后回报 "已报"
        simulator.schedule(() -> {
            if (callback != null) {
                callback.onOrderUpdate(new OrderUpdate(orderId, "SUBMITTED", 0, 0, "报单已提交"));
            }
            
            // 3. 模拟撮合 (500ms 后全部成交)
            simulateMatch(orderId, req);
            
        }, 5, TimeUnit.MILLISECONDS);
        
        return orderId;
    }

    private void simulateMatch(String orderId, OrderRequest req) {
        simulator.schedule(() -> {
            if (callback != null) {
                // 模拟完全成交
                System.out.println("[券商适配器] 模拟撮合成功: " + orderId);
                callback.onOrderUpdate(new OrderUpdate(
                    orderId, "FILLED", req.price, req.quantity, "全部成交"
                ));
            }
        }, 500, TimeUnit.MILLISECONDS);
    }

    @Override
    public void cancelOrder(String orderId) {
        System.out.println("[券商适配器] 收到撤单: " + orderId);
        simulator.schedule(() -> {
            if (callback != null) {
                callback.onOrderUpdate(new OrderUpdate(orderId, "CANCELED", 0, 0, "撤单成功"));
            }
        }, 10, TimeUnit.MILLISECONDS);
    }

    @Override
    public void queryPosition() {
        // 模拟返回持仓
        System.out.println("[券商适配器] 查询持仓: 空仓");
    }
}