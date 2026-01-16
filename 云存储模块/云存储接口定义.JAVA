import java.io.File;
import java.io.InputStream;

/**
 * 对应文件：云存储接口定义.java
 * 职责：定义云存储的标准行为 (Strategy Pattern)，解耦具体厂商
 */
public interface 云存储接口定义 {

    /**
     * 初始化连接
     * @param endpoint 访问域名
     * @param ak Access Key
     * @param sk Secret Key
     */
    void init(String endpoint, String ak, String sk);

    /**
     * 上传文件 (支持自动重试)
     * @param bucket 存储桶
     * @param key 云端路径 (如 models/v1/xgb.model)
     * @param file 本地文件
     * @return 是否成功
     */
    boolean upload(String bucket, String key, File file);

    /**
     * 流式上传 (用于日志流)
     */
    boolean uploadStream(String bucket, String key, InputStream inputStream, long length);

    /**
     * 下载文件
     */
    boolean download(String bucket, String key, String localPath);

    /**
     * 检查文件是否存在
     */
    boolean exists(String bucket, String key);
}