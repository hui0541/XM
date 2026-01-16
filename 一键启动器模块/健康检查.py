import time
import socket
import psutil
from PySide6.QtCore import QThread, Signal, QObject, QMutex

class HealthStatus:
    OK = "OK"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    DEAD = "DEAD"

class HealthMonitorWorker(QObject):
    """
    健康检查后台工作者
    持续监控所有受管服务的 端口响应 和 资源占用
    """
    # 信号：服务名, 状态, 详情信息(CPU/Mem/Latency)
    sig_update = Signal(str, str, str)

    def __init__(self, services_config):
        super().__init__()
        self.services = services_config
        self.running = True
        self.mutex = QMutex()
        self._pid_map = {} # {service_name: pid}

    def update_pids(self, pid_map):
        """ 由进程管理器调用，更新最新的 PID 列表 """
        self.mutex.lock()
        self._pid_map = pid_map
        self.mutex.unlock()

    def stop(self):
        self.running = False

    def run_loop(self):
        while self.running:
            self.mutex.lock()
            current_pids = self._pid_map.copy()
            self.mutex.unlock()

            for svc in self.services:
                name = svc['name']
                # 1. 检查配置中是否定义了健康检查目标
                check_rule = svc.get('health_check')
                
                status = HealthStatus.OK
                details = []

                # --- A. 进程级检查 ---
                pid = current_pids.get(name)
                if pid and psutil.pid_exists(pid):
                    try:
                        p = psutil.Process(pid)
                        # CPU & Mem
                        cpu = p.cpu_percent(interval=None) # 非阻塞
                        mem = p.memory_info().rss / 1024 / 1024 # MB
                        details.append(f"CPU:{cpu:.1f}% Mem:{mem:.0f}MB")
                    except psutil.NoSuchProcess:
                        status = HealthStatus.DEAD
                        details.append("进程消失")
                else:
                    # 如果应该运行但没有PID，视为停止
                    if svc.get('keep_alive', False): 
                        status = HealthStatus.DEAD
                    else:
                        status = "STOPPED"

                # --- B. 端口/服务级检查 (仅对运行中的服务) ---
                if status == HealthStatus.OK and check_rule:
                    check_type = check_rule.get('type')
                    
                    if check_type == 'tcp':
                        port = check_rule.get('port')
                        latency = self._tcp_ping('127.0.0.1', port)
                        if latency is None:
                            status = HealthStatus.CRITICAL
                            details.append(f"Port {port} 无响应")
                        else:
                            details.append(f"Ping:{latency:.1f}ms")
                    
                    # 可扩展 HTTP 检查等...

                # 发送更新信号
                msg = " | ".join(details) if details else ""
                self.sig_update.emit(name, status, msg)

            # 检查间隔 3秒
            time.sleep(3)

    def _tcp_ping(self, host, port):
        """ 返回毫秒延迟，失败返回 None """
        t0 = time.time()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0) # 1秒超时
        try:
            s.connect((host, port))
            s.close()
            return (time.time() - t0) * 1000
        except:
            return None

class HealthMonitor(QThread):
    """ QThread 包装器 """
    def __init__(self, services_config):
        super().__init__()
        self.worker = HealthMonitorWorker(services_config)
    
    def update_pids(self, pid_map):
        self.worker.update_pids(pid_map)

    def run(self):
        self.worker.run_loop()
    
    def stop(self):
        self.worker.stop()
        self.wait()