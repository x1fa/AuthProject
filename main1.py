import subprocess
import sys
import cpuinfo
import psutil
import hashlib
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QGridLayout, QLineEdit


def get_cpu_id():
    # 使用 subprocess 来调用 wmic 命令
    cmd = 'wmic cpu get ProcessorId'
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True,
                               creationflags=subprocess.CREATE_NO_WINDOW)
    out, err = process.communicate()
    if process.returncode == 0:
        # 解析输出结果
        # WMIC 输出格式通常包括标题行和实际数据行，我们需要解析实际的数据行
        output = out.decode().strip().split('\n')
        # 第一行通常是标题，第二行是数据
        if len(output) > 1:
            return output[1].strip()  # 返回处理后的 CPU ID
        else:
            return "No CPU ID found"
    else:
        return f"Error retrieving CPU ID: {err.decode().strip()}"


# def get_disk_info():
#     # 获取第一个磁盘的设备名
#     for disk in psutil.disk_partitions():
#         if 'fixed' in disk.opts:
#             return disk.device
#     return None


def generate_fingerprint():
    # 组合获取的信息生成机器指纹
    cpu_info = get_cpu_id()
    text_info = 'douyin'
    if None in (cpu_info, text_info):
        raise ValueError("Failed to get all necessary hardware IDs.")

    # 创建原始指纹字符串
    raw_fingerprint = f"{cpu_info}|{text_info}"
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


def open_window():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    open_window()
