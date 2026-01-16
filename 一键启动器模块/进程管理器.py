import os
from PySide6.QtCore import QObject, QProcess, Signal, QTimer
from utils import SystemUtils

class ProcessManager(QObject):
    """
    进程托管服务
    负责：启动、停止、重启、日志重定向、状态监控
    """
    # 信号定义：服务名, 状态信息, 日志内容
    sig_status_changed = Signal(str, str)
    sig_log_received = Signal(str, str)
    sig_process_finished = Signal(str, int)

    def __init__(self, service_config: dict):
        super().__init__()
        self.config = service_config
        self.name = service_config['name']
        self.process = QProcess()
        self.keep_alive = service_config.get('keep_alive', False)
        
        # 自动重启定时器
        self.restart_timer = QTimer()
        self.restart_timer.setSingleShot(True)
        self.restart_timer.timeout.connect(self.start_service)

        self._setup_process()

    def _setup_process(self):
        """配置 QProcess 运行环境"""
        # 设置工作目录
        work_dir = os.path.abspath(self.config['work_dir'])
        if not os.path.exists(work_dir):
            os.makedirs(work_dir, exist_ok=True)
        self.process.setWorkingDirectory(work_dir)

        # 合并环境变量
        env = QProcess.systemEnvironment()
        if 'env' in self.config:
            for k, v in self.config['env'].items():
                env.append(f"{k}={v}")
        self.process.setEnvironment(env)

        # 信号绑定
        self.process.readyReadStandardOutput.connect(self._handle_stdout)
        self.process.readyReadStandardError.connect(self._handle_stderr)
        self.process.stateChanged.connect(self._handle_state_change)
        self.process.finished.connect(self._handle_finished)

    def start_service(self):
        """启动服务"""
        if self.process.state() != QProcess.NotRunning:
            return
        
        cmd_line = self.config['command']
        # 解析命令和参数
        parts = cmd_line.split()
        program = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        self.sig_status_changed.emit(self.name, "正在启动...")
        self.process.start(program, args)

    def stop_service(self):
        """停止服务"""
        self.keep_alive = False  # 手动停止时禁用自动重启
        if self.process.state() != QProcess.NotRunning:
            # 尝试优雅退出
            self.process.terminate()
            # 2秒后如果还在运行，则强杀
            QTimer.singleShot(2000, self._force_kill)

    def _force_kill(self):
        if self.process.state() != QProcess.NotRunning:
            self.process.kill()

    def _handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode('utf-8', errors='ignore')
        if data.strip():
            self.sig_log_received.emit(self.name, data)

    def _handle_stderr(self):
        data = self.process.readAllStandardError().data().decode('utf-8', errors='ignore')
        if data.strip():
            self.sig_log_received.emit(self.name, f"[ERR] {data}")

    def _handle_state_change(self, state):
        state_map = {
            QProcess.NotRunning: "已停止",
            QProcess.Starting: "启动中",
            QProcess.Running: "运行中"
        }
        self.sig_status_changed.emit(self.name, state_map.get(state, "未知状态"))

    def _handle_finished(self, exit_code, exit_status):
        self.sig_status_changed.emit(self.name, f"已退出 (Code: {exit_code})")
        self.sig_process_finished.emit(self.name, exit_code)

        # 守护进程逻辑：非正常退出且开启了保活
        if self.keep_alive and exit_code != 0:
            self.sig_status_changed.emit(self.name, "3秒后触发自动重启...")
            self.restart_timer.start(3000)