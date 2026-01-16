package com.trading.storage;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.ArrayList;
import java.util.List;

public class ClickHouseWriter {
    // 异步缓冲队列
    private final BlockingQueue<String[]> buffer = new LinkedBlockingQueue<>(50000);

    public ClickHouseWriter() {
        // 启动后台批量落库线程
        new Thread(this::flushLoop).start();
    }

    public void queueData(String[] row) {
        buffer.offer(row);
    }

    private void flushLoop() {
        List<String[]> batch = new ArrayList<>();
        while (true) {
            try {
                // 积累 2000 条或等待 1 秒后批量写入
                long startTime = System.currentTimeMillis();
                while (batch.size() < 2000 && (System.currentTimeMillis() - startTime < 1000)) {
                    String[] row = buffer.poll(100, java.util.concurrent.TimeUnit.MILLISECONDS);
                    if (row != null)
                        batch.add(row);
                }

                if (!batch.isEmpty()) {
                    executeBatchInsert(batch); // 真正的JDBC批量操作
                    batch.clear();
                }
            } catch (Exception e) {
                // 错误记录，保证服务不中断
            }
        }
    }
}