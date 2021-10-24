import mplfinance as mpf
import matplotlib.pyplot as plt    
import pandas as pd
import matplotlib
matplotlib.use("Agg")

def bollinger(df):
    for i in range(len(df.Close)-1):
        if df.TP.values[i] < df.TP.values[i+1]: 
            df.PMF.values[i+1] = df.TP.values[i+1] * df.Volume.values[i+1] # 긍정적 현금흐름에 저장
            df.NMF.values[i+1] = 0
        else:
            df.NMF.values[i+1] = df.TP.values[i+1] * df.Volume.values[i+1]
            df.PMF.values[i+1] = 0
    df['MFR'] = df.PMF.rolling(window=10).sum() / df.NMF.rolling(window=10).sum()
    df['MFI10'] = 100 - 100 / (1 + df['MFR'])
    df = df[19:]
    plt.figure(figsize=(6,3))
    plt.title(f'MFI')
    plt.plot(df.index, df['Close'], color='#0000ff', label='Close')
    plt.plot(df.index, df['upper'], 'r--', label ='Upper band')
    plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
    plt.plot(df.index, df['lower'], 'c--', label ='Lower band')
    plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
    plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')

    for i in range(0, len(df.Close)):
        if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:   
            plt.plot(df.index.values[i], df.Close.values[i], 'r^')
        elif df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0: 
            plt.plot(df.index.values[i], df.Close.values[i], 'bv')
    plt.xticks(rotation=45)
    plt.gcf().subplots_adjust(bottom=0.30)
    plt.legend(loc='upper right')
    plt.savefig('./static/img/bo.png')

def trend(df):
    plt.figure(figsize=(6,3))
    plt.title(f'trend')
    plt.plot(df.index, df['PB'] * 100, 'b', label='%B x 100')       
    plt.plot(df.index, df['MFI10'], 'g--', label='MFI(10 day)')    
    plt.yticks([-20, 0, 20, 40, 60, 80, 100, 120])                  
    for i in range(len(df.Close)):
        if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:
            plt.plot(df.index.values[i], 0, 'r^')
        elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:
            plt.plot(df.index.values[i], 0, 'bv')
    plt.xticks(rotation=45)
    plt.gcf().subplots_adjust(bottom=0.30)
    plt.grid(True)
    plt.legend(loc='best')
    plt.savefig('./static/img/tr.png')

def candle(df):
    mc = mpf.make_marketcolors(up='r', down='b', inherit=True)
    s  = mpf.make_mpf_style(marketcolors=mc)
    mpf.plot(df,type='candle',volume=True, mav=(2, 4, 6), savefig=dict(fname='./static/img/candle.png',dpi=100,pad_inches=0.25), style=s)

def train_candle(df, file_name, folder_name):
    rc={
        "axes.labelcolor": "none",
        "axes.spines.bottom": False,
        "axes.spines.left": False,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "font.size": 0,
        "xtick.color": "none",
        "ytick.color": "none",
        "figure.facecolor" : "none",
    }
    df = pd.DataFrame(df)
    df.set_index('Date',inplace = True)
    mc=mpf.make_marketcolors(up='red', down='blue', inherit=True)
    style_final=mpf.make_mpf_style(marketcolors=mc, rc=rc)
    if folder_name == 'static':
        mpf.plot(df, type='candle', style=style_final, savefig = f"./{folder_name}/daily/{file_name}.png")
    else:
        mpf.plot(df, type='candle', style=style_final, savefig = f"./img/{folder_name}/{file_name}.png")


def data(df):
    df.set_index('Date',inplace=True)
    
    df = df.dropna()
    candle(df)

    df['MA20'] = df['Close'].rolling(window=20).mean() 
    df['stddev'] = df['Close'].rolling(window=20).std() 
    df['upper'] = df['MA20'] + (df['stddev'] * 2)
    df['lower'] = df['MA20'] - (df['stddev'] * 2)
    df['PB'] = (df['Close'] - df['lower']) / (df['upper'] - df['lower'])
    df['II'] = (2*df['Close']-df['High']-df['Low'])/(df['High']-df['Low'])*df['Volume'] 
    df['IIP21'] = df['II'].rolling(window=21).sum()/df['Volume'].rolling(window=21).sum()*100  
    df['TP'] = (df['High'] + df['Low'] + df['Close']) / 3 
    df['PMF'] = 0
    df['NMF'] = 0

    bollinger(df)
    trend(df)

def bar(result):
    x = [1,2,3]
    y = [result[0][2],result[0][3],result[0][4]]
    values = ['Nochange', 'Up', 'Down']
    color = ['gray','red','blue']
    plt.bar(x,y,color=color)
    plt.xticks(x,values)
    plt.savefig('./static/img/bar.png')

