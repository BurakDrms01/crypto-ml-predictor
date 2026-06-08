import pandas as pd
import ta
import numpy as np

df=pd.read_csv("crypto_ml_project/data/BTC_data.csv",index_col="timestamp",parse_dates=True)

rsi_indicator=ta.momentum.RSIIndicator(close=df["close"], window=14)

df["rsi"]=rsi_indicator.rsi()

print(df[["close","rsi"]].head(20))

macd_indicator=ta.trend.MACD(close=df["close"],window_slow=26,window_fast=12,window_sign=9)

df["macd"]=macd_indicator.macd()
df["macd_signal"]=macd_indicator.macd_signal()
df["macd_diff"]=macd_indicator.macd_diff()



print(df[["close","macd","macd_signal","macd_diff"]].head(40))

bb_indicator=ta.volatility.BollingerBands(close=df["close"],window=20,window_dev=2)

df["bb_upper"]=bb_indicator.bollinger_hband()
df["bb_lower"]=bb_indicator.bollinger_lband()
df["mid"]=bb_indicator.bollinger_mavg()
df["width"]=bb_indicator.bollinger_wband()
print(df[["close","bb_upper","bb_lower","mid","width"]].head(40))

df["sma_20"]=df["close"].rolling(window=20).mean()
df["sma_50"]=df["close"].rolling(window=50).mean()
df["sma_cross"]=df["sma_20"]-df["sma_50"]

print(df[["sma_cross","close","sma_20","sma_50"]].tail(50))

df["target"]=(df["close"].shift(-1)>df["close"]).astype(int)
#print(df["target"].value_counts())

#print(df.isnull().sum())

df.dropna(inplace=True)
print(df.shape)
df.to_csv("crypto_ml_project/data/BTC_features.csv")

