import yaml
import os
import socket
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                               QPushButton, QMessageBox, QLabel, QSplitter, QListWidget)
from PySide6.QtGui import QFont, QColor, QSyntaxHighlighter, QTextCharFormat
from PySide6.QtCore import Signal

class ConfigSchemaValidator:
    """
    配置编译器/校验器
    负责将 YAML 文本 '编译' 为可信的配置对象，并抛出具体的语法或逻辑错误
    """
    @staticmethod
    def validate(yaml_content, base_dir):
        errors = []
        try:
            config = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            return False, [f"YAML 语法解析错误: {e}"]

        if not isinstance(config, dict) or 'services' not in config:
            return False, ["根节点必须包含 'services' 列表"]

        used_ports = {}
        used_names = set()

        for idx, svc in enumerate(config['services']):
            # 1. 必填字段检查
            if 'name' not in svc:
                errors.append(f"第 {idx+1} 项服务缺少 'name' 字段")
                continue
            name = svc['name']
            
            if name in used_names:
                errors.append(f"服务名称重复: {name}")
            used_names.add(name)

            if 'command' not in svc:
                errors.append(f"服务 '{name}' 缺少 'command' 启动命令")

            # 2. 路径有效性检查 (编译期检查)
            if 'work_dir' in svc:
                # 转换为绝对路径进行检查
                full_path = os.path.normpath(os.path.join(base_dir, svc['work_dir']))
                if not os.path.exists(full_path):
                    errors.append(f"服务 '{name}' 的工作目录不存在: {svc['work_dir']}")

            # 3. 端口冲突检查
            if 'health_check' in svc and svc['health_check'].get('type') == 'tcp':
                port = svc['health_check'].get('port')
                if not isinstance(port, int):
                    errors.append(f"服务 '{name}' 的端口必须是整数")
                elif port in used_ports:
                    prev_svc = used_ports[port]
                    errors.append(f"端口冲突: 服务 '{name}' 与 '{prev_svc}' 同时使用了端口 {port}")
                else:
                    used_ports[port] = name

        return (len(errors) == 0), errors

class ConfigEditor(QWidget):
    sig_config_reloaded = Signal() # 热加载信号

    def __init__(self, config_path):
        super().__init__()
        self.config_path = config_path
        self.setup_ui()
        self.load_file()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # 顶部操作栏
        toolbar = QHBoxLayout()
        self.lbl_status = QLabel("Ready")
        self.btn_check = QPushButton("🔍 编译校验")
        self.btn_check.clicked.connect(self.compile_check)
        self.btn_save = QPushButton("💾 保存并热更")
        self.btn_save.clicked.connect(self.save_and_reload)
        self.btn_save.setStyleSheet("background-color: #2da44e; color: white; font-weight: bold;")
        
        toolbar.addWidget(QLabel("配置文件源: "))
        toolbar.addWidget(self.lbl_status)
        toolbar.addStretch()
        toolbar.addWidget(self.btn_check)
        toolbar.addWidget(self.btn_save)
        layout.addLayout(toolbar)

        # 编辑器主体
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 11))
        self.editor.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; border: 1px solid #444;")
        layout.addWidget(self.editor)

        # 错误输出控制台
        self.console = QListWidget()
        self.console.setMaximumHeight(100)
        self.console.setStyleSheet("background-color: #000; color: #ff5555; font-family: Consolas;")
        layout.addWidget(self.console)

    def load_file(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.editor.setPlainText(f.read())

    def compile_check(self):
        """ 执行静态编译/校验 """
        self.console.clear()
        content = self.editor.toPlainText()
        base_dir = os.path.dirname(self.config_path)
        
        is_valid, errors = ConfigSchemaValidator.validate(content, base_dir)
        
        if is_valid:
            self.console.setStyleSheet("background-color: #000; color: #55ff55;")
            self.console.addItem("✅ 编译成功: 配置格式正确，无逻辑冲突。")
            self.lbl_status.setText("Pass")
            return True
        else:
            self.console.setStyleSheet("background-color: #000; color: #ff5555;")
            self.console.addItem(f"❌ 编译失败，发现 {len(errors)} 个错误:")
            for err in errors:
                self.console.addItem(f"  - {err}")
            self.lbl_status.setText("Error")
            return False

    def save_and_reload(self):
        if not self.compile_check():
            QMessageBox.warning(self, "校验失败", "配置存在错误，禁止保存。请查看下方控制台。")
            return

        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
            
            QMessageBox.information(self, "成功", "配置已保存！\n系统正在尝试热重载...")
            self.sig_config_reloaded.emit() # 触发外部热加载
            
        except Exception as e:
            QMessageBox.critical(self, "保存失败", str(e))