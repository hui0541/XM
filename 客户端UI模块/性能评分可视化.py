# -*- coding: utf-8 -*-
import sys
import time
import math
import random
from collections import deque
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QApplication, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, QRectF, QPointF, pyqtSignal, QSize
from PyQt5.QtGui import (QPainter, QColor, QPen, QFont, QBrush, 
                         QLinearGradient, QPainterPath, QRadialGradient)

# 颜色定义 (Dark Mode)
COLOR_BG = QColor("#1e1e1e")
COLOR_ACCENT = QColor("#007acc")
COLOR_GOOD = QColor("#4caf50")
COLOR_WARN = QColor("#ff9800")
COLOR_CRIT = QColor("#f44336")
COLOR_TEXT = QColor("#ffffff")

class PerformanceGauge(QWidget):
    """
    高性能绘制的圆形仪表盘，用于显示系统评分 (0-100)
    """
    def __init__(self, title="System Health"):
        super().__init__()
        self.title = title
        self.value = 100.0
        self.setMinimumSize(200, 200)

    def set_value(self, val):
        self.value = max(0.0, min(100.0, val))
        self.update() # 触发重绘

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 坐标变换：中心点为 (0,0)
        side = min(self.width(), self.height())
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        # 1. 绘制背景刻度槽
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(40, 40, 40))
        painter.drawPie(-80, -80, 160, 160, 225 * 16, -270 * 16)

        # 2. 绘制动态进度条 (根据分数变色)
        if self.value > 90: color = COLOR_GOOD
        elif self.value > 60: color = COLOR_WARN
        else: color = COLOR_CRIT
        
        painter.setBrush(color)
        span_angle = -270 * (self.value / 100.0) * 16
        painter.drawPie(-80, -80, 160, 160, 225 * 16, span_angle)

        # 3. 遮罩中心，形成圆环
        painter.setBrush(COLOR_BG)
        painter.drawEllipse(-60, -60, 120, 120)

        # 4. 绘制文字
        painter.setPen(COLOR_TEXT)
        font = QFont("Segoe UI", 24, QFont.Bold)
        painter.setFont(font)
        text = f"{int(self.value)}"
        fm = painter.fontMetrics()
        text_w = fm.width(text)
        painter.drawText(int(-text_w/2), 10, text)

        font.setPointSize(10)
        painter.setFont(font)
        painter.setPen(QColor(150, 150, 150))
        title_w = fm.width(self.title)
        # 简单估算文字居中
        painter.drawText(int(-30), 30, self.title)

class RealTimePlot(QWidget):
    """
    极简高性能时序图，绘制最近 N 个点的时延曲线
    """
    def __init__(self, max_points=100):
        super().__init__()
        self.data = deque([0]*max_points, maxlen=max_points)
        self.max_points = max_points
        self.setStyleSheet("background-color: #252526; border: 1px solid #3e3e3e;")
        self.setMinimumHeight(150)

    def add_point(self, value):
        self.data.append(value)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        # 绘制背景网格
        painter.setPen(QPen(QColor(60, 60, 60), 1, Qt.DotLine))
        painter.drawLine(0, int(h/2), w, int(h/2))

        # 数据归一化 (动态缩放 Y 轴)
        max_val = max(max(self.data), 1.0)
        min_val = 0
        
        # 构建路径
        path = QPainterPath()
        x_step = w / (self.max_points - 1)
        
        points = []
        for i, val in enumerate(self.data):
            x = i * x_step
            # Y轴翻转，0在底部
            if max_val == 0: ratio = 0
            else: ratio = val / max_val
            y = h - (ratio * h * 0.9) - 5 # 留白
            points.append(QPointF(x, y))
        
        if points:
            path.moveTo(points[0])
            for p in points[1:]:
                path.lineTo(p)

            # 绘制填充 (渐变)
            gradient = QLinearGradient(0, 0, 0, h)
            gradient.setColorAt(0, QColor(0, 122, 204, 100)) # 蓝色半透明
            gradient.setColorAt(1, QColor(0, 122, 204, 10))
            
            fill_path = QPainterPath(path)
            fill_path.lineTo(w, h)
            fill_path.lineTo(0, h)
            fill_path.closeSubpath()
            
            painter.fillPath(fill_path, QBrush(gradient))

            # 绘制线条
            painter.setPen(QPen(COLOR_ACCENT, 2))
            painter.drawPath(path)

            # 绘制最新数值标签
            painter.setPen(COLOR_TEXT)
            painter.drawText(w - 50, 20, f"{self.data[-1]:.1f} μs")
            painter.drawText(5, 20, f"Max: {max_val:.0f}")

class ServiceStatusLight(QWidget):
    """
    微服务状态指示灯 (C++, Java, Redis)
    """
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.is_alive = False
        self.setFixedSize(100, 30)
    
    def set_status(self, alive):
        self.is_alive = alive
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        color = COLOR_GOOD if self.is_alive else COLOR_CRIT
        
        # 灯泡
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(5, 10, 10, 10)
        
        # 文字
        painter.setPen(COLOR_TEXT)
        font = painter.font()
        font.setPointSize(9)
        painter.setFont(font)
        painter.drawText(25, 20, self.name)

class SystemMonitorWidget(QWidget):
    """
    性能监控总成面板
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # 模拟数据更新计时器 (实际应连接 Redis 信号)
        self.timer = QTimer()
        self.timer.timeout.connect(self.mock_update)
        self.timer.start(100) # 100ms 刷新一次

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 1. 顶部：健康评分 + 状态灯
        top_panel = QHBoxLayout()
        
        self.gauge = PerformanceGauge("健康评分")
        top_panel.addWidget(self.gauge)
        
        status_layout = QVBoxLayout()
        self.status_md = ServiceStatusLight("MD-Feed (C++)")
        self.status_algo = ServiceStatusLight("Algo-Engine (Py)")
        self.status_oms = ServiceStatusLight("OMS (Java)")
        
        status_layout.addWidget(QLabel("服务状态:"))
        status_layout.addWidget(self.status_md)
        status_layout.addWidget(self.status_algo)
        status_layout.addWidget(self.status_oms)
        status_layout.addStretch()
        
        top_panel.addLayout(status_layout)
        layout.addLayout(top_panel)
        
        # 2. 中部：时延曲线
        layout.addWidget(QLabel("Tick-to-Trade 时延 (微秒)"))
        self.latency_plot = RealTimePlot()
        layout.addWidget(self.latency_plot)
        
        # 3. 底部：资源占用
        layout.addWidget(QLabel("CPU 负载"))
        self.cpu_plot = RealTimePlot() # 复用组件
        layout.addWidget(self.cpu_plot)

    def mock_update(self):
        # 模拟：生成随机波动数据
        # 实际项目中，这里接收 RedisWorker 解析后的数据
        import random
        
        # 模拟时延：正常 200us，偶尔抖动到 800us
        latency = 200 + random.random() * 50
        if random.random() > 0.95: latency += 500
        self.latency_plot.add_point(latency)
        
        # 模拟CPU
        cpu = 10 + random.random() * 5
        self.cpu_plot.add_point(cpu)
        
        # 计算健康分
        score = 100 - (latency / 100) - (cpu / 5)
        self.gauge.set_value(score)
        
        # 模拟状态
        self.status_md.set_status(True)
        self.status_algo.set_status(True)
        self.status_oms.set_status(score > 60)

    def update_data(self, data_dict):
        """
        供外部调用的真实数据更新接口
        data_dict = {'latency': 230, 'cpu': 12, 'services': {'md': True, ...}}
        """
        if 'latency' in data_dict:
            self.latency_plot.add_point(data_dict['latency'])
        if 'score' in data_dict:
            self.gauge.set_value(data_dict['score'])
        # ... 处理其他字段

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SystemMonitorWidget()
    win.setStyleSheet("background-color: #1e1e1e; color: white;")
    win.show()
    sys.exit(app.exec_())