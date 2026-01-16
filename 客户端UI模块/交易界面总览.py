# -*- coding: utf-8 -*-
import sys
import json
import redis
import time
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QSplitter,
                             QTextEdit, QGroupBox, QFormLayout, QTabWidget)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QColor, QFont

# === 关键修改：引入新的性能可视化模块 ===
try:
    from 性能评分可视化 import PerformanceVisualizer
except ImportError:
    print("[Warning] 性能评分可视化.py 未找到，使用空白占位符")
    class PerformanceVisualizer(QWidget):
        def update_data(self, d): pass
# ======================================

# --- 配置 ---
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
MARKET_CHANNEL = 'market_tick_channel'

class RedisWorker(QThread):
    market_signal = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.running = True
        try:
            self.pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
            self.r = redis.StrictRedis(connection_pool=self.pool)
        except Exception as e:
            print(f"Redis Init Error: {e}")

    def run(self):
        if not hasattr(self, 'r'): return
        pubsub = self.r.pubsub()
        pubsub.subscribe(MARKET_CHANNEL)
        
        while self.running:
            try:
                msg = pubsub.get_message(ignore_subscribe_messages=True)
                if msg and msg['type'] == 'message':
                    try:
                        data = json.loads(msg['data'])
                        self.market_signal.emit(data)
                    except:
                        pass
                time.sleep(0.001) 
            except Exception:
                time.sleep(1)

    def stop(self):
        self.running = False

class TradingDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XM HFT Terminal - [CodeMaster Edition]")
        self.resize(1400, 900)
        self.apply_dark_theme()
        
        self.init_ui()
        
        # 启动 Redis 监听
        self.worker = RedisWorker()
        self.worker.market_signal.connect(self.on_market_data)
        self.worker.start()
        
        # 模拟性能遥测数据 (实际应从 C++ 后端获取)
        self.telemetry_timer = self.startTimer(100) # 100ms 刷新

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; color: #ffffff; }
            QWidget { background-color: #1e1e1e; color: #cccccc; font-family: 'Segoe UI'; font-size: 14px; }
            QGroupBox { border: 1px solid #333; margin-top: 10px; padding-top: 15px; font-weight: bold; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; color: #007acc; }
            QTableWidget { background-color: #252526; gridline-color: #333; border: none; }
            QHeaderView::section { background-color: #333; padding: 4px; border: none; color: #aaa; }
            QLineEdit { background-color: #333; border: 1px solid #444; padding: 5px; color: white; }
            QPushButton { background-color: #0e639c; padding: 8px; border: none; color: white; }
            QPushButton:hover { background-color: #1177bb; }
            QTabWidget::pane { border: 1px solid #333; }
            QTabBar::tab { background: #2d2d2d; padding: 8px 20px; color: #aaa; }
            QTabBar::tab:selected { background: #3e3e3e; border-top: 2px solid #007acc; color: white; }
        """)

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        
        # === 左侧面板：行情与交易 ===
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0,0,0,0)
        
        # 行情表
        self.quote_table = QTableWidget(0, 5)
        self.quote_table.setHorizontalHeaderLabels(["Symbol", "Price", "Vol", "Bid", "Ask"])
        self.quote_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.quote_table.verticalHeader().setVisible(False)
        left_layout.addWidget(self.quote_table)
        
        # 下单区
        order_box = QGroupBox("极速下单 (Fast Order)")
        form = QFormLayout(order_box)
        form.addRow("代码:", QLineEdit("BTC-USDT"))
        form.addRow("价格:", QLineEdit())
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(QPushButton("买入"))
        btn_layout.addWidget(QPushButton("卖出"))
        form.addRow(btn_layout)
        left_layout.addWidget(order_box)
        
        # === 右侧面板：性能与日志 ===
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0,0,0,0)
        
        tabs = QTabWidget()
        
        # 1. 性能可视化 Tab
        self.perf_viz = PerformanceVisualizer()
        tabs.addTab(self.perf_viz, "性能评分 (Health)")
        
        # 2. 系统日志 Tab
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        tabs.addTab(self.log_text, "系统日志 (Logs)")
        
        right_layout.addWidget(tabs)
        
        # 分割比例
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([800, 600])
        
        layout.addWidget(splitter)
        self.statusBar().showMessage("Ready.")

    def on_market_data(self, data):
        # 收到行情数据，更新表格
        sym = data.get('symbol', 'N/A')
        # ... (此处省略表格更新逻辑，与之前相同) ...
        # 简单演示：
        self.statusBar().showMessage(f"Last Tick: {sym} @ {data.get('last_price')}")

    def timerEvent(self, event):
        # 生成模拟数据以驱动性能仪表盘
        # 实际项目中，这些数据应来自 Redis 的 'system_monitor' 频道
        latency = 20 + random.random() * 30 # 20-50ms 波动
        if random.random() > 0.9: latency += 40 # 偶发抖动
        
        cpu_usage = 15 + random.random() * 5
        
        # 评分算法：基础分100，每增加1ms时延扣0.5分
        score = max(0, 100 - (latency - 10) * 0.8)
        
        self.perf_viz.update_data({
            'latency': latency,
            'cpu': cpu_usage,
            'score': score
        })

    def closeEvent(self, event):
        self.worker.stop()
        self.worker.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TradingDashboard()
    win.show()
    sys.exit(app.exec_())