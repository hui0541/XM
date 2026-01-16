# -*- coding: utf-8 -*-
import math
from collections import deque
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QPointF, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QBrush, QLinearGradient, QPainterPath, QRadialGradient

# --- 视觉风格定义 ---
COLOR_BG = QColor("#1e1e1e")
COLOR_TEXT = QColor("#ffffff")
COLOR_SCORE_HIGH = QColor("#00ff00") # 绿色
COLOR_SCORE_MED = QColor("#ffaa00")  # 橙色
COLOR_SCORE_LOW = QColor("#ff0000")  # 红色
COLOR_GRID = QColor("#3e3e3e")

class ScoreGauge(QWidget):
    """
    高性能性能评分仪表盘
    """
    def __init__(self, size=200):
        super().__init__()
        self.setMinimumSize(size, size)
        self.score = 100.0
        self.target_score = 100.0
        
        # 动画平滑定时器
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self._animate)
        self.anim_timer.start(16) # ~60 FPS

    def set_score(self, val):
        self.target_score = max(0.0, min(100.0, float(val)))

    def _animate(self):
        diff = self.target_score - self.score
        if abs(diff) > 0.1:
            self.score += diff * 0.1 # 缓动系数
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w, h = self.width(), self.height()
        center = QPointF(w/2, h/2)
        radius = min(w, h) / 2 - 10

        # 1. 绘制背景轨道 (270度弧)
        painter.setPen(QPen(QColor(50, 50, 50), 15, Qt.SolidLine, Qt.RoundCap))
        start_angle = 135 * 16
        span_angle = -270 * 16
        path_rect = (center.x()-radius, center.y()-radius, radius*2, radius*2)
        painter.drawArc(*path_rect, start_angle, span_angle)

        # 2. 绘制分数进度条
        if self.score > 80: color = COLOR_SCORE_HIGH
        elif self.score > 50: color = COLOR_SCORE_MED
        else: color = COLOR_SCORE_LOW
        
        painter.setPen(QPen(color, 15, Qt.SolidLine, Qt.RoundCap))
        score_span = -270 * (self.score / 100.0) * 16
        painter.drawArc(*path_rect, start_angle, int(score_span))

        # 3. 绘制中心文字
        painter.setPen(COLOR_TEXT)
        painter.setFont(QFont("Segoe UI", 36, QFont.Bold))
        text = f"{int(self.score)}"
        fm = painter.fontMetrics()
        tw = fm.width(text)
        painter.drawText(int(center.x() - tw/2), int(center.y() + 10), text)
        
        painter.setFont(QFont("Segoe UI", 10))
        painter.setPen(QColor("#aaaaaa"))
        sub_text = "系统评分"
        stw = fm.width(sub_text)
        painter.drawText(int(center.x() - stw/2), int(center.y() + 35), sub_text)

class LatencyChart(QWidget):
    """
    极简时延折线图
    """
    def __init__(self):
        super().__init__()
        self.data = deque([0]*100, maxlen=100)
        self.setMinimumHeight(100)
        self.setStyleSheet("background-color: #252526; border-radius: 5px;")

    def add_point(self, val):
        self.data.append(val)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        
        # 网格
        painter.setPen(QPen(COLOR_GRID, 1, Qt.DotLine))
        painter.drawLine(0, h//2, w, h//2)

        if not self.data: return

        # 归一化
        max_val = max(max(self.data), 10.0) # 至少显示10ms刻度
        points = []
        x_step = w / (len(self.data) - 1) if len(self.data) > 1 else 0
        
        path = QPainterPath()
        for i, val in enumerate(self.data):
            x = i * x_step
            y = h - (val / max_val * h * 0.9) - 5
            pt = QPointF(x, y)
            points.append(pt)
            if i == 0: path.moveTo(pt)
            else: path.lineTo(pt)
        
        # 填充
        fill_path = QPainterPath(path)
        fill_path.lineTo(w, h)
        fill_path.lineTo(0, h)
        fill_path.closeSubpath()
        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0, QColor(0, 122, 204, 100))
        grad.setColorAt(1, QColor(0, 122, 204, 10))
        painter.fillPath(fill_path, QBrush(grad))
        
        # 描边
        painter.setPen(QPen(QColor("#007acc"), 2))
        painter.drawPath(path)
        
        # 显示最新值
        painter.setPen(COLOR_TEXT)
        painter.setFont(QFont("Consolas", 9))
        painter.drawText(5, 15, f"Latency: {self.data[-1]:.1f}ms")

class PerformanceVisualizer(QWidget):
    """
    性能可视化总成：结合仪表盘和图表
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 左侧：大仪表盘
        self.gauge = ScoreGauge()
        layout.addWidget(self.gauge)
        
        # 右侧：详细指标图表区
        right_panel = QWidget()
        v_layout = QVBoxLayout(right_panel)
        v_layout.setContentsMargins(0, 0, 0, 0)
        
        self.lat_chart = LatencyChart()
        v_layout.addWidget(QLabel("核心穿透时延 (Tick-to-Trade)"))
        v_layout.addWidget(self.lat_chart)
        
        v_layout.addStretch()
        
        # 底部状态指标
        stats_layout = QHBoxLayout()
        self.lbl_cpu = QLabel("CPU: 0%")
        self.lbl_mem = QLabel("MEM: 0MB")
        stats_layout.addWidget(self.lbl_cpu)
        stats_layout.addWidget(self.lbl_mem)
        v_layout.addLayout(stats_layout)
        
        layout.addWidget(right_panel)

    def update_data(self, data):
        """
        接收数据并更新 UI
        data: {'latency': float, 'cpu': float, 'mem': float, 'score': float}
        """
        if 'latency' in data:
            self.lat_chart.add_point(data['latency'])
        
        if 'score' in data:
            self.gauge.set_score(data['score'])
        else:
            # 简单的自动评分逻辑：时延越低分越高
            lat = data.get('latency', 0)
            auto_score = max(0, 100 - lat / 2) # 假设 200ms 时延为 0 分
            self.gauge.set_score(auto_score)

        if 'cpu' in data:
            self.lbl_cpu.setText(f"CPU: {data['cpu']:.1f}%")