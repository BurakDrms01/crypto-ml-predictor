import joblib
import sklearn
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
from  sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score,recall_score,f1_score,confusion_matrix,precision_score
from sklearn.preprocessing import StandardScaler 
from sklearn.model_selection import RandomizedSearchCV
import joblib
import os

df=pd.read_csv('crypto_ml_project/data/BTC_features.csv',index_col="timestamp",parse_dates=True)

X=df.drop("target",axis=1)
y=df["target"]

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,shuffle=False)
scaler=StandardScaler()
X_train=scaler.fit_transform(X_train)
X_test=scaler.transform(X_test)

model_dictionary={"Logistic Regresyon":LogisticRegression(max_iter=1000),
"Random Forest":RandomForestClassifier(),
"XGBoost":XGBClassifier()

}
for name,model in model_dictionary.items():
    model.fit(X_train,y_train)
    y_pred_test=model.predict(X_test)
    y_pred_train=model.predict(X_train)
    print(f"\n--- {name} ---")
    print(f"Train Accuracy: {accuracy_score(y_train, y_pred_train):.2f}")
    print(f"Test Accuracy:  {accuracy_score(y_test, y_pred_test):.2f}")
    print(f"Precision: {precision_score(y_test, y_pred_test):.2f}")
    print(f"Recall:    {recall_score(y_test, y_pred_test):.2f}")
    print(f"F1:        {f1_score(y_test, y_pred_test):.2f}")

    # Hangi Feature Ne Kadar Önemli? (XGBoost'a Göre)
best_model = model_dictionary["XGBoost"] # Eğitilmiş XGBoost'u alıyoruz
importances = best_model.feature_importances_
# Değerleri büyükten küçüğe sıralayalım
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 6))
sns.barplot(x=importances[indices], y=X.columns[indices], hue=X.columns[indices], legend=False, palette="viridis")
plt.title("XGBoost Karar Verirken Neye Baktı? (Feature Importance)")
plt.xlabel("Önem Derecesi")
plt.ylabel("Özellikler (Features)")
plt.tight_layout()
plt.show()

# Her modelin kendi param_grid'i
param_grids = {
    "Random Forest": {
        "n_estimators": [50, 100, 200],
        "max_depth": [3, 5, 10],
        "min_samples_split": [2, 5, 10],
    },
    "XGBoost": {
        "max_depth": [2, 3, 4],
        "learning_rate": [0.01, 0.05, 0.1],
        "n_estimators": [50, 100, 200],
        "subsample": [0.6, 0.8, 1.0],
    }
}

tuned_models = {
    "Random Forest": RandomForestClassifier(),
    "XGBoost": XGBClassifier()
}

print("\n\n=== HYPERPARAMETER TUNING ===")
for name, model in tuned_models.items():
    rs = RandomizedSearchCV(estimator=model, param_distributions=param_grids[name],
                            n_iter=10, cv=3, random_state=42)
    rs.fit(X_train, y_train)
    best = rs.best_estimator_
    y_pred_test = best.predict(X_test)
    y_pred_train = best.predict(X_train)
    print(f"\n--- {name} (Tuned) ---")
    print(f"En iyi parametreler: {rs.best_params_}")
    print(f"Train Accuracy: {accuracy_score(y_train, y_pred_train):.2f}")
    print(f"Test Accuracy:  {accuracy_score(y_test, y_pred_test):.2f}")
    print(f"Precision:      {precision_score(y_test, y_pred_test):.2f}")
    print(f"Recall:         {recall_score(y_test, y_pred_test):.2f}")
    print(f"F1:             {f1_score(y_test, y_pred_test):.2f}")

# ==========================================
# 5. MODELİ VE GEREKLİ ARAÇLARI KAYDETME
# ==========================================

# Önce 'models' adında bir klasör oluşturuyoruz (eğer yoksa)
os.makedirs("crypto_ml_project/models", exist_ok=True)

# 1. Modeli Kaydetme
# 'best' değişkeni, yukarıdaki döngüden çıkan en son ve en iyi modeli (XGBoost'u) tutuyor.
# Neden kaydediyoruz?: Proje kapanınca eğitilmiş model silinmesin diye.
joblib.dump(best, "crypto_ml_project/models/xgboost_model.pkl")

# 2. Scaler'ı (Ölçekleyiciyi) Kaydetme
# Neden kaydediyoruz?: Model eğitilirken RSI'yi 0-100'den, MACD'yi 0-5000'den alıp belli bir standarda çekti.
# Yarın dışarıdan canlı veri geldiğinde, o canlı veriyi de aynı oranda küçültüp/büyültmesi için scaler'ın hafızasına ihtiyacımız var!
joblib.dump(scaler, "crypto_ml_project/models/scaler.pkl")

# 3. Özellik (Feature) İsimlerini Kaydetme
# Neden kaydediyoruz?: Model özellikleri hangi sırayla öğrendiyse (önce bb_upper, sonra bb_lower vs.), 
# yarın dışarıdan soru sorarken de o sırayla sormamız lazım. Kontrol etmek için listeyi kaydediyoruz.
joblib.dump(list(X.columns), "crypto_ml_project/models/feature_names.pkl")

print("\nModel, Scaler ve Özellik İsimleri başarıyla 'models' klasörüne kaydedildi! 💾")