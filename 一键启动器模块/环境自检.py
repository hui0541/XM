import sys
import shutil
import psutil
import socket
from PySide6.QtCore import QThread, Signal, QObject

class EnvCheckWorker(QObject):
    """
    后台环境检测工作线程
    """
    sig_log = Signal(str, bool)  # msg, is_success
    sig_finished = Signal(bool)  # all_passed

    def run_checks(self):
        all_passed = True
        
        # 1. 检查 Python 环境
        self.sig_log.emit(f"Checking Python... {sys.version.split()[0]}", True)

        # 2. 检查 Java 环境 (交易网关和存储模块依赖)
        if shutil.which("java"):
            self.sig_log.emit("Checking Java Runtime... OK", True)
        else:
            self.sig_log.emit("Checking Java Runtime... MISSING (请安装 JDK 11+)", False)
            all_passed = False

        # 3. 检查 核心端口占用 (假设 Redis=6379, ClickHouse=8123)
        # 如果是启动前检查，端口应该是空闲的；或者是外部服务已启动
        # 这里策略是：检查关键端口是否被 *其他非本机* 程序占用，或者仅仅提示状态
        ports = {6379: "Redis", 8123: "ClickHouse", 9999: "UDP Gateway"}
        for port, name in ports.items():
            is_open = self._is_port_open(port)
            status = "OCCUPIED" if is_open else "FREE"
            # 这里的逻辑根据实际需求：如果是启动新服务，occupied 可能是冲突；
            # 如果是连接外部服务，occupied 是好事。
            # 这里假设我们需要本地启动，所以 occupied 是警告
            msg = f"Port {port} ({name}): {status}"
            self.sig_log.emit(msg, not is_open) 
            if is_open:
                self.sig_log.emit(f"   -> 警告: 端口 {port} 已被占用，启动可能失败", False)

        # 4. 磁盘空间检查
        usage = psutil.disk_usage('.')
        free_gb = usage.free / (1024**3)
        if free_gb < 10:
            self.sig_log.emit(f"Disk Space: {free_gb:.2f} GB (低空间警告)", False)
        else:
            self.sig_log.emit(f"Disk Space: {free_gb:.2f} GB OK", True)

        self.sig_finished.emit(all_passed)

    def _is_port_open(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        try:
            return sock.connect_ex(('127.0.0.1', port)) == 0
        finally:
            sock.close()

class EnvChecker(QThread):
    """ 包装为 QThread 方便 UI 调用 """
    def __init__(self, worker_logic):
        super().__init__()
        self.worker = worker_logic
    
    def run(self):
        self.worker.run_checks()