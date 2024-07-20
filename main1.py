import sys
import subprocess
import uuid
import hashlib

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QGridLayout, QLineEdit


def get_mac_address():
    # 使用uuid获取MAC地址
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 8)][::-1])
    return mac


def get_cpu_serial():
    # Windows系统下获取CPU序列号
    command = "wmic cpu get ProcessorId"
    return subprocess.check_output(command, shell=True).decode().split('\n')[1].strip()


def get_disk_serial():
    # Windows系统下获取硬盘序列号
    command = "wmic diskdrive get SerialNumber"
    return subprocess.check_output(command, shell=True).decode().split('\n')[1].strip()


def get_baseboard_serial():
    # Windows系统下获取主板序列号
    command = "wmic baseboard get SerialNumber"
    return subprocess.check_output(command, shell=True).decode().split('\n')[1].strip()


def generate_fingerprint():
    # 生成机器指纹
    components = [get_mac_address(), get_cpu_serial(), get_disk_serial(), get_baseboard_serial()]
    raw_fingerprint = ''.join(components)
    return hashlib.sha256(raw_fingerprint.encode()).hexdigest()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        # 创建按钮
        self.button = QPushButton('Get Machine Fingerprint', self)
        self.button.clicked.connect(self.on_click)
        grid.addWidget(self.button, 1, 1, 1, 1, Qt.AlignTop)
        # 创建文本框
        self.textEdit = QLineEdit(self)
        self.textEdit.setReadOnly(True)
        grid.addWidget(self.textEdit, 1, 2, 1, 3, Qt.AlignTop)
        # 设置窗口的标题和大小
        self.setWindowTitle('Machine Fingerprint')
        self.setGeometry(300, 300, 580, 50)

    def on_click(self):
        # 获取机器指纹并显示在文本框中
        fingerprint = generate_fingerprint()
        self.textEdit.setText(fingerprint)


def main():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
