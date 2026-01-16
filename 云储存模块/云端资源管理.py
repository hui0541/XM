package com.trading.cloud;

import java.util.List;

public class CloudResourceManager {
    private CloudStorageProvider bosProvider; // 注入 BOS 适配

    public void archiveDailyData(String date) {
        // 1. 将当日 ClickHouse 导出的样本文件压缩
        // 2. 调用 BOS 接口上传
        // 3. 设置生命周期：30天后自动转为归档存储(Cold Storage)以节省成本
        String localFile = "D:/data/samples_" + date + ".zip";
        bosProvider.uploadFile(localFile, "archive/" + date + "/samples.zip");
    }
}