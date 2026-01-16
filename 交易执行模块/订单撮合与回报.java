import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * 对应文件：订单撮合与回报.java
 * 职责：订单状态机管理 (OMS - Order Management System)
 */
public class 订单撮合与回报 implements 券商交易接口.TradeCallback {

    // 内存订单库: <OrderID, OrderInfo>
    private final Map<String, OrderInfo> orderBook = new ConcurrentHashMap<>();
    
    @lombok.Data
    public static class OrderInfo {
        String internalId; // 内部ID
        String brokerId;   // 券商返回ID
        String symbol;
        String status;
        long createTime;
        long updateTime;
    }

    /**
     * 处理来自券商的回报推送
     */
    @Override
    public void onOrderUpdate(券商交易接口.OrderUpdate update) {
        String orderId = update.getOrderId();
        
        OrderInfo order = orderBook.get(orderId);
        if (order == null) {
            // 可能是系统重启前下的单，或者是新单
            order = new OrderInfo();
            order.setBrokerId(orderId);
            order.setCreateTime(System.currentTimeMillis());
            orderBook.put(orderId, order);
        }
        
        order.setStatus(update.getStatus());
        order.setUpdateTime(System.currentTimeMillis());
        
        // 打印关键日志
        printLog(order, update);
        
        // TODO: 这里可以将回报通过 UDP/Redis 推送回 Python 策略端
    }
    
    public void registerOrder(String brokerOrderId, String symbol) {
        OrderInfo info = new OrderInfo();
        info.setBrokerId(brokerOrderId);
        info.setSymbol(symbol);
        info.setStatus("SENDING");
        info.setCreateTime(System.currentTimeMillis());
        orderBook.put(brokerOrderId, info);
    }

    private void printLog(OrderInfo order, 券商交易接口.OrderUpdate update) {
        String colorCode = "\u001B[33m"; // 黄色
        if ("FILLED".equals(update.getStatus())) colorCode = "\u001B[32m"; // 绿色
        if ("REJECTED".equals(update.getStatus())) colorCode = "\u001B[31m"; // 红色
        
        System.out.printf("%s[OMS] 订单更新: ID=%s 状态=%s 价格=%.2f 量=%d Msg=%s\u001B[0m%n",
                colorCode, update.getOrderId(), update.getStatus(), 
                update.getTradedPrice(), update.getTradedVolume(), update.getMessage());
    }
}