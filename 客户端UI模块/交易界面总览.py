# -*- coding: utf-8 -*-
import sys
import json
import redis
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QSplitter,
                             QTextEdit, QGroupBox, QFormLayout, QTabWidget) # 新增 QTabWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt
# 导入我们刚刚编写的性能监控组件
# 假设性能监控组件.py 在同一目录下
from 性能监控组件 import SystemMonitorWidget

# --- 配置区域 ---
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
MARKET_CHANNEL = 'market_tick_channel'
MONITOR_CHANNEL = 'system_monitor_channel' # 新增监控频道

# --- 样式表 (保持 Dark Theme) ---
# ... (样式表与之前相同，这里省略以节省篇幅，实际文件中请保留) ...
DARK_STYLESHEET = """
QMainWindow { background-color: #1e1e1e; color: #ffffff; }
QWidget { background-color: #1e1e1e; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
QTabWidget::pane { border: 1px solid #3e3e3e; }
QTabBar::tab { background: #2d2d2d; color: #aaa; padding: 8px 20px; }
QTabBar::tab:selected { background: #3e3e3e; color: white; border-bottom: 2px solid #007acc; }
/* ... 其他原有样式 ... */
"""

class RedisWorker(QThread):
    market_data_received = pyqtSignal(dict)
    monitor_data_received = pyqtSignal(dict) # 新增信号

    def __init__(self):
        super().__init__()
        self.running = True
        self.pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        self.r = redis.StrictRedis(connection_pool=self.pool)

    def run(self):
        pubsub = self.r.pubsub()
        # 同时订阅行情和监控频道
        pubsub.subscribe(MARKET_CHANNEL, MONITOR_CHANNEL)
        
        while self.running:
            try:
                message = pubsub.get_message(ignore_subscribe_messages=True)
                if message:
                    channel = message['channel']
                    data_str = message['data']
                    try:
                        data = json.loads(data_str)
                        if channel == MARKET_CHANNEL:
                            self.market_data_received.emit(data)
                        elif channel == MONITOR_CHANNEL:
                            self.monitor_data_received.emit(data)
                    except:
                        pass
                time.sleep(0.001)
            except Exception as e:
                print(f"Redis error: {e}")
                time.sleep(1)

    def stop(self):
        self.running = False

class TradingDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XM HFT Terminal - [CodeMaster Edition]")
        self.resize(1400, 900) # 稍微调大一点
        self.setStyleSheet(DARK_STYLESHEET)
        
        self.init_ui()
        self.start_worker()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # === 左侧：行情与下单 (保持不变) ===
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # ... (省略行情表格和下单框代码，与上一版一致) ...
        # 为了演示完整性，我简写占位
        self.market_table = QTableWidget(5, 4)
        left_layout.addWidget(QLabel("实时深度行情"))
        left_layout.addWidget(self.market_table)
        left_layout.addWidget(QPushButton("快速下单面板 (Placeholder)"))

        # === 右侧：增强型信息面板 ===
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # 使用 Tab 页切换日志和监控
        self.info_tabs = QTabWidget()
        
        # Tab 1: 系统日志
        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)
        self.info_tabs.addTab(self.log_viewer, "运行日志 (Logs)")
        
        # Tab 2: 性能监控 (新增!)
        self.monitor_widget = SystemMonitorWidget()
        self.info_tabs.addTab(self.monitor_widget, "性能遥测 (Telemetry)")
        
        right_layout.addWidget(self.info_tabs)

        # 布局分割
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([800, 600]) # 调整比例
        
        main_layout.addWidget(splitter)
        self.statusBar().showMessage("系统就绪 - 等待数据流...")

    def start_worker(self):
        self.worker = RedisWorker()
        self.worker.market_data_received.connect(self.update_market)
        self.worker.monitor_data_received.connect(self.update_monitor) # 连接监控数据
        self.worker.start()

    def update_market(self, data):
        # ... 原有的行情更新逻辑 ...
        pass

    def update_monitor(self, data):
        # 将后端发来的性能数据传递给监控组件
        self.monitor_widget.update_data(data)

    def closeEvent(self, event):
        self.worker.stop()
        self.worker.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradingDashboard()
    window.show()
    sys.exit(app.exec_())