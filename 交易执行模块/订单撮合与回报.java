public class OrderStateMachine {
    enum State {
        NEW, SUBMITTED, PARTIAL, FILLED, CANCELLED, REJECTED
    }

    public void handleReport(String orderId, String status) {
        // 根据券商返回更新本地订单状态
        State currentState = getOrderState(orderId);

        switch (status) {
            case "0": // 成交
                updateState(orderId, State.FILLED);
                break;
            case "ERR":
                // 自动纠错机制：如果报单失败，尝试重试或发出告警
                retryOrAlert(orderId);
                break;
        }
    }

    private void retryOrAlert(String orderId) {
        // 稳定性保障：实现最多3次重试逻辑
    }
}