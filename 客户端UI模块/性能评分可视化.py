import sys
import random
from collections import deque
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QFrame)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient, QFont

class LatencyChart(QWidget):
    """ 实时延迟曲线图 """
    def __init__(self):
        super().__init__()
        self.data = deque([0]*100, maxlen=100)
        self.setMinimumHeight(200)
        self.setStyleSheet("background-color: #1e1e1e;")

    def add_point(self, latency_ms):
        self.data.append(latency_ms)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        
        # 背景网格
        painter.setPen(QPen(QColor("#333"), 1, Qt.DotLine))
        for i in range(0, h, 40):
            painter.drawLine(0, i, w, i)

        # 绘制曲线
        path_pen = QPen(QColor("#00bcd4"), 2)
        painter.setPen(path_pen)
        
        # 找到最大值用于归一化
        max_val = max(max(self.data), 10) # 最小10ms刻度
        step_x = w / (len(self.data) - 1)
        
        points = []
        for i, val in enumerate(self.data):
            x = i * step_x
            y = h - (val / max_val) * (h - 20) # 留底边
            points.append((x, y))
            
        for i in range(len(points) - 1):
            painter.drawLine(int(points[i][0]), int(points[i][1]), 
                             int(points[i+1][0]), int(points[i+1][1]))
            
        # 显示当前延迟
        curr = self.data[-1]
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        color = QColor("#00ff00") if curr < 5 else QColor("#ff0000")
        painter.setPen(color)
        painter.drawText(w - 100, 30, f"{curr:.2f} ms")

class PerformanceMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("系统性能监控 - Latency Watchdog")
        self.resize(600, 400)
        self.setStyleSheet("background-color: #121212; color: #fff;")
        
        layout = QVBoxLayout(self)
        
        # 标题栏
        title_box = QHBoxLayout()
        lbl = QLabel("🌩️ 全链路延迟监控")
        lbl.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        title_box.addWidget(lbl)
        
        self.score_lbl = QLabel("评分: 98.5")
        self.score_lbl.setStyleSheet("color: #00ff00; font-size: 14px;")
        title_box.addStretch()
        title_box.addWidget(self.score_lbl)
        
        layout.addLayout(title_box)
        
        # 曲线图
        self.chart = LatencyChart()
        layout.addWidget(self.chart)
        
        # 统计面板
        stats_frame = QFrame()
        stats_frame.setStyleSheet("background-color: #1e1e1e; border-radius: 5px;")
        stats_layout = QHBoxLayout(stats_frame)
        
        self.lbl_avg = QLabel("平均: 0.00 ms")
        self.lbl_p99 = QLabel("P99: 0.00 ms")
        self.lbl_jitter = QLabel("抖动: 0.00 ms")
        
        for l in [self.lbl_avg, self.lbl_p99, self.lbl_jitter]:
            l.setStyleSheet("color: #aaa; font-size: 12px;")
            stats_layout.addWidget(l)
            
        layout.addWidget(stats_frame)
        
        # 模拟数据定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100) # 100ms 更新一次

    def update_data(self):
        # 模拟：大部分在 1-3ms，偶尔跳到 10ms
        base = random.uniform(1.0, 3.0)
        if random.random() > 0.95:
            base += random.uniform(5.0, 10.0)
            
        self.chart.add_point(base)
        
        # 更新统计
        data = list(self.chart.data)
        avg = sum(data) / len(data)
        data.sort()
        p99 = data[int(len(data) * 0.99)]
        
        self.lbl_avg.setText(f"平均: {avg:.2f} ms")
        self.lbl_p99.setText(f"P99: {p99:.2f} ms")
        
        # 评分逻辑
        score = 100 - avg * 2
        self.score_lbl.setText(f"系统健康分: {score:.1f}")
        if score < 80:
            self.score_lbl.setStyleSheet("color: #ff5252; font-size: 14px;")
        else:
            self.score_lbl.setStyleSheet("color: #69f0ae; font-size: 14px;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PerformanceMonitor()
    win.show()
    sys.exit(app.exec())