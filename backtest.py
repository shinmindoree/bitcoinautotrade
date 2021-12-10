import pyupbit
import numpy as np
import requests
import json

access = ""          # 본인 값으로 변경
secret = ""          # 본인 값으로 변경
myToken = ""


def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# 시작 메세지 슬랙 전송
post_message(myToken,"#upbit", "autotrade start")


df = pyupbit.get_ohlcv("KRW-BTC", count=200)
df['range'] = (df['high'] - df['low']) * 0.4
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.00105 # 업비트 수수료
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee, 
                     1)

df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD(%): ", df['dd'].max()) 
print("HOR(%): ", df['hpr'])

