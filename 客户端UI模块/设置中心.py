import sys
import os
import json
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                               QTabWidget, QLabel, QLineEdit, QFormLayout, 
                               QPushButton, QCheckBox, QComboBox, QGroupBox, 
                               QMessageBox, QScrollArea)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

# 复用全局样式
STYLESHEET = """
QWidget { background-color: #1e1e1e; color: #e0e0e0; font-family: "Microsoft YaHei"; }
QLineEdit { background-color: #252526; border: 1px solid #3e3e42; padding: 5px; color: #fff; }
QLineEdit:focus { border: 1px solid #007acc; }
QGroupBox { border: 1px solid #3e3e42; margin-top: 10px; font-weight: bold; }
QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; color: #007acc; }
QTabWidget::pane { border: 1px solid #3e3e42; }
QTabBar::tab { background: #2d2d30; padding: 8px 20px; color: #aaa; }
QTabBar::tab:selected { background: #1e1e1e; color: #fff; border-top: 2px solid #007acc; }
QPushButton { background-color: #0e639c; color: white; border: none; padding: 8px 15px; border-radius: 4px; }
QPushButton:hover { background-color: #1177bb; }
QPushButton#CancelBtn { background-color: #3e3e42; }
QPushButton#CancelBtn:hover { background-color: #4e4e52; }
QComboBox { background-color: #252526; border: 1px solid #3e3e42; padding: 5px; }
"""

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("系统设置中心 - Configuration Hub")
        self.resize(800, 600)
        self.setStyleSheet(STYLESHEET)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        
        # 顶部标题
        header = QLabel("⚙️ 全局参数配置")
        header.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        header.setStyleSheet("color: #007acc; margin-bottom: 10px;")
        main_layout.addWidget(header)
        
        # Tab 容器
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # 添加各个配置页签
        self.init_connection_tab()
        self.init_risk_tab()
        self.init_database_tab()
        self.init_cloud_tab()
        
        # 底部按钮区
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_reset = QPushButton("重置默认")
        self.btn_reset.setObjectName("CancelBtn")
        self.btn_reset.clicked.connect(self.load_defaults)
        
        self.btn_save = QPushButton("保存并应用")
        self.btn_save.clicked.connect(self.save_config)
        self.btn_save.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        
        btn_layout.addWidget(self.btn_reset)
        btn_layout.addWidget(self.btn_save)
        main_layout.addLayout(btn_layout)

    def init_connection_tab(self):
        """ 连接与接口设置 """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # C++ 行情网关
        grp_market = QGroupBox("C++ 极速行情网关")
        form_market = QFormLayout()
        self.udp_port = QLineEdit("9999")
        self.udp_port.setPlaceholderText("UDP Broadcast Port")
        self.tcp_source = QLineEdit("tcp://127.0.0.1:8888")
        form_market.addRow("本地监听端口 (UDP):", self.udp_port)
        form_market.addRow("上游行情源 (TCP):", self.tcp_source)
        grp_market.setLayout(form_market)
        layout.addWidget(grp_market)
        
        # Java 交易网关
        grp_trade = QGroupBox("Java 交易执行网关")
        form_trade = QFormLayout()
        self.trade_ip = QLineEdit("127.0.0.1")
        self.trade_port = QLineEdit("8888")
        self.broker_account = QLineEdit("SIM_888888")
        self.broker_pwd = QLineEdit()
        self.broker_pwd.setEchoMode(QLineEdit.Password)
        self.broker_pwd.setPlaceholderText("不修改请留空")
        
        form_trade.addRow("网关 IP:", self.trade_ip)
        form_trade.addRow("指令监听端口:", self.trade_port)
        form_trade.addRow("券商资金账号:", self.broker_account)
        form_trade.addRow("交易密码:", self.broker_pwd)
        grp_trade.setLayout(form_trade)
        layout.addWidget(grp_trade)
        
        layout.addStretch()
        self.tabs.addTab(tab, "🔌 接口连接")

    def init_risk_tab(self):
        """ 策略与风控设置 """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 资金风控
        grp_fund = QGroupBox("资金安全闸")
        form_fund = QFormLayout()
        self.max_pos_value = QLineEdit("1000000")
        self.single_order_limit = QLineEdit("50000")
        self.daily_loss_limit = QLineEdit("20000")
        
        form_fund.addRow("最大持仓市值 (CNY):", self.max_pos_value)
        form_fund.addRow("单笔最大委托 (CNY):", self.single_order_limit)
        form_fund.addRow("单日最大亏损 (CNY):", self.daily_loss_limit)
        grp_fund.setLayout(form_fund)
        layout.addWidget(grp_fund)
        
        # 策略行为
        grp_behavior = QGroupBox("策略行为控制")
        form_beh = QFormLayout()
        
        self.chk_allow_short = QCheckBox("允许裸卖空 (需融券权限)")
        self.chk_algo_trading = QCheckBox("启用算法拆单 (TWAP/VWAP)")
        self.chk_future_check = QCheckBox("启用未来函数实时检测 (Proxy)")
        self.chk_future_check.setChecked(True)
        
        form_beh.addRow(self.chk_allow_short)
        form_beh.addRow(self.chk_algo_trading)
        form_beh.addRow(self.chk_future_check)
        grp_behavior.setLayout(form_beh)
        layout.addWidget(grp_behavior)
        
        layout.addStretch()
        self.tabs.addTab(tab, "🛡️ 策略风控")

    def init_database_tab(self):
        """ 数据库配置 """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Redis
        grp_redis = QGroupBox("Redis (热数据缓存)")
        form_redis = QFormLayout()
        self.redis_host = QLineEdit("127.0.0.1")
        self.redis_port = QLineEdit("6379")
        self.redis_auth = QLineEdit()
        self.redis_auth.setEchoMode(QLineEdit.Password)
        
        form_redis.addRow("Host:", self.redis_host)
        form_redis.addRow("Port:", self.redis_port)
        form_redis.addRow("Password:", self.redis_auth)
        grp_redis.setLayout(form_redis)
        layout.addWidget(grp_redis)
        
        # ClickHouse
        grp_ch = QGroupBox("ClickHouse (历史行情存储)")
        form_ch = QFormLayout()
        self.ch_url = QLineEdit("jdbc:clickhouse://127.0.0.1:8123/speed_trader")
        self.ch_user = QLineEdit("default")
        self.ch_pwd = QLineEdit()
        self.ch_pwd.setEchoMode(QLineEdit.Password)
        
        form_ch.addRow("JDBC URL:", self.ch_url)
        form_ch.addRow("Username:", self.ch_user)
        form_ch.addRow("Password:", self.ch_pwd)
        grp_ch.setLayout(form_ch)
        layout.addWidget(grp_ch)
        
        layout.addStretch()
        self.tabs.addTab(tab, "💾 数据存储")

    def init_cloud_tab(self):
        """ AI 与云服务 """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        grp_bos = QGroupBox("百度智能云 BOS (模型/日志归档)")
        form_bos = QFormLayout()
        self.bos_endpoint = QLineEdit("bj.bcebos.com")
        self.bos_ak = QLineEdit()
        self.bos_sk = QLineEdit()
        self.bos_sk.setEchoMode(QLineEdit.Password)
        self.bos_bucket = QLineEdit("speed-trader-models")
        
        form_bos.addRow("Endpoint:", self.bos_endpoint)
        form_bos.addRow("Access Key:", self.bos_ak)
        form_bos.addRow("Secret Key:", self.bos_sk)
        form_bos.addRow("Bucket Name:", self.bos_bucket)
        grp_bos.setLayout(form_bos)
        layout.addWidget(grp_bos)
        
        grp_model = QGroupBox("AI 模型加载")
        form_model = QFormLayout()
        self.model_path = QLineEdit("./models/xgb_v1.model")
        self.btn_select_model = QPushButton("选择文件...")
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.model_path)
        h_layout.addWidget(self.btn_select_model)
        
        form_model.addRow("当前模型路径:", h_layout)
        grp_model.setLayout(form_model)
        layout.addWidget(grp_model)
        
        layout.addStretch()
        self.tabs.addTab(tab, "☁️ AI 云服务")

    def load_defaults(self):
        """ 加载默认设置 """
        reply = QMessageBox.question(self, "确认", "确定要重置所有设置为默认值吗？", 
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 仅演示恢复部分字段
            self.udp_port.setText("9999")
            self.redis_host.setText("127.0.0.1")
            self.max_pos_value.setText("1000000")
            QMessageBox.information(self, "提示", "已恢复默认设置")

    def save_config(self):
        """ 收集数据并保存 """
        # 简单校验
        if not self.udp_port.text().isdigit():
            QMessageBox.critical(self, "错误", "UDP 端口必须是数字！")
            return
            
        config_data = {
            "market": {
                "udp_port": int(self.udp_port.text()),
                "source": self.tcp_source.text()
            },
            "trade": {
                "ip": self.trade_ip.text(),
                "port": int(self.trade_port.text()),
                "account": self.broker_account.text()
            },
            "risk": {
                "max_position": float(self.max_pos_value.text()),
                "check_future": self.chk_future_check.isChecked()
            }
            # ... 其他字段省略
        }
        
        # 模拟保存到文件
        try:
            with open("config_user_settings.json", "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "成功", "配置已保存并生效！\n(部分网络设置可能需要重启服务)")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "保存失败", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SettingsWindow()
    win.show()
    sys.exit(app.exec())