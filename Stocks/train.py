import pymysql
import pandas as pd
from Invester import graph, func
import os

class Train:
    def __init__(self):
        # DB 연결
        self.conn = pymysql.connect(host='localhost', port = 3306, user='root', password='1234', db='INVESTAR', charset='utf8', 
                          autocommit = True, cursorclass = pymysql.cursors.DictCursor)
        self.codes = {}

        # company_info 테이블에서 읽어와서 companyData와 codes에 저장
        sql = "SELECT * FROM company_info"
        companyInfo = pd.read_sql(sql, self.conn)
        for idx in range(len(companyInfo)):
            self.codes[companyInfo['code'].values[idx]] = companyInfo['company'].values[idx]
        
        # 학습용 이미지가 저장될 폴더
        if not os.path.exists('./img'):
            os.mkdir('./img')
            os.mkdir('./img/보합')
            os.mkdir('./img/상승')
            os.mkdir('./img/하락')

    def main(self, full_df, code):        
        df = full_df[0]
        # 반전형인지 확인하기 위해 필요한 변수들 담는 딕셔너리
        lst = {'H':df['High'],'H_idx':0,'L':df['Low'],'L_idx':0,'D':'직선형'}
        size = 19 # 캔들봉 최대 20개

        for i in range(1, len(full_df)-1):
            if i <= size:
                df = full_df[:i]
            else:
                df = full_df[i-size:i]
                lst = func.HL(df, lst)
                lst['D'] = func.direction(lst)
             
            data = full_df[i]
            df.append(data)
            lst = func.new_HL(lst, data, len(df))
            new_D = func.direction(lst)
            target = full_df[i+1]

            # 반전형이면 학습용 캔들 차트 생성 및 저장
            if lst['D'] != new_D:
                folder_name = func.result(data, target)
                graph.train_candle(df, f'{code}_{i}', folder_name)
                lst['D'] = new_D
    
    # KOSPI종목 main함수 실행
    def all_code(self):
        for code in self.codes:
            with self.conn.cursor() as curs:
                sql = f"SELECT Date, Open, High, Low, Close FROM min_price WHERE code = '{code}'"
                curs.execute(sql)
                full_df = curs.fetchall()
                if len(full_df) >= 2:
                    self.main(full_df, code)

        
if __name__ == '__main__':
    train_data = Train()
    train_data.all_code()
