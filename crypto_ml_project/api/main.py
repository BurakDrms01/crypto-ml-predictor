from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import joblib 
import pandas as pd
from pydantic import BaseModel
import ccxt
import ta



app=FastAPI(title=" Bitcoin Tahmin Botu",description="XGBoost ile BTC Yön Tahmini")

# Sitenin CSS ve JS dosyalarını dışarıya açıyoruz
app.mount("/static", StaticFiles(directory="crypto_ml_project/frontend"), name="static")

model = joblib.load("crypto_ml_project/models/xgboost_model.pkl")
scaler = joblib.load("crypto_ml_project/models/scaler.pkl")
feature_names = joblib.load("crypto_ml_project/models/feature_names.pkl")

# Müşterinin bize göndermek ZORUNDA olduğu veriler (Sipariş Fişi)
class TahminIstegi(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: float
    rsi: float
    macd: float
    macd_signal: float
    macd_diff: float
    bb_upper: float
    bb_lower: float
    mid: float
    width: float
    sma_20: float
    sma_50: float
    sma_cross: float


@app.get("/")
def ana_sayfa():
    return FileResponse("crypto_ml_project/frontend/index.html")

# Müşteri bize veri GÖNDERECEĞİ için GET değil POST kullanıyoruz.
@app.post("/predict")
def tahmin_yap(istek: TahminIstegi):
    
    # 1. Müşterinin fişini (Pydantic modelini) bir Python Sözlüğüne (Dictionary) çevir
    istek_dict = istek.model_dump()
    
    # 2. Modeller DataFrame (Tablo) sever! Sözlüğü 1 satırlık bir Tabloya çeviriyoruz.
    df_istek = pd.DataFrame([istek_dict])
    
    # GÜVENLİK ÖNLEMİ: Müşteri verileri karışık sırayla göndermiş olabilir. 
    # Kaydettiğimiz "feature_names" listesini kullanarak sırayı düzeltiyoruz!
    df_istek = df_istek[feature_names]
    
    # 3. Sayıları modelin anlayacağı dile (küçültülmüş hale) çeviriyoruz (Tercüman)
    scaled_data = scaler.transform(df_istek)
    
    # 4. Aşçıyı çağır ve tahmin yap (0 veya 1 döner)
    tahmin = model.predict(scaled_data)[0]
    
    # 5. Modelin "0" veya "1" cevabını insanın anlayacağı metne çeviriyoruz
    if tahmin == 1:
        karar = "AL Sinyali 🚀 (Fiyat Yükselecek)"
    else:
        karar = "SAT Sinyali 🩸 (Fiyat Düşecek veya Sabit Kalacak)"
        
    # 6. Müşteriye JSON formatında fişi teslim et!
    return {
        "karar": karar, 
        "modelin_kodu": int(tahmin)
    }

# Müşterinin veri girmesine gerek bırakmayan OTOMATİK rota! (GET kullanıyoruz çünkü bizden bir şey istiyor)
@app.get("/predict_auto")
def otomatik_tahmin():
    # 1. Binance'e bağlan ve son 60 günün verisini çek
    borsa = ccxt.binance()
    veriler = borsa.fetch_ohlcv('BTC/USDT', timeframe='1d', limit=60)
    
    # 2. Gelen veriyi Tabloya (DataFrame) çevir
    df = pd.DataFrame(veriler, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # 3. Teknik göstergeleri hesapla (Aylardır yaptığımız şeyin aynısı)
    df["rsi"] = ta.momentum.RSIIndicator(close=df["close"], window=14).rsi()
    
    macd = ta.trend.MACD(close=df["close"], window_slow=26, window_fast=12, window_sign=9)
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_diff"] = macd.macd_diff()
    
    bb = ta.volatility.BollingerBands(close=df["close"], window=20, window_dev=2)
    df["bb_upper"] = bb.bollinger_hband()
    df["bb_lower"] = bb.bollinger_lband()
    df["mid"] = bb.bollinger_mavg()
    df["width"] = bb.bollinger_wband()
    
    df["sma_20"] = df["close"].rolling(window=20).mean()
    df["sma_50"] = df["close"].rolling(window=50).mean()
    df["sma_cross"] = df["sma_20"] - df["sma_50"]
    
    # 4. BÜYÜK NUMARA: Tablodaki EN SON satır (Yani tam şu anki BUGÜNÜN verisi) bize lazım!
    bugun_df = df.iloc[[-1]] # Sadece son satırı aldık
    
    # Güvenlik Önlemi: Kolon sıraları aynı olsun
    bugun_df = bugun_df[feature_names]
    
    # 5. Tercümana çevirt ve Aşçıyı çalıştır!
    scaled_data = scaler.transform(bugun_df)
    tahmin = model.predict(scaled_data)[0]
    
    if tahmin == 1:
        karar = "AL Sinyali 🚀 (Yükseliş Bekleniyor)"
    else:
        karar = "SAT Sinyali 🩸 (Düşüş Bekleniyor)"
        
    # Müşteriye sonucu ver
    return {
        "bugunku_anlik_fiyat": float(bugun_df["close"].iloc[0]),
        "karar": karar,
        "mesaj": "Tüm veriler anlık olarak Binance'ten çekildi ve otomatik hesaplandı!"
    }
