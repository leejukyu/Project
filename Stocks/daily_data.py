import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
import threading
import pymysql

class MyWindow(QMainWindow):

    # 프로그램 초기화.
    def __init__(self):
        super().__init__()

        self.conn = pymysql.connect(host='localhost', port=3306, user='root',
                                    password='1234', db='INVESTAR', charset='utf8')

        # 실시간 데이터 담을 테이블 없으면 생성.
        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS daily_stocks(
                code VARCHAR(20),
                Date DATETIME,
                Open BIGINT(20),
                High BIGINT(20),
                Low BIGINT(20),
                Close BIGINT(20),
                Volume BIGINT(20))
            """
            curs.execute(sql)

        # 가져오기 구독 할 종목 코드 DB에서.
        with self.conn.cursor(pymysql.cursors.DictCursor) as curs:
            sql = "SELECT code FROM investar.company_info;"
            curs.execute(query=sql)
            global stocks_dict
            stocks_dict = {code["code"]:[] for code in curs.fetchall()}
        self.conn.commit()
        self.setWindowTitle("RealTimeSet")
        self.setGeometry(1200, 300, 300, 300)
        btn = QPushButton("Register", self)
        btn.move(20, 20)
        btn.clicked.connect(self.btn_clicked)
        btn2 = QPushButton("Cancel", self)
        btn2.move(20, 70)
        btn2.clicked.connect(self.btn2_clicked)
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self._handler_login)

        # 등록된 fid에 대해서 변화가 일어날때, 여기서 매번 이벤트 발생.
        self.ocx.OnReceiveRealData.connect(self._handler_real_data)

        # 연결.
        self.CommmConnect()

    # 초기화 관련 함수들.
    def CommmConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        self.statusBar().showMessage("login 중 ...")
    def _handler_login(self, err_code):
        if err_code == 0:
            self.statusBar().showMessage("login 완료")

    # 60초 마다 쌓은 종목 데이터를 가공해서 DB에 저장.
    def data_cumulative(self):
        threading.Timer(60, self.data_cumulative).start()
        insert_count = 0
        global stocks_dict
        for code in stocks_dict.keys():
            if len(stocks_dict[code]) != 0:
                if len(stocks_dict[code][0]) == 5:
                    if len(stocks_dict[code]) == 1:
                        Open = stocks_dict[code][0][3]
                        Close = Open
                    else:
                        Open = stocks_dict[code][1][0]
                        Close = stocks_dict[code][-1][0]
                    High = Open
                    Low = Open
                    Volume = 0
                else:
                    Open = stocks_dict[code][0][0]
                    High = Open
                    Low = Open
                    Close = stocks_dict[code][-1][0]
                    Volume = stocks_dict[code][0][1]

                for i in range(1, len(stocks_dict[code])):
                    if stocks_dict[code][i][0] > High:
                        High = stocks_dict[code][i][0]
                    if stocks_dict[code][i][0] < Low:
                        Low = stocks_dict[code][i][0]
                    Volume += stocks_dict[code][i][1]
                stocks_dict[code] = [[Open, High, Low, Close, Volume]]
                with self.conn.cursor() as curs:
                    sql = f"INSERT INTO daily_stocks (code, Date, Open, High, Low, Close, Volume)" \
                          f"VALUES ('{code}', DATE_FORMAT(now(),'%Y-%m-%d-%h-%i'),{stocks_dict[code][0][0]},{stocks_dict[code][0][1]}, {stocks_dict[code][0][2]},{stocks_dict[code][0][3]}, {stocks_dict[code][0][4]});"
                    curs.execute(sql)
                insert_count += 1
        self.conn.commit()
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(f"{insert_count}개의 종목 DB 저장 성공.")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    # 등록 버튼.
    def btn_clicked(self):
        push_fids = ""
        for crnt in subscription_fids:
            push_fids += crnt+";"
        push_codes = ""
        screen_num = 1000
        num = 0
        for code in stocks_dict.keys():
            num += 1
            push_codes += code+";"
            if num%100 == 0:
                screen_nums.append(f"{screen_num}")
                self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                                     f"{screen_num}", f"{push_codes}", f"{push_fids}", "1")
                screen_num += 1
                num = 0
                push_codes = ""
        if num > 0:
            screen_num += 1
            screen_nums.append(f"{screen_num}")
            self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)",
                                 f"{screen_num}", f"{push_codes}", f"{push_fids}", "1")
        print(f"{len(stocks_dict)}개 구독 등록 완료.", end="\n\n")
        self.data_cumulative()

    # 해제 버튼.
    def btn2_clicked(self):
        for screen_num in screen_nums:
            self.ocx.dynamicCall("DisConnectRealData(QString)", f"{screen_num}")
        print(f"{len(stocks_dict)}개 구독 해제 완료.", end="\n\n")
        threading.Timer(60, self.data_cumulative).cancel()

    # init에 OnReceiveRealData과 연결.
    def _handler_real_data(self, code, real_type, data):
        if real_type == "주식체결":
            data2 = list(map(str,str(data).split()))
            global stocks_dict
            recived_list = [abs(int(data2[1])), abs(int(data2[6]))]
            stocks_dict[code].append(recived_list)
            print(f"{code} 임시 저장 완료.")

    def closeEvent(self, event):
        self.deleteLater()

if __name__ == "__main__":
    # 10 : 현재가, 15 : 거래량
    subscription_fids = ["10", "15"]
    screen_nums = []
    stocks_dict = dict()

    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()