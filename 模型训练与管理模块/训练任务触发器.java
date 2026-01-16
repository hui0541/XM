import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.File;

/**
 * 对应文件：训练任务触发器.java
 * 职责：Java 端调度入口，启动 Python 训练进程
 */
public class 训练任务触发器 {

    private static final String PYTHON_ENV = "python"; // 或指定具体路径 /usr/bin/python3
    private static final String SCRIPT_PATH = "自学习训练管道.py";
    private static final String WORK_DIR = "../模型训练与管理模块";

    /**
     * 触发一次全量训练
     */
    public void triggerTraining() {
        System.out.println(">>> [Scheduler] 触发每日模型自学习任务...");
        
        try {
            ProcessBuilder pb = new ProcessBuilder(PYTHON_ENV, SCRIPT_PATH);
            pb.directory(new File(WORK_DIR));
            pb.redirectErrorStream(true); // 合并 stderr 到 stdout

            Process process = pb.start();
            
            // 实时读取 Python 输出日志
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    System.out.println("[Python-Train] " + line);
                }
            }

            int exitCode = process.waitFor();
            if (exitCode == 0) {
                System.out.println(">>> [Scheduler] 训练任务成功完成。");
            } else {
                System.err.println(">>> [Scheduler] 训练任务失败，ExitCode: " + exitCode);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * 触发模型回滚 (暴露给管理后台)
     */
    public void triggerRollback() {
        System.out.println(">>> [Scheduler] 收到人工回滚指令！");
        // 这里可以通过调用 Python 的 rollback 脚本实现，或者简单地通过命令行
        // python -c "from 模型版本管理 import ModelRegistry; ModelRegistry().rollback()"
        try {
            String cmd = "from 模型版本管理 import ModelRegistry; ModelRegistry().rollback()";
            ProcessBuilder pb = new ProcessBuilder(PYTHON_ENV, "-c", cmd);
            pb.directory(new File(WORK_DIR));
            pb.inheritIO().start().waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        训练任务触发器 trigger = new 训练任务触发器();
        
        // 模拟：触发训练
        trigger.triggerTraining();
        
        // 模拟：触发回滚
        // trigger.triggerRollback(); 
    }
}