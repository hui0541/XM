# -*- coding: utf-8 -*-
import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QTabWidget, QSpinBox, 
                             QDoubleSpinBox, QPushButton, QMessageBox, QCheckBox)
from PyQt5.QtGui import QIcon, QFont

# 模拟配置文件路径
CONFIG_FILE = "trading_config.json"

class SettingsCenter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("设置中心 - System Configuration")
        self.resize(500, 400)
        self.setStyleSheet("""
            QWidget { background-color: #2d2d2d; color: #cccccc; font-size: 14px; }
            QLineEdit, QSpinBox, QDoubleSpinBox { background-color: #1e1e1e; border: 1px solid #555; padding: 4px; color: white; }
            QTabWidget::pane { border: 1px solid #444; }
            QTabBar::tab { background: #333; padding: 8px 20px; color: #aaa; }
            QTabBar::tab:selected { background: #444; color: white; border-bottom: 2px solid #007acc; }
            QPushButton { background-color: #0e639c; color: white; padding: 8px; border: none; }
            QPushButton:hover { background-color: #1177bb; }
        """)
        
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_connection_tab(), "连接设置")
        self.tabs.addTab(self.create_risk_tab(), "风控参数")
        self.tabs.addTab(self.create_strategy_tab(), "策略开关")
        
        layout.addWidget(self.tabs)
        
        # 底部按钮
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("保存配置 (Save)")
        btn_save.clicked.connect(self.save_settings)
        btn_cancel = QPushButton("取消 (Cancel)")
        btn_cancel.setStyleSheet("background-color: #555;")
        btn_cancel.clicked.connect(self.close)
        
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def create_connection_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Redis Host:"))
        self.redis_host = QLineEdit("localhost")
        layout.addWidget(self.redis_host)
        
        layout.addWidget(QLabel("Redis Port:"))
        self.redis_port = QSpinBox()
        self.redis_port.setRange(1, 65535)
        self.redis_port.setValue(6379)
        layout.addWidget(self.redis_port)

        layout.addWidget(QLabel("ClickHouse Host:"))
        self.ch_host = QLineEdit("localhost")
        layout.addWidget(self.ch_host)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_risk_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("单笔最大下单量 (Max Qty):"))
        self.max_order_qty = QDoubleSpinBox()
        self.max_order_qty.setRange(0.01, 1000.0)
        self.max_order_qty.setValue(10.0)
        layout.addWidget(self.max_order_qty)
        
        layout.addWidget(QLabel("日内最大亏损限额 ($):"))
        self.max_daily_loss = QSpinBox()
        self.max_daily_loss.setRange(0, 1000000)
        self.max_daily_loss.setValue(5000)
        layout.addWidget(self.max_daily_loss)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_strategy_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.cb_algo1 = QCheckBox("启用双均线策略 (MA Cross)")
        self.cb_algo2 = QCheckBox("启用网格交易 (Grid Trading)")
        self.cb_algo3 = QCheckBox("启用高频做市 (HFT Market Making)")
        
        layout.addWidget(self.cb_algo1)
        layout.addWidget(self.cb_algo2)
        layout.addWidget(self.cb_algo3)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def load_settings(self):
        """从 JSON 加载设置，模拟生产环境"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.redis_host.setText(data.get('redis_host', 'localhost'))
                    self.redis_port.setValue(data.get('redis_port', 6379))
                    self.max_order_qty.setValue(data.get('max_qty', 1.0))
            except Exception as e:
                print(f"Loading config failed: {e}")

    def save_settings(self):
        """保存设置到 JSON，并可能通知 Redis"""
        data = {
            'redis_host': self.redis_host.text(),
            'redis_port': self.redis_port.value(),
            'ch_host': self.ch_host.text(),
            'max_qty': self.max_order_qty.value(),
            'max_loss': self.max_daily_loss.value(),
            'strategies': {
                'ma_cross': self.cb_algo1.isChecked(),
                'grid': self.cb_algo2.isChecked(),
                'hft': self.cb_algo3.isChecked()
            }
        }
        
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            QMessageBox.information(self, "成功", "配置已保存，请重启服务以生效。")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsCenter()
    window.show()
    sys.exit(app.exec_())