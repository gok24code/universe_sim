# 🌌 Universe Sim - Evren Simülasyonu

Ursina Engine kullanılarak geliştirilmiş, prosedürel olarak oluşturulan galaksiler, yıldız sistemleri ve karadeliklerin etrafında süzülen asteroidleri içeren büyüleyici bir uzay simülasyonu.

## 🚀 Özellikler

- **Devasa Sarmal Galaksiler:** Binlerce yıldızdan oluşan, merkezinde olay ufku (event horizon) bulunan dinamik galaksiler.
- **Kütleçekimsel Asteroidler:** Karadeliğe yaklaşırken hızlanan, yörüngesi bükülen ve arkasında parlak buz mavisi kuyruklar bırakan asteroidler (Slingshot etkisi).
- **Prosedürel Yıldız Sistemleri:** Rastgele oluşan güneşler, gezegenler ve uydular.
- **Sonsuz Keşif:** Gelişmiş kamera sistemi ile galaksiler arasında ışık hızında seyahat.

## 🛠️ Kurulum

Simülasyonu çalıştırmak için bilgisayarınızda **Python 3.x** yüklü olmalıdır.

### Hızlı Kurulum (Linux & macOS)

Terminali açın ve proje klasöründe şu komutu çalıştırın:

```bash
chmod +x installscript.sh
./installscript.sh
```

Bu betik otomatik olarak bir sanal ortam (`venv`) oluşturacak ve gerekli kütüphaneleri yükleyecektir.

### Manuel Kurulum

Eğer kurulum betiğini kullanmak istemiyorsanız:

1. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
2. Simülasyonu başlatın:
   ```bash
   python3 main.py
   ```

## 🎮 Kontroller

- **Fare Sağ Tık + WASD:** Kamerayı yönlendirin ve hareket edin.
- **Sol Shift (Basılı Tutun):** Işık hızına geçiş yapın (Kamera hareketini hızlandırır).
- **Fare Tekerleği:** İleri/Geri yakınlaşma.
- **ESC:** Simülasyondan çıkış.

## 📂 Proje Yapısı

- `main.py`: Uygulamanın ana giriş noktası.
- `app_settings.py`: Pencere ve kamera ayarları.
- `objects/prefabs.py`: Galaksi, yıldız sistemleri ve asteroid fiziklerinin tanımlandığı yer.
- `requirements.txt`: Gerekli Python kütüphaneleri.

---
*Bu proje bir evren simülasyonu prototipidir. Keyifli keşifler!* 🌠
