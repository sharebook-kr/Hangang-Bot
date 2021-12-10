from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import *
import pyupbit
import time

KEY_FILE = "upbit_keys.txt"


class UpbitTrader(QThread):
    data_update = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        # 초기 데이터 설정 
        self.data = ["Upbit", "미 연결", "없음", "-", "-", "-", "-"]
        self.prev_tickers = self.get_tickers()
        self.private = None
        self.new_ticker = None
        self.hold = False
        self.current_price = 0
        self.buy_price = 0
        self.buy_amount = 0
        self.returns = 0

        self.create_private_instance()

    def get_tickers(self):
        tickers = pyupbit.get_tickers()
        return tickers

    def create_private_instance(self):
        with open(KEY_FILE) as f:
            lines = f.readlines()
            access = lines[0].strip()
            secret = lines[1].strip()
            self.private = pyupbit.Upbit(access, secret)

        if self.private is not None:
            self.data[1] = "연결 중"

    def check_listing(self):
        self.curr_tickers = self.get_tickers()
        difference = set(self.curr_tickers) - set(self.prev_tickers)
        self.prev_tickers = self.curr_tickers                           # update prev

        if len(difference) > 0:
            self.new_ticker = difference.pop()
            self.data[2] = self.new_ticker

    def buy(self):
        pass 

    def trailing_stop(self):
        pass

    def run(self):
        while True:
            # 리스트 갱신 체크 
            self.check_listing()

            # 보유하지 않았고 새로운 티커가 있으면 
            if self.hold is False and self.new_ticker is not None:
                self.buy()


            # UI로 데이터 전송
            self.data_update.emit(self.data)

            # 대기
            time.sleep(0.2)


if __name__ == "__main__":
    trader = UpbitTrader()
    trader.run()