import pandas as pd

# 20개 이상일 때 고가 저가 위치 초기화
def HL(df, lst):
    df = pd.DataFrame(df)
    lst['H'] = df['High'].max()
    lst['H_idx'] = list(df['High']).index(lst['H'])
    lst['L'] = df['Low'].min()
    lst['L_idx'] = list(df['Low']).index(lst['L'])
    return lst

# 새로운 고가 저가 위치 찾기
def new_HL(lst, data, num):
    if lst['H'] < data['High']:
        lst['H'] = data['High']
        lst['H_idx'] = num

    if lst['L'] > data['Low']:
        lst['L'] = data['Low']
        lst['L_idx'] = num
    return lst

# 고가 저가 위치로 방향 확인
def direction(lst):
    if lst['H_idx'] > lst['L_idx']:
        D = '상승형'
    elif lst['H_idx'] < lst['L_idx']:
        D = '하락형'
    else:
        D = '직선형'
    return D

# target값 구하기
def result(data, target):
    if data['Close'] < target['Close']:
        label = '상승'
    elif data['Close'] > target['Close']:
        label = '하락'
    else:
        label = '보합'
    return label