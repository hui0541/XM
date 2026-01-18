# -*- coding: utf-8 -*-
"""
A股极速交易系统 - 总控台 (Launcher Main)
集成功能：服务编排、进程守护、健康监控、配置热更、环境自检、日志聚合
"""

import sys
import os
import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QTextEdit, QTableWidget, 
                               QTableWidgetItem, QHeaderView, QLabel, QTabWidget, 
                               QMessageBox, QSplitter, QProgressBar)
from PySide6.QtCore import Qt, Slot, QTimer, QSize
from PySide6.QtGui import QColor, QFont, QIcon, QAction

# 引入子模块
from utils import SystemUtils
from 进程管理器 import ProcessManager
from 配置编译器 import ConfigEditor
from 环境自检 import EnvCheckWorker, EnvChecker
from 健康检查 import HealthMonitor
from 日志聚合器 import LogAggregator

# 全局样式表 (Dark Mode)
DARK_STYLESHEET = """
QMainWindow { background-color: #1e1e1e; color: #e0e0e0; }
QWidget { background-color: #1e1e1e; color: #e0e0e0; font-family: "Microsoft YaHei", "Consolas"; }
QTabWidget::pane { border: 1px solid #3d3d3d; top: -1px; }
QTabBar::tab { background: #2d2d2d; color: #888; padding: 8px 20px; border: 1px solid #3d3d3d; border-bottom: none; }
QTabBar::tab:selected { background: #1e1e1e; color: #00aaff; border-top: 2px solid #00aaff; }
QTableWidget { background-color: #252526; border: 1px solid #3d3d3d; gridline-color: #3d3d3d; }
QTableWidget::item { padding: 4px; }
QTableWidget::item:selected { background-color: #094771; }
QHeaderView::section { background-color: #333333; padding: 4px; border: none; font-weight: bold; }
QTextEdit { background-color: #101010; color: #00ff00; font-family: "Consolas"; border: 1px solid #3d3d3d; }
QPushButton { background-color: #0e639c; border: none; padding: 6px 12px; color: white; border-radius: 2px; }
QPushButton:hover { background-color: #1177bb; }
QPushButton:pressed { background-color: #094771; }
QPushButton#stop_btn { background-color: #8b0000; }
QPushButton#stop_btn:hover { background-color: #a00000; }
"""

class ServiceMonitorPanel(QWidget):
    """
    核心面板：服务列表、操作控制、日志流、健康状态
    """
    def __init__(self, config_path):
        super().__init__()
        self.config_path = config_path
        self.managers = {}        # {service_name: ProcessManager}
        self.health_thread = None # 健康检查线程
        
        # 初始化日志聚合器
        self.logger = LogAggregator()
        
        self.setup_ui()
        self.load_services()
        self.start_health_monitor()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 1. 顶部控制栏
        top_bar = QHBoxLayout()
        
        self.btn_start_all = QPushButton("🚀 一键启动全部")
        self.btn_start_all.clicked.connect(self.start_all)
        self.btn_start_all.setMinimumHeight(35)
        
        self.btn_stop_all = QPushButton("🛑 一键紧急停止")
        self.btn_stop_all.setObjectName("stop_btn")
        self.btn_stop_all.clicked.connect(self.stop_all)
        self.btn_stop_all.setMinimumHeight(35)

        self.lbl_summary = QLabel("系统就绪")
        self.lbl_summary.setStyleSheet("color: #888888; font-size: 12px;")

        top_bar.addWidget(self.btn_start_all)
        top_bar.addWidget(self.btn_stop_all)
        top_bar.addStretch()
        top_bar.addWidget(self.lbl_summary)
        layout.addLayout(top_bar)

        # 2. 中部：服务列表 (使用 Splitter 允许调整高度)
        splitter = QSplitter(Qt.Vertical)
        layout.addWidget(splitter)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["服务名称", "分组", "运行状态", "健康指标 (Health)", "操作"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents) # 健康列自适应
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        splitter.addWidget(self.table)

        # 3. 底部：实时日志
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)
        log_layout.setContentsMargins(0, 0, 0, 0)
        log_label = QLabel("📝 实时聚合日志 (Stdout/Stderr)")
        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        log_layout.addWidget(log_label)
        log_layout.addWidget(self.log_console)
        splitter.addWidget(log_widget)

        # 设置 Splitter 比例 (6:4)
        splitter.setStretchFactor(0, 6)
        splitter.setStretchFactor(1, 4)

    def load_services(self):
        """ 加载/重载服务配置 """
        # 清理旧对象
        self.stop_all() 
        self.table.setRowCount(0)
        self.managers.clear()

        try:
            config = SystemUtils.load_config(self.config_path)
            # 按优先级排序
            services = sorted(config.get('services', []), key=lambda x: x.get('priority', 99))
            
            self.table.setRowCount(len(services))
            
            for idx, svc in enumerate(services):
                name = svc['name']
                
                # 初始化进程管理器
                manager = ProcessManager(svc)
                manager.sig_status_changed.connect(self.on_process_status)
                manager.sig_log_received.connect(self.on_process_log)
                self.managers[name] = manager

                # 填充表格
                self.table.setItem(idx, 0, QTableWidgetItem(name))
                self.table.setItem(idx, 1, QTableWidgetItem(svc.get('group', 'Default')))
                
                status_item = QTableWidgetItem("STOPPED")
                status_item.setForeground(QColor("#777777"))
                self.table.setItem(idx, 2, status_item)
                
                health_item = QTableWidgetItem("-")
                health_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(idx, 3, health_item)

                # 操作按钮
                btn_widget = QWidget()
                l = QHBoxLayout(btn_widget)
                l.setContentsMargins(4, 2, 4, 2)
                l.setSpacing(5)
                
                btn_start = QPushButton("启动")
                btn_start.setStyleSheet("background-color: #2da44e; padding: 4px;")
                btn_start.clicked.connect(lambda c, m=manager: m.start_service())
                
                btn_stop = QPushButton("停止")
                btn_stop.setObjectName("stop_btn")
                btn_stop.setStyleSheet("background-color: #cf222e; padding: 4px;")
                btn_stop.clicked.connect(lambda c, m=manager: m.stop_service())
                
                l.addWidget(btn_start)
                l.addWidget(btn_stop)
                self.table.setCellWidget(idx, 4, btn_widget)

            self.append_log("System", f"配置加载完毕，共 {len(services)} 个服务。")
            
            # 重启健康检查以适应新配置
            self.start_health_monitor()

        except Exception as e:
            self.append_log("System", f"配置加载严重错误: {e}")
            QMessageBox.critical(self, "错误", f"配置加载失败: {e}")

    def start_health_monitor(self):
        """ 启动或重启健康检查线程 """
        if self.health_thread:
            self.health_thread.stop()
            self.health_thread = None

        try:
            config = SystemUtils.load_config(self.config_path)
            self.health_thread = HealthMonitor(config.get('services', []))
            self.health_thread.worker.sig_update.connect(self.on_health_update)
            self.health_thread.start()
            
            # 启动 PID 同步定时器 (每 2 秒同步一次 PID 给监控线程)
            self.pid_timer = QTimer(self)
            self.pid_timer.timeout.connect(self._sync_pids)
            self.pid_timer.start(2000)
            
        except Exception as e:
            self.append_log("System", f"健康监控启动失败: {e}")

    def _sync_pids(self):
        """ 收集当前运行中的 PID """
        pid_map = {}
        for name, mgr in self.managers.items():
            if mgr.process.state() == ProcessManager.QProcess.Running:
                pid_map[name] = mgr.process.processId()
        if self.health_thread:
            self.health_thread.update_pids(pid_map)

    @Slot(str, str)
    def on_process_status(self, name, status):
        """ 进程状态变更回调 """
        row = self._find_row(name)
        if row is not None:
            item = self.table.item(row, 2)
            item.setText(status)
            if "运行中" in status:
                item.setForeground(QColor("#4ec9b0")) # 亮青色
            elif "停止" in status or "退出" in status:
                item.setForeground(QColor("#777777")) # 灰色
            else:
                item.setForeground(QColor("#dcdcaa")) # 黄色
            
            self.logger.write(name, f"Status Change: {status}")

    @Slot(str, str, str)
    def on_health_update(self, name, status, details):
        """ 健康检查回调 """
        row = self._find_row(name)
        if row is not None:
            item = self.table.item(row, 3)
            item.setText(status)
            item.setToolTip(details) # 鼠标悬停显示 CPU/内存/Ping

            if status == "OK":
                item.setForeground(QColor("#00ff00"))
            elif status == "WARNING":
                item.setForeground(QColor("#ffff00"))
            elif status == "CRITICAL" or status == "DEAD":
                item.setForeground(QColor("#ff0000"))
                item.setFont(QFont("Segoe UI", 9, QFont.Bold))
            else:
                item.setForeground(QColor("#555555"))

    @Slot(str, str)
    def on_process_log(self, name, msg):
        """ 日志回调 """
        # 1. 写入本地文件
        self.logger.write(name, msg)
        # 2. 更新 UI (带简单的 HTML 颜色)
        self.append_log(name, msg)

    def append_log(self, name, msg):
        time_str = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        color = "#569cd6" # Blue for service name
        msg_color = "#d4d4d4" # Default text
        
        if "[ERR]" in msg or "Error" in msg:
            msg_color = "#ff5555"
        elif "Warning" in msg:
            msg_color = "#ffaa00"

        html = f'<span style="color:#666;">[{time_str}]</span> <b style="color:{color};">[{name}]</b> <span style="color:{msg_color};">{msg}</span>'
        
        # 性能优化：限制日志行数，防止内存溢出
        if self.log_console.document().blockCount() > 2000:
            self.log_console.clear()
            self.log_console.append(f'<span style="color:#888;">[System] 日志清理 ({time_str})</span>')

        self.log_console.append(html)

    def _find_row(self, name):
        items = self.table.findItems(name, Qt.MatchExactly)
        if items:
            return items[0].row()
        return None

    def start_all(self):
        self.append_log("System", ">>> 收到全量启动指令...")
        # 按照优先级顺序启动 (实际生产中应配合 wait_for_port 逻辑)
        # 这里简单遍历启动，依赖 ProcessManager 的启动逻辑
        for name, mgr in self.managers.items():
            mgr.start_service()

    def stop_all(self):
        self.append_log("System", ">>> 收到紧急停止指令...")
        for name, mgr in self.managers.items():
            mgr.stop_service()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("A股极速交易系统 - 总控台 (CodeMaster Edition)")
        self.resize(1200, 800)
        self.setWindowIcon(QIcon("resources/app.ico")) # 假设有图标
        
        # 配置文件路径
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(base_dir, "服务定义.yaml")
        
        self.init_ui()
        
        # 延迟 500ms 启动环境自检，确保 UI 先显示
        QTimer.singleShot(500, self.run_startup_check)

    def init_ui(self):
        # 1. 应用全局样式
        app = QApplication.instance()
        app.setStyleSheet(DARK_STYLESHEET)
        
        # 2. 主 Tab 容器
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # 3. 构建子面板
        self.monitor_panel = ServiceMonitorPanel(self.config_path)
        self.config_panel = ConfigEditor(self.config_path)
        
        # 4. 连接 ConfigEditor 的热加载信号 -> MonitorPanel 的重载方法
        self.config_panel.sig_config_reloaded.connect(self.monitor_panel.load_services)

        # 5. 添加 Tabs
        self.tabs.addTab(self.monitor_panel, "📡 服务监控中台")
        self.tabs.addTab(self.config_panel, "⚙️ 服务配置编译")
        
        # 6. 状态栏
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("系统初始化完成。等待指令。")

    def run_startup_check(self):
        """ 启动时运行环境自检 """
        self.monitor_panel.append_log("System", "正在执行启动前环境自检...")
        self.status_bar.showMessage("正在自检环境...")
        
        # 创建自检线程
        self.check_worker = EnvCheckWorker()
        self.check_worker.sig_log.connect(self.on_check_log)
        self.check_worker.sig_finished.connect(self.on_check_finished)
        
        self.check_thread = EnvChecker(self.check_worker)
        self.check_thread.start()

    @Slot(str, bool)
    def on_check_log(self, msg, is_success):
        prefix = "✅" if is_success else "❌"
        self.monitor_panel.append_log("EnvCheck", f"{prefix} {msg}")

    @Slot(bool)
    def on_check_finished(self, all_passed):
        if all_passed:
            self.monitor_panel.append_log("EnvCheck", "环境自检通过。系统准备就绪。")
            self.status_bar.showMessage("环境正常 | 就绪")
            QMessageBox.information(self, "自检通过", "环境检查通过，可以启动服务。")
        else:
            self.monitor_panel.append_log("EnvCheck", "⚠️ 环境自检发现潜在问题，请检查日志。")
            self.status_bar.showMessage("环境警告")
            QMessageBox.warning(self, "环境警告", "部分环境检查未通过，请查看日志详情。")

    def closeEvent(self, event):
        """ 关闭窗口时确认 """
        reply = QMessageBox.question(self, '退出确认', 
                                     "确定要关闭交易系统总控台吗？\n这将停止所有托管的子进程！",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.monitor_panel.stop_all()
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    # 高分屏适配
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    
    app = QApplication(sys.argv)
    
    # 设置默认字体
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
