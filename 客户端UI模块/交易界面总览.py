import sys
import random
import datetime
from collections import deque

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QGridLayout, QLabel, QPushButton, 
                               QTableWidget, QTableWidgetItem, QHeaderView, 
                               QFrame, QSplitter, QProgressBar, QLineEdit, QGroupBox)
from PySide6.QtCore import Qt, QTimer, Signal, Slot, QThread
from PySide6.QtGui import QColor, QFont, QPainter, QBrush, QPen

# 全局配色 (Dark Theme)
COLOR_BG = "#121212"
COLOR_PANEL = "#1e1e1e"
COLOR_TEXT = "#e0e0e0"
COLOR_RED = "#ff5252"   # 卖方/下跌
COLOR_GREEN = "#69f0ae" # 买方/上涨
COLOR_BLUE = "#448aff"
COLOR_BORDER = "#333333"

STYLESHEET = f"""
QMainWindow {{ background-color: {COLOR_BG}; color: {COLOR_TEXT}; }}
QWidget {{ background-color: {COLOR_BG}; color: {COLOR_TEXT}; font-family: "Consolas", "Microsoft YaHei"; }}
QFrame {{ background-color: {COLOR_PANEL}; border: 1px solid {COLOR_BORDER}; border-radius: 4px; }}
QLabel {{ border: none; background: transparent; }}
QPushButton {{ background-color: {COLOR_BLUE}; color: white; border: none; padding: 5px; border-radius: 3px; font-weight: bold; }}
QPushButton:hover {{ background-color: #2979ff; }}
QPushButton:pressed {{ background-color: #2962ff; }}
QPushButton#SellBtn {{ background-color: {COLOR_RED}; }}
QPushButton#BuyBtn {{ background-color: {COLOR_GREEN}; color: #000; }}
QTableWidget {{ background-color: {COLOR_PANEL}; gridline-color: {COLOR_BORDER}; border: none; }}
QHeaderView::section {{ background-color: #2c2c2c; padding: 4px; border: none; }}
QTableWidget::item {{ padding: 2px; }}
QLineEdit {{ background-color: #000; border: 1px solid {COLOR_BORDER}; color: {COLOR_GREEN}; padding: 3px; }}
QProgressBar {{ border: 1px solid {COLOR_BORDER}; text-align: center; }}
QProgressBar::chunk {{ background-color: {COLOR_BLUE}; }}
"""

class OrderBookWidget(QWidget):
    """
    高性能自定义绘制：十档行情深度图
    """
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(300)
        self.asks = [(0, 0)] * 10 # Price, Vol
        self.bids = [(0, 0)] * 10
        self.last_price = 0.0

    def update_data(self, asks, bids, last):
        self.asks = asks
        self.bids = bids
        self.last_price = last
        self.update() # 触发重绘

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        
        # 1. 绘制背景
        painter.fillRect(0, 0, w, h, QColor(COLOR_PANEL))
        
        # 2. 计算最大成交量用于缩放条形图
        max_vol = 1
        for _, v in self.asks + self.bids:
            max_vol = max(max_vol, v)
        
        # 3. 绘制中间分割线 (最新价)
        mid_y = h / 2
        painter.setPen(QPen(QColor(COLOR_BORDER), 1, Qt.DashLine))
        painter.drawLine(0, int(mid_y), w, int(mid_y))
        
        # 绘制最新价文字
        painter.setFont(QFont("Consolas", 14, QFont.Bold))
        price_color = QColor(COLOR_RED) if self.asks and self.last_price < self.asks[0][0] else QColor(COLOR_GREEN)
        painter.setPen(price_color)
        painter.drawText(10, int(mid_y - 5), f"{self.last_price:.2f}")

        # 4. 绘制卖盘 (Ask) - 上半部分，从下往上
        row_h = (mid_y - 10) / 10
        for i in range(10):
            if i >= len(self.asks): break
            p, v = self.asks[i]
            y = mid_y - (i + 1) * row_h
            
            # 深度条
            bar_w = (v / max_vol) * (w * 0.4)
            painter.fillRect(int(w - bar_w), int(y), int(bar_w), int(row_h - 2), QColor(COLOR_RED).lighter(120))
            
            # 文字
            painter.setFont(QFont("Consolas", 10))
            painter.setPen(QColor(COLOR_RED))
            painter.drawText(10, int(y + row_h - 2), f"Ask {i+1}")
            painter.setPen(QColor(COLOR_TEXT))
            painter.drawText(60, int(y + row_h - 2), f"{p:.2f}")
            painter.drawText(140, int(y + row_h - 2), f"{v}")

        # 5. 绘制买盘 (Bid) - 下半部分，从上往下
        for i in range(10):
            if i >= len(self.bids): break
            p, v = self.bids[i]
            y = mid_y + i * row_h + 5
            
            # 深度条
            bar_w = (v / max_vol) * (w * 0.4)
            painter.fillRect(int(w - bar_w), int(y), int(bar_w), int(row_h - 2), QColor(COLOR_GREEN).lighter(120))
            
            # 文字
            painter.setFont(QFont("Consolas", 10))
            painter.setPen(QColor(COLOR_GREEN))
            painter.drawText(10, int(y + row_h - 2), f"Bid {i+1}")
            painter.setPen(QColor(COLOR_TEXT))
            painter.drawText(60, int(y + row_h - 2), f"{p:.2f}")
            painter.drawText(140, int(y + row_h - 2), f"{v}")

class TickStreamWidget(QTableWidget):
    """ 逐笔成交明细 """
    def __init__(self):
        super().__init__()
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["时间", "价格", "现量"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
    
    def add_tick(self, time_str, price, vol, direction):
        self.insertRow(0)
        
        c_time = QTableWidgetItem(time_str)
        c_price = QTableWidgetItem(f"{price:.2f}")
        c_vol = QTableWidgetItem(str(vol))
        
        color = QColor(COLOR_RED) if direction < 0 else QColor(COLOR_GREEN)
        if direction == 0: color = QColor(COLOR_TEXT)
        
        for item in [c_time, c_price, c_vol]:
            item.setForeground(color)
            item.setFont(QFont("Consolas", 10))
            
        self.setItem(0, 0, c_time)
        self.setItem(0, 1, c_price)
        self.setItem(0, 2, c_vol)
        
        # 保持只显示最近 50 条
        if self.rowCount() > 50:
            self.removeRow(50)

class StrategyControlPanel(QFrame):
    """ 策略控制面板 """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # 标题
        title = QLabel("🚀 策略引擎控制")
        title.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        title.setStyleSheet("color: #448aff;")
        layout.addWidget(title)
        
        # 状态
        self.status_lbl = QLabel("状态: 等待行情...")
        layout.addWidget(self.status_lbl)
        
        # 按钮组
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("启动策略")
        self.btn_start.clicked.connect(self.toggle_strategy)
        self.btn_stop = QPushButton("停止")
        self.btn_stop.setEnabled(False)
        self.btn_stop.setStyleSheet(f"background-color: {COLOR_PANEL}; border: 1px solid #555;")
        
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
        layout.addLayout(btn_layout)
        
        # 参数表单
        form = QGridLayout()
        form.addWidget(QLabel("交易标的:"), 0, 0)
        self.input_symbol = QLineEdit("sh600000")
        form.addWidget(self.input_symbol, 0, 1)
        
        form.addWidget(QLabel("单笔手数:"), 1, 0)
        self.input_qty = QLineEdit("100")
        form.addWidget(self.input_qty, 1, 1)
        
        form.addWidget(QLabel("止损阈值:"), 2, 0)
        self.input_sl = QLineEdit("-2.0%")
        form.addWidget(self.input_sl, 2, 1)
        
        layout.addLayout(form)
        
        # 信号流
        layout.addWidget(QLabel("📡 实时信号流:"))
        self.signal_log = QTableWidget()
        self.signal_log.setColumnCount(2)
        self.signal_log.setHorizontalHeaderLabels(["时间", "消息"])
        self.signal_log.horizontalHeader().setStretchLastSection(True)
        self.signal_log.verticalHeader().setVisible(False)
        self.signal_log.setShowGrid(False)
        layout.addWidget(self.signal_log)
        
    def log_signal(self, msg):
        row = self.signal_log.rowCount()
        self.signal_log.insertRow(row)
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        self.signal_log.setItem(row, 0, QTableWidgetItem(time_str))
        self.signal_log.setItem(row, 1, QTableWidgetItem(msg))
        self.signal_log.scrollToBottom()

    def toggle_strategy(self):
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.btn_start.setText("运行中...")
        self.btn_start.setStyleSheet(f"background-color: {COLOR_GREEN}; color: black;")
        self.status_lbl.setText("状态: 🔥 监控中")
        self.log_signal("策略引擎已启动，正在监听 UDP...")

class TradingDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("A股极速交易系统 - 交易员终端 (Trader Cockpit)")
        self.resize(1280, 800)
        
        # 应用全局样式
        self.setStyleSheet(STYLESHEET)
        
        # 主布局：左右分割
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(5,5,5,5)
        
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # === 左侧区域：策略控制 (25%) ===
        self.strategy_panel = StrategyControlPanel()
        splitter.addWidget(self.strategy_panel)
        
        # === 中间区域：核心行情 (50%) ===
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0,0,0,0)
        
        # 1. 顶部信息栏
        info_bar = QFrame()
        info_layout = QHBoxLayout(info_bar)
        self.lbl_symbol = QLabel("贵州茅台 (sh600519)")
        self.lbl_symbol.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        self.lbl_change = QLabel("+2.54%  ▲")
        self.lbl_change.setStyleSheet(f"color: {COLOR_GREEN}; font-size: 16px; font-weight: bold;")
        
        info_layout.addWidget(self.lbl_symbol)
        info_layout.addWidget(self.lbl_change)
        info_layout.addStretch()
        center_layout.addWidget(info_bar)
        
        # 2. 盘口深度图
        self.order_book = OrderBookWidget()
        center_layout.addWidget(self.order_book, stretch=2)
        
        # 3. 逐笔成交
        center_layout.addWidget(QLabel("成交明细:"))
        self.tick_stream = TickStreamWidget()
        center_layout.addWidget(self.tick_stream, stretch=1)
        
        splitter.addWidget(center_widget)
        
        # === 右侧区域：账户与订单 (25%) ===
        right_widget = QFrame()
        right_layout = QVBoxLayout(right_widget)
        
        # 资金账户
        right_layout.addWidget(QLabel("💰 资金账户"))
        self.balance_table = QTableWidget(2, 2)
        self.balance_table.verticalHeader().setVisible(False)
        self.balance_table.horizontalHeader().setVisible(False)
        self.balance_table.setItem(0, 0, QTableWidgetItem("可用资金"))
        self.balance_table.setItem(0, 1, QTableWidgetItem("¥ 1,254,000"))
        self.balance_table.setItem(1, 0, QTableWidgetItem("持仓市值"))
        self.balance_table.setItem(1, 1, QTableWidgetItem("¥ 850,000"))
        self.balance_table.setFixedHeight(80)
        right_layout.addWidget(self.balance_table)
        
        # 手动下单区
        order_group = QGroupBox("手动干预")
        order_layout = QGridLayout(order_group)
        self.btn_buy = QPushButton("买入开仓")
        self.btn_buy.setObjectName("BuyBtn")
        self.btn_sell = QPushButton("卖出平仓")
        self.btn_sell.setObjectName("SellBtn")
        order_layout.addWidget(self.btn_buy, 0, 0)
        order_layout.addWidget(self.btn_sell, 0, 1)
        right_layout.addWidget(order_group)

        # 持仓列表
        right_layout.addWidget(QLabel("📦 当前持仓"))
        self.pos_table = QTableWidget()
        self.pos_table.setColumnCount(3)
        self.pos_table.setHorizontalHeaderLabels(["代码", "数量", "盈亏"])
        self.pos_table.verticalHeader().setVisible(False)
        self.pos_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Mock 持仓
        self.pos_table.insertRow(0)
        self.pos_table.setItem(0, 0, QTableWidgetItem("sh600519"))
        self.pos_table.setItem(0, 1, QTableWidgetItem("500"))
        pnl = QTableWidgetItem("+12,500")
        pnl.setForeground(QColor(COLOR_GREEN))
        self.pos_table.setItem(0, 2, pnl)
        right_layout.addWidget(self.pos_table)
        
        splitter.addWidget(right_widget)
        
        # 设置比例
        splitter.setSizes([250, 600, 250])

        # 启动模拟数据生成器 (为了演示)
        self.data_thread = MockDataThread()
        self.data_thread.sig_tick.connect(self.on_tick_update)
        self.data_thread.start()

    @Slot(dict)
    def on_tick_update(self, data):
        """ 收到新行情 """
        # 更新顶部
        self.lbl_symbol.setText(f"{data['symbol']} (Level-2)")
        
        # 更新盘口
        self.order_book.update_data(data['asks'], data['bids'], data['price'])
        
        # 更新 Tick 流
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        self.tick_stream.add_tick(time_str, data['price'], data['last_vol'], data['dir'])
        
        # 随机触发策略信号
        if random.random() < 0.05:
            self.strategy_panel.log_signal(f"检测到大单买入: {data['last_vol']}手")

class MockDataThread(QThread):
    """ 模拟数据源 (替代 Redis/UDP，确保 UI 可运行) """
    sig_tick = Signal(dict)
    
    def run(self):
        price = 100.0
        while True:
            # 随机漫步
            change = random.uniform(-0.1, 0.1)
            price += change
            
            # 生成 10 档盘口
            asks = [(price + 0.01 * i, random.randint(10, 500)) for i in range(1, 11)]
            bids = [(price - 0.01 * i, random.randint(10, 500)) for i in range(1, 11)]
            
            data = {
                "symbol": "sh600519",
                "price": price,
                "asks": asks,
                "bids": bids,
                "last_vol": random.randint(1, 50),
                "dir": 1 if change > 0 else -1
            }
            
            self.sig_tick.emit(data)
            self.msleep(200) # 200ms 刷新率 (5Hz)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)
    
    window = TradingDashboard()
    window.show()
    sys.exit(app.exec())