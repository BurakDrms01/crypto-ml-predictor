import ccxt
import pandas as pd

exchange=ccxt.binance()

since = exchange.milliseconds() - 1100 * 24 * 60 * 60 * 1000
ohlcv=exchange.fetch_ohlcv("BTC/USDT","1d",since=since,limit=1000
)

ohlcv=pd.DataFrame(columns=["timestamp","open","high","low","close","volume"],data=ohlcv)
ohlcv["timestamp"]=pd.to_datetime(ohlcv["timestamp"],unit="ms")
ohlcv=ohlcv.set_index("timestamp")
save=ohlcv.to_csv("crypto_ml_project/data/BTC_data.csv",index=True)

