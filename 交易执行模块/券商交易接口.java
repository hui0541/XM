/**
 * 对应文件：券商交易接口.java
 * 职责：定义标准化的交易动作
 */
public interface 券商交易接口 {

    // 初始化连接
    void init(String config);

    // 报单 (返回 OrderID)
    String insertOrder(OrderRequest request);

    // 撤单
    void cancelOrder(String orderId);

    // 查询持仓
    void queryPosition();

    // 注册回报回调 (当订单状态变化时调用)
    void setCallback(TradeCallback callback);

    // ============================
    // 内部数据结构
    // ============================
    @lombok.Data
    class OrderRequest {
        String symbol; // 代码
        int direction; // 1=Buy, -1=Sell
        double price; // 价格
        int quantity; // 数量
        String strategyId; // 来源策略ID
    }

    @lombok.Data
    @lombok.AllArgsConstructor
    class OrderUpdate {
        String orderId;
        String status; // SUBMITTED, PARTIAL, FILLED, CANCELED, REJECTED
        double tradedPrice;
        int tradedVolume;
        String message;
    }

    // 回调接口
    interface TradeCallback {
        void onOrderUpdate(OrderUpdate update);
    }
}