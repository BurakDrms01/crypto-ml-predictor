
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns 


df=pd.read_csv("crypto_ml_project/data/BTC_data.csv",index_col="timestamp",parse_dates=True)


# print(df.head())

# print(df.shape)
# print(df.dtypes)
# print(df.isnull().sum())
# print(df.index.dtype)
# print(df.describe())
# plt.plot(df.index,df["close"])
# plt.title("BTC/USDT-Son 1 Yıl")
# plt.xlabel("Tarih")
# plt.ylabel("Fiyat (USD)")
# plt.grid(True)

# plt.show()

# sns.heatmap(df.corr(),annot=True)
# plt.show()
# returns=df["close"].pct_change()

# # plt.plot(df.index,returns)
# # plt.show()

# # sns.histplot(data=returns, kde=True,bins=50)
# # plt.show()

# sns.scatterplot(x=df.index,y=returns)
# plt.show()
volume=df["volume"].pct_change()

# sns.scatterplot(x=df.index,y=volume)
# plt.show()

sns.histplot(data=volume, kde=True, bins=50)
plt.show()