package com.trading.cloud;

import java.io.File;

public interface CloudStorageProvider {
    void uploadFile(String localPath, String remotePath);

    void downloadFile(String remotePath, String localPath);

    boolean exists(String remotePath);
}