import pandas as pd
import mplfinance as mpf

class Turn:    
    def __init__(self):
        return

    def labeling(self, row_data):
        """캔들 모양 라벨링"""
        S = row_data['Open']
        E = row_data['Close']
        H = row_data['High']
        L = row_data['Low']

        up_down_state = E-S
        if up_down_state > 0:
            body = E-S
            top_t = H - E
            bottom_t = S - L
        else:
            body = S-E
            top_t = H-S
            bottom_t = E-L
        candle_sum = top_t + bottom_t + body

        if candle_sum == 0: # 0으로 나눌 수 없어 1로 변경
            candle_sum = 1

        top_t = round(top_t/candle_sum, 5); bottom_t = round(bottom_t/candle_sum, 5); body = round(body/candle_sum, 5)

        # E유형 분류
        if body < 0.1: # body 비중이 10% 이하면, 도지형으로 분류

            if top_t < 0.1: # 동시에 위 꼬리의 비중도 10%가 안되면,
                answer = "E2"
            elif bottom_t < 0.1: # 아래 꼬리의 비중이 10%가 안되면,
                answer = 'E4'
            elif top_t >= 0.1 and bottom_t >= 0.1: # 위아래 꼬리 둘다 각각 10% 이상의 비중을 차지하면,
                answer = 'E3'
            else: # 그 외.
                answer = 'E1'
        else:
            # 양봉 음봉 판별.
            if up_down_state > 0:
                answer = "U"
            else:
                answer = "D"

            # body 길이에 따라 분류
            if body < 0.37: # 소봉
                if top_t >= 0.1 and bottom_t >= 0.1:
                    answer += '7'
                elif top_t < 0.1:
                    if answer == "U":
                        answer += '4'
                    else:
                        answer += '8'
                elif bottom_t < 0.1:
                    if answer == "U":
                        answer += '8'
                    else:
                        answer += '4'
                else:
                    pass

            elif body < 0.64: # 중봉
                if top_t >= 0.1 and bottom_t >= 0.1:
                    answer += '6'
                elif top_t < 0.1:
                    if answer == "U":
                        answer += '3'
                    else:
                        answer += '9'
                elif bottom_t < 0.1:
                    if answer == "U":
                        answer += '9'
                    else:
                        answer += '3'
                else:
                    pass

            elif body < 0.9: # 대봉
                if top_t >= 0.1 and bottom_t >= 0.1:
                    answer += '5'
                elif top_t < 0.1:
                    if answer == "U":
                        answer += '2'
                    else:
                        answer += '10'
                elif bottom_t < 0.1:
                    if answer == "U":
                        answer += '10'
                    else:
                        answer += '2'
                else:
                    pass

            else: # 장대봉
                answer += '1'
        return answer

    def candle_labeling(self, df):
        """끝에서 두 개 데이터만 인덱싱"""
        df1 = df[-2]
        df2 = df[-1]
        C1 = self.labeling(df1)
        C2 = self.labeling(df2)
        return C1, C2
