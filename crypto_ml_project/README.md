# 🚀 Uçtan Uca Bitcoin Tahmin Botu (XGBoost & FastAPI)

Bu proje, makine öğrenmesi (Machine Learning) algoritmaları kullanarak günlük Bitcoin fiyat hareketlerini tahmin eden ve bu tahminleri modern bir web arayüzü ile kullanıcıya sunan uçtan uca (End-to-End) bir projedir.

## 🛠️ Kullanılan Teknolojiler (Tech Stack)
- **Veri Bilimi & ML:** `Pandas`, `Scikit-Learn`, `XGBoost`, `TA` (Technical Analysis)
- **Veri Kaynağı:** `CCXT` (Binance API)
- **Backend (API):** `FastAPI`, `Uvicorn`, `Pydantic`
- **Frontend:** `HTML5`, `CSS3` (Vanilla), `JavaScript`

## 📂 Proje Mimarisi
Proje, veri toplama aşamasından başlayarak canlı bir web arayüzüne kadar 4 temel aşamadan oluşur:

- `/notebooks`: Verinin Binance üzerinden çekildiği (01), keşifsel analizinin yapıldığı (02), teknik analiz indikatörleriyle (RSI, MACD vb.) özelliklerin üretildiği (03) ve modelin XGBoost kullanılarak eğitilip kaydedildiği (04) Jupyter defterleri.
- `/models`: Eğitilmiş makine öğrenmesi modeli (`xgboost_model.pkl`), veri ölçekleyici (`scaler.pkl`) ve özellik isimlerinin kaydedildiği klasör.
- `/api`: Kaydedilen makine öğrenmesi modelini dış dünyaya açan `FastAPI` sunucusu (`main.py`).
- `/frontend`: Tahmin sonuçlarının anlık ve görsel olarak gösterildiği kullanıcı arayüzü dosyaları (`index.html`, `style.css`, `script.js`).

## ⚙️ Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırayla izleyin:

### 1. Depoyu İndirin (Clone)
```bash
git clone https://github.com/BurakDrms01/crypto-ml-predictor.git
cd crypto-ml-predictor
```

### 2. Gerekli Kütüphaneleri Yükleyin
Sanal bir ortam (virtual environment) oluşturduktan sonra `requirements.txt` içindeki bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

### 3. API Sunucusunu Başlatın
Aşağıdaki komutu kullanarak FastAPI sunucusunu ayağa kaldırın:
```bash
uvicorn api.main:app --reload
```

### 4. Web Arayüzüne Gidin
Sunucu başlatıldıktan sonra tarayıcınızı açın ve şu adrese gidin:
👉 **http://127.0.0.1:8000**

## 📈 Nasıl Çalışır?
Arayüzdeki **"Sinyali Analiz Et"** butonuna tıkladığınızda:
1. JavaScript, arka plandaki `FastAPI` endpoint'ine (`/predict_auto`) istek atar.
2. FastAPI, `CCXT` kütüphanesi ile Binance'e bağlanır ve Bitcoin'in son 60 günlük verisini anlık olarak çeker.
3. Çekilen bu veriler `TA` kütüphanesi kullanılarak RSI, MACD, Bollinger Bantları gibi özelliklere dönüştürülür.
4. Kaydedilmiş XGBoost modeli bu özellikleri kullanarak bir tahmin üretir.
5. Sonuç (AL veya SAT sinyali) ekranda şık bir şekilde gösterilir.
