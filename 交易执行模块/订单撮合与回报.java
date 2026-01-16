package com.trading.execution;

import java.util.concurrent.ConcurrentHashMap;
import java.util.Map;
import java.util.logging.Logger;

/**
 * 订单状态机 (Order State Machine)
 * 管理订单生命周期，处理从 NEW 到 FILLED/CANCELLED 的状态流转。
 */
public class OrderStateMachine {
    private static final Logger logger = Logger.getLogger(OrderStateMachine.class.getName());

    // 订单状态枚举
    public enum OrderStatus {
        UNKNOWN,
        NEW, // 已创建
        SUBMITTED, // 已提交给券商
        PARTIAL_FILLED, // 部分成交
        FILLED, // 全部成交
        CANCELLING, // 正在撤单
        CANCELLED, // 已撤单
        REJECTED // 被拒绝
    }

    // 存储所有订单的当前状态，Key 为 OrderID
    // 使用 ConcurrentHashMap 支持高并发访问
    private final Map<String, OrderStatus> orderStateMap = new ConcurrentHashMap<>();

    /**
     * 初始化订单状态
     */
    public void registerOrder(String orderId) {
        orderStateMap.putIfAbsent(orderId, OrderStatus.NEW);
        logger.info("Registered new order: " + orderId);
    }

    /**
     * 处理券商回报，更新状态
     * 
     * @param orderId      订单ID
     * @param reportStatus 券商返回的原始状态字符串
     */
    public synchronized void handleReport(String orderId, String reportStatus) {
        OrderStatus currentStatus = orderStateMap.get(orderId);
        if (currentStatus == null) {
            logger.warning("Received report for unknown order: " + orderId);
            return;
        }

        OrderStatus newStatus = mapBrokerStatusToEnum(reportStatus);

        if (isValidTransition(currentStatus, newStatus)) {
            orderStateMap.put(orderId, newStatus);
            logger.info(String.format("Order %s transitioned from %s to %s", orderId, currentStatus, newStatus));

            // TODO: 这里可以触发下游事件，例如更新持仓数据库
            if (newStatus == OrderStatus.FILLED) {
                onOrderFilled(orderId);
            }
        } else {
            logger.warning(String.format("Invalid state transition for order %s: %s -> %s", orderId, currentStatus,
                    newStatus));
        }
    }

    /**
     * 验证状态流转是否合法
     * 防止如 "已成交" -> "新订单" 这种逻辑错误
     */
    private boolean isValidTransition(OrderStatus current, OrderStatus next) {
        if (current == next)
            return true; // 状态未变，视为合法（幂等）
        if (current == OrderStatus.FILLED || current == OrderStatus.CANCELLED || current == OrderStatus.REJECTED) {
            return false; // 终态不可变
        }
        return true;
    }

    /**
     * 将券商的字符串状态映射为内部枚举
     */
    private OrderStatus mapBrokerStatusToEnum(String status) {
        if (status == null)
            return OrderStatus.UNKNOWN;
        switch (status.toUpperCase()) {
            case "SUBMITTED":
                return OrderStatus.SUBMITTED;
            case "PARTIALLY_FILLED":
                return OrderStatus.PARTIAL_FILLED;
            case "FILLED":
                return OrderStatus.FILLED;
            case "CANCELED":
            case "CANCELLED":
                return OrderStatus.CANCELLED;
            case "REJECTED":
                return OrderStatus.REJECTED;
            default:
                return OrderStatus.UNKNOWN;
        }
    }

    private void onOrderFilled(String orderId) {
        // 实现成交后的后续逻辑，如更新 Redis 缓存中的资金和持仓
        // RedisRealTimeCache.updatePosition(...)
        logger.info("Processing fill logic for order: " + orderId);
    }
}