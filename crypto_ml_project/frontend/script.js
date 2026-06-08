// HTML'deki "Sinyali Al" butonuna tıklanınca bu fonksiyon çalışır
async function sinyalAl() {
    const btnText = document.getElementById("btn-text");
    const resultCard = document.getElementById("result-card");
    const priceDisplay = document.getElementById("price-display");
    const signalDisplay = document.getElementById("signal-display");
    const resultMessage = document.getElementById("result-message");

    // Kullanıcıya yükleniyor mesajı ver
    btnText.innerText = "⏳ Binance'ten Veriler Çekiliyor...";

    try {
        // GİDİP BİZİM YAZDIĞIMIZ API'YE (/predict_auto) VURUYORUZ!
        const response = await fetch("/predict_auto");
        const data = await response.json(); // Gelen JSON cevabını okuyoruz

        // Gelen verileri HTML'deki yerlerine yerleştir
        // Fiyatı daha güzel göstermek için küsuratları silebiliriz veya bırakabiliriz
        priceDisplay.innerText = "$" + data.bugunku_anlik_fiyat.toLocaleString("en-US");
        signalDisplay.innerText = data.karar;
        resultMessage.innerText = data.mesaj;

        // AL veya SAT durumuna göre rengi değiştir (Yeşil veya Kırmızı)
        signalDisplay.className = ""; // Eski rengi sil
        if (data.karar.includes("AL")) {
            signalDisplay.classList.add("signal-buy");
        } else {
            signalDisplay.classList.add("signal-sell");
        }

        // Sonuç kartını görünür yap (Animasyonlu)
        resultCard.classList.add("show");
        
        // Butonu eski haline getir
        btnText.innerText = "🔍 Sinyali Güncelle";

    } catch (error) {
        // Eğer bir hata olursa (İnternet kopması vs)
        alert("Bir hata oluştu! Sunucu açık mı?");
        btnText.innerText = "❌ Hata, Tekrar Dene";
        console.error(error);
    }
}
