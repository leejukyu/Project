import FinanceDataReader as fdr
import pymysql
import pandas as pd
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

class add:
    def __init__(self):
        """DB 연결"""
        self.conn = pymysql.connect(host='localhost', port = 3306, user='root', password='1234', db='INVESTAR', charset='utf8')

        with self.conn.cursor() as curs:
            # 일봉 데이터 저장 테이블
            sql = """
            CREATE TABLE IF NOT EXISTS day_price(
                code VARCHAR(20),
                Date DATETIME,
                Open BIGINT(20),
                High BIGINT(20),
                Low BIGINT(20),
                Close BIGINT(20),
                Volume BIGINT(20),
                PRIMARY KEY (code, Date))
            """
            curs.execute(sql)
            self.conn.commit()

        self.codes = {}
        """company_info 테이블에서 읽어와서 companyData와 codes에 저장"""
        sql = "SELECT * FROM company_info"
        companyInfo = pd.read_sql(sql, self.conn)
        for idx in range(len(companyInfo)):
            self.codes[companyInfo['code'].values[idx]] = companyInfo['company'].values[idx]

    # 일봉 데이터 저장
    def datareader(self, code):
        rd_df = fdr.DataReader(code, '2021-08-01')
        if rd_df is not None:
            rd_df['Date'] = rd_df.index
            with self.conn.cursor() as curs:
                for r in rd_df.itertuples():
                    sql = f"REPLACE INTO day_price VALUES"\
                        f" ('{code}', '{r.Date}', {r.Open}, {r.High}, {r.Low}, {r.Close},{r.Volume})"
                    curs.execute(sql)
                self.conn.commit()

    # db의 마지막 날짜와 지금 날짜가 차이가 있으면 그 기간만큼 db업데이트
    def read_db(self):
        with self.conn.cursor() as curs:
            sql = f"select max(date) from day_price"
            curs.execute(sql)
            date = curs.fetchone()
        today = datetime.today()
        temp = pd.Timestamp(today)
        date_diff = today - date[0]
        
        # 주식장이 없는 날이거나 날짜 차이가 없으면 실행하지 않기
        if (temp.dayofweek == 5 and date_diff.days == 1) or (temp.dayofweek == 6 and date_diff.days == 2) or date_diff.days == 0:
            print(" ")
        else:
            beforday = datetime.date(date[0])
            self.all_code(beforday)

    def all_code(self, date):
        for code in self.codes:
            print(code)
            rd_df = fdr.DataReader(code, f'{date}')
            if rd_df is not None:
                rd_df['Date'] = rd_df.index
                with self.conn.cursor() as curs:
                    for r in rd_df.itertuples():
                        sql = f"REPLACE INTO day_price VALUES"\
                            f" ('{code}', '{r.Date}', {r.Open}, {r.High}, {r.Low}, {r.Close},{r.Volume})"
                        curs.execute(sql)
                    self.conn.commit()

    def excute(self):
        with self.conn.cursor() as curs:
            sql = f"select * from day_price"
            curs.execute(sql)
            df = curs.fetchone()
        if len(df) == 0:
            for code in self.codes:
                self.datareader(code)
        else:
            self.read_db()

if __name__ == '__main__':
    re = add()
    re.excute()