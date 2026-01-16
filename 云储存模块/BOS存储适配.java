package com.trading.cloud;

import com.baidubce.auth.DefaultBceCredentials;
import com.baidubce.services.bos.BosClient;
import com.baidubce.services.bos.BosClientConfiguration;

public class BosStorageAdapter implements CloudStorageProvider {
    private final BosClient client;
    private final String bucketName = "my-trading-bucket";

    public BosStorageAdapter(String ak, String sk, String endpoint) {
        BosClientConfiguration config = new BosClientConfiguration();
        config.setCredentials(new DefaultBceCredentials(ak, sk));
        config.setEndpoint(endpoint);
        this.client = new BosClient(config);
    }

    @Override
    public void uploadFile(String localPath, String remotePath) {
        // 极速异步上传策略回测报告或样本数据
        new Thread(() -> {
            try {
                client.putObject(bucketName, remotePath, new java.io.File(localPath));
                System.out.println("[BOS] 上传成功: " + remotePath);
            } catch (Exception e) {
                System.err.println("[BOS] 上传失败: " + e.getMessage());
            }
        }).start();
    }

    @Override
    public void downloadFile(String remotePath, String localPath) {
        client.getObject(bucketName, remotePath, new java.io.File(localPath));
    }
}