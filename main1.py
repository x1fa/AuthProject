import sys
import cpuinfo
import psutil
import hashlib
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QGridLayout, QLineEdit


def get_cpu_info():
    info = cpuinfo.get_cpu_info()
    return info['brand_raw']  # 获取 CPU 型号作为部分指纹


def get_disk_info():
    # 获取第一个磁盘的设备名
    for disk in psutil.disk_partitions():
        if 'fixed' in disk.opts:
            return disk.device
    return None


def generate_fingerprint():
    # 组合获取的信息生成机器指纹
    cpu_info = get_cpu_info()
    disk_info = get_disk_info()
    text_info = 'douyin'
    if None in (cpu_info, disk_info, text_info):
        raise ValueError("Failed to get all necessary hardware IDs.")

    # 创建原始指纹字符串
    raw_fingerprint = f"{cpu_info} | {disk_info} | {text_info}"
    # 使用 SHA-256 哈希算法生成指纹
    fingerprint = hashlib.sha256(raw_fingerprint.encode()).hexdigest()
    return fingerprint


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
