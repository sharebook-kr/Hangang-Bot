import sys 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime

EXCHANGE = ["업비트", "빗썸", "코빗", "코인원"]


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__() 

        # MainWindow 
        self.setGeometry(300, 300, 750, 300)
        self.setWindowTitle("Hangang Bot v0.1")

        # Timer 
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)

        # QTableWidget 생성 
        self.create_table()                

        # QLayout
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(self.table)
        self.setCentralWidget(widget)

    def create_table(self):
        self.table = QTableWidget()
        columns = ["거래소", "연결상태", "신규상장코인", "현재가", "매수가", "수량", "수익률"]
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnCount(len(columns))
        self.table.setRowCount(len(EXCHANGE))
        self.table.setHorizontalHeaderLabels(columns)

    def timeout(self):
        now = datetime.datetime.now()
        self.statusBar().showMessage(str(now))    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()