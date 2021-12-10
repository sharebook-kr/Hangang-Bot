import sys 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime
from exchanges.upbit_trader import *

EXCHANGE = ["Upbit", "Bithumb", "Korbit", "CoinOne"]


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__() 

        # MainWindow 
        self.setGeometry(300, 300, 750, 300)
        self.setWindowTitle("Hangang Bot v0.1")

        # Timer 
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.update_status_bar)

        # QTableWidget 생성 
        self.columns = ["거래소", "연결상태", "신규상장코인", "현재가", "매수가", "수량", "수익률"]
        self.table_data = [
            [EXCHANGE[0], "미 연결", "없음", "-", "-", "-", "-"],
            [EXCHANGE[1], "미 연결", "없음", "-", "-", "-", "-"],
            [EXCHANGE[2], "미 연결", "없음", "-", "-", "-", "-"],
            [EXCHANGE[3], "미 연결", "없음", "-", "-", "-", "-"],
        ]
        self.create_table()                

        # QLayout
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(self.table)
        self.setCentralWidget(widget)

        # Work thread
        self.upbit_trader = UpbitTrader()
        self.upbit_trader.data_update.connect(self.update_table_row)
        self.upbit_trader.start()


    def create_table(self):
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnCount(len(self.columns))
        self.table.setRowCount(len(EXCHANGE))
        self.table.setHorizontalHeaderLabels(self.columns)

        for row in range(0, len(EXCHANGE)):
            for col in range(0, len(self.columns)):
                item = QTableWidgetItem(self.table_data[row][col])
                self.table.setItem(row, col, item)

    def update_status_bar(self):
        now = datetime.datetime.now()
        self.statusBar().showMessage(str(now))    

    @pyqtSlot(list)
    def update_table_row(self, exchange_data):
        exchange = exchange_data[0]
        row = EXCHANGE.index(exchange)

        # update a row 
        for col in range(0, len(self.columns)):
            item = QTableWidgetItem(exchange_data[col])
            self.table.setItem(row, col, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()