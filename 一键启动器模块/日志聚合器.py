import os
import datetime
import threading

class LogAggregator:
    """
    日志聚合落盘服务
    单例模式，线程安全
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, log_dir="./logs"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.start_new_log(log_dir)
            return cls._instance

    def start_new_log(self, log_dir):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.file_path = os.path.join(log_dir, f"system_all_{date_str}.log")
        self.file = open(self.file_path, "a", encoding="utf-8")

    def write(self, service_name, message):
        """ 写入日志 """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        line = f"[{timestamp}] [{service_name}] {message}\n"
        
        with self._lock:
            self.file.write(line)
            self.file.flush()

    def close(self):
        with self._lock:
            if self.file:
                self.file.close()

# 全局单例
logger = LogAggregator()