package com.trading.executor;

/**
 * 极速交易接口抽象，支持插拔式对接 CTP, TORA, 或通达信 DLL
 */
public interface TradeAdapter {
    // 基础报单
    String insertOrder(String code, double price, long qty, int direction);

    // 撤单
    boolean cancelOrder(String orderId);

    // 查询资金/持仓
    void queryAccount();

    // 接收柜台回调（通过监听器模式实现）
    interface OrderListener {
        void onRtnOrder(String orderId, int status, String msg);

        void onRtnTrade(String orderId, long filledQty, double filledPrice);
    }
}