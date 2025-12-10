# 🎯 Yüz Tanıma Tabanlı Yoklama Sistemi

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Bu proje, **Python** ve **OpenCV** kullanarak geliştirilmiş tam özellikli bir **Yüz Tanıma Tabanlı Yoklama Sistemi**dir. Kamera aracılığıyla öğrencilerin yüzlerini tanıyarak otomatik yoklama kaydı oluşturur.

---

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Proje Yapısı](#-proje-yapısı)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Konfigürasyon](#-konfigürasyon)
- [Sorun Giderme](#-sorun-giderme)
- [Yüz Tanıma Doğruluğunu Artırma](#-yüz-tanıma-doğruluğunu-artırma)
- [Katkıda Bulunma](#-katkıda-bulunma)

---

## ✨ Özellikler

- ✅ **Gerçek Zamanlı Yüz Tanıma**: Kamera ile canlı yüz algılama ve tanıma
- ✅ **Otomatik Excel Kaydı**: Tanınan öğrenciler için otomatik yoklama kaydı
- ✅ **Çift Kayıt Engelleme**: Aynı öğrenci günde bir kez kaydedilir
- ✅ **128-D Yüz Encoding**: Yüksek doğruluklu yüz tanıma algoritması
- ✅ **Performans Optimizasyonu**: Frame atlama ile hızlı işlem
- ✅ **Modüler Tasarım**: Temiz ve genişletilebilir kod yapısı
- ✅ **Detaylı Loglama**: İşlem adımlarının konsola yazdırılması

---

## 📁 Proje Yapısı

```
yuz_tanima/
│
├── 📂 dataset/                 # Öğrenci yüz fotoğrafları
│   ├── 123_Ali_Yilmaz.jpg
│   ├── 124_Ayse_Kaya.jpg
│   └── ...
│
├── 📂 encodings/               # Yüz encoding verileri
│   └── face_encodings.pickle
│
├── 📂 attendance/              # Yoklama Excel dosyaları
│   └── yoklama_2025_12_03.xlsx
│
├── 📄 main.py                  # Ana program (kamera + yüz tanıma)
├── 📄 encode_faces.py          # Yüz encoding oluşturma
├── 📄 utils.py                 # Yardımcı fonksiyonlar
├── 📄 requirements.txt         # Gerekli kütüphaneler
└── 📄 README.md                # Bu dosya
```

---

## 🚀 Kurulum

### 1. Gereksinimler

- Python 3.10 veya üstü
- Webcam veya USB kamera
- Windows 10/11, macOS veya Linux

### 2. Depoyu Klonlayın

```bash
git clone https://github.com/kullanici/yuz-tanima-yoklama.git
cd yuz-tanima-yoklama
```

### 3. Sanal Ortam Oluşturun (Önerilen)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Kütüphaneleri Kurun

```bash
pip install -r requirements.txt
```

### ⚠️ Windows için Özel Kurulum

`face_recognition` kütüphanesi dlib'e bağımlıdır. Windows'ta kurulum için:

**Yöntem 1: Visual Studio Build Tools**
1. [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) indirin
2. "C++ build tools" seçeneğini kurun
3. `pip install cmake dlib face_recognition`

**Yöntem 2: Conda ile (Daha Kolay)**
```bash
conda install -c conda-forge dlib
pip install face_recognition
```

**Yöntem 3: Hazır Wheel Dosyası**
```bash
# Python sürümünüze uygun wheel indirin
pip install dlib-19.22.99-cp310-cp310-win_amd64.whl
pip install face_recognition
```

---

## 📖 Kullanım

### Adım 1: Öğrenci Fotoğraflarını Hazırlayın

`dataset/` klasörüne öğrenci fotoğraflarını ekleyin.

**Dosya Adı Formatı**: `NUMARA_ADSOYAD.jpg`

```
dataset/
├── 123_Ali_Yilmaz.jpg
├── 124_Ayse_Kaya.png
├── 125_Mehmet_Demir.jpg
└── 126_Zeynep_Ozturk.jpeg
```

**Fotoğraf Kuralları**:
- 📸 Yüz net görünmeli (bulanık olmamalı)
- 📸 Yüz tam önden çekilmeli
- 📸 İyi aydınlatma olmalı
- 📸 Yüzün en az %30'u görüntüde olmalı
- 📸 Tek kişi olmalı (arka planda başka yüz olmamalı)
- 📸 Desteklenen formatlar: `.jpg`, `.jpeg`, `.png`, `.bmp`

### Adım 2: Yüz Encoding'lerini Oluşturun

```bash
python encode_faces.py
```

Bu komut:
- Dataset'teki tüm fotoğrafları tarar
- Her fotoğraftan yüz bulur
- 128-D encoding vektörü oluşturur
- `encodings/face_encodings.pickle` dosyasına kaydeder

**Çıktı Örneği**:
```
==============================================================
 YÜZ ENCODING OLUŞTURMA
==============================================================

[1/4] İşleniyor: Ali Yilmaz (123)
  [✓] Resim yüklendi: 123_Ali_Yilmaz.jpg
  [✓] Yüz lokasyonu bulundu
  [✓] 128-D encoding vektörü oluşturuldu
  [✓] Başarıyla kaydedildi!

[BAŞARILI] 4 öğrenci encoding'i başarıyla kaydedildi!
```

### Adım 3: Yoklama Sistemini Çalıştırın

```bash
python main.py
```

**Kontroller**:
- `q` veya `ESC`: Programı kapat
- `s`: Yoklama özetini göster

**Ekran Görüntüsü**:
```
┌─────────────────────────────────────────────┐
│  Yuz Tanima Yoklama Sistemi                 │
│  03.12.2025 14:30:45         Yoklama: 5 kisi│
├─────────────────────────────────────────────┤
│                                             │
│      ┌───────────┐                          │
│      │           │                          │
│      │   YÜZ     │                          │
│      │           │                          │
│      └───────────┘                          │
│      Ali Yilmaz                             │
│                                             │
├─────────────────────────────────────────────┤
│  Cikis: 'q' | Ozet: 's'                     │
└─────────────────────────────────────────────┘
```

---

## ⚙️ Konfigürasyon

`main.py` dosyasındaki ayarları değiştirebilirsiniz:

```python
# Kamera ayarları
CAMERA_INDEX = 0          # 0 = dahili kamera, 1 = USB kamera
FRAME_WIDTH = 640         # Görüntü genişliği
FRAME_HEIGHT = 480        # Görüntü yüksekliği

# Performans ayarları
PROCESS_EVERY_N_FRAMES = 4  # Her 4 frame'de 1 işle (düşük = hızlı, yüksek = performanslı)
SCALE_FACTOR = 0.25         # Görüntü küçültme (0.25 = %25)

# Yüz tanıma ayarları
FACE_MATCH_TOLERANCE = 0.5  # Eşleşme toleransı (0.4-0.6 arası)
```

### Tolerans Değerleri

| Değer | Açıklama |
|-------|----------|
| 0.4   | Çok katı - Yanlış eşleşme az, kaçırma fazla |
| 0.5   | Dengeli - Önerilen değer |
| 0.6   | Gevşek - Yanlış eşleşme fazla, kaçırma az |

---

## 🔧 Sorun Giderme

### ❌ Kamera Açılmıyor

**Olası Nedenler ve Çözümler**:

1. **Kamera bağlı değil**
   - USB kameranın düzgün takılı olduğundan emin olun

2. **Başka uygulama kullanıyor**
   - Zoom, Skype, Teams gibi uygulamaları kapatın
   - Tarayıcıdaki kamera izinlerini kontrol edin

3. **Kamera izni yok**
   - Windows: Ayarlar → Gizlilik → Kamera izinlerini kontrol edin
   - Uygulamanın kamera erişimine izin verin

4. **Yanlış kamera indexi**
   ```python
   # main.py'de değiştirin
   CAMERA_INDEX = 1  # veya 2
   ```

5. **Sürücü sorunu**
   - Kamera sürücülerini güncelleyin
   - Cihaz Yöneticisi'nden kontrol edin

### ❌ face_recognition Kurulumu Başarısız

**Windows için**:
```bash
# 1. cmake kurun
pip install cmake

# 2. Visual Studio Build Tools kurun
# https://visualstudio.microsoft.com/visual-cpp-build-tools/

# 3. Sonra kurun
pip install dlib
pip install face_recognition
```

**macOS için**:
```bash
brew install cmake
pip install dlib face_recognition
```

**Linux için**:
```bash
sudo apt-get install cmake libboost-all-dev
pip install dlib face_recognition
```

### ❌ Yüz Tanınmıyor

1. **Fotoğraf kalitesi düşük**
   - Daha net fotoğraf kullanın
   - Yüzün büyük görünmesini sağlayın

2. **Aydınlatma sorunu**
   - Ortamı daha iyi aydınlatın
   - Arka ışıktan kaçının

3. **Yüz açısı**
   - Kameraya doğrudan bakın
   - Yüzün tam görünmesini sağlayın

4. **Tolerans değeri**
   ```python
   FACE_MATCH_TOLERANCE = 0.6  # Daha gevşek
   ```

### ❌ Excel Dosyası Açılmıyor

```bash
pip install openpyxl --upgrade
```

---

## 🎯 Yüz Tanıma Doğruluğunu Artırma

### 1. Kaliteli Fotoğraf Kullanın

| ✅ Doğru | ❌ Yanlış |
|----------|-----------|
| Net, odaklı | Bulanık |
| İyi aydınlatma | Karanlık veya arka ışık |
| Tam yüz | Yandan veya eğik |
| Tek kişi | Birden fazla yüz |

### 2. Birden Fazla Fotoğraf Ekleyin

Her öğrenci için 2-3 farklı fotoğraf ekleyin:
```
dataset/
├── 123_Ali_Yilmaz_1.jpg
├── 123_Ali_Yilmaz_2.jpg
├── 123_Ali_Yilmaz_3.jpg
```

### 3. HOG Yerine CNN Kullanın (GPU Gerekli)

`encode_faces.py` dosyasında:
```python
# Daha doğru ama daha yavaş
face_locations = face_recognition.face_locations(image, model="cnn")
```

### 4. Tolerans Değerini Ayarlayın

```python
# Daha katı eşleşme
FACE_MATCH_TOLERANCE = 0.45
```

### 5. Frame İşleme Sıklığını Artırın

```python
# Her frame işle (daha yavaş ama daha güvenilir)
PROCESS_EVERY_N_FRAMES = 1
```

---

## 📊 Excel Çıktı Formatı

Yoklama dosyası `attendance/yoklama_YYYY_MM_DD.xlsx` olarak kaydedilir:

| Ad Soyad | Numara | Tarih | Saat | Durum |
|----------|--------|-------|------|-------|
| Ali Yılmaz | 123 | 03.12.2025 | 09:15:32 | Geldi |
| Ayşe Kaya | 124 | 03.12.2025 | 09:16:45 | Geldi |
| Mehmet Demir | 125 | 03.12.2025 | 09:20:11 | Geldi |

---

## 🔐 Güvenlik Notları

- Yüz verileri (`face_encodings.pickle`) hassas veri içerir
- Bu dosyayı paylaşmayın veya sürüm kontrolüne eklemeyin
- KVKK/GDPR uyumluluğu için izin alın
- Verileri güvenli şekilde saklayın

---

## 🛠️ Geliştirme

### Kod Standartları

- PEP 8 uyumlu Python kodu
- Type hints kullanımı
- Detaylı docstring'ler
- Try-except hata yönetimi

### Test

```bash
# utils.py testleri
python utils.py

# encode_faces.py bilgi modu
python encode_faces.py --info
```

---

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

---

## 🙏 Teşekkürler

- [face_recognition](https://github.com/ageitgey/face_recognition) - Adam Geitgey
- [OpenCV](https://opencv.org/) - Open Source Computer Vision Library
- [dlib](http://dlib.net/) - Modern C++ Machine Learning Toolkit

---

## 📧 İletişim

Sorularınız için issue açabilir veya katkıda bulunabilirsiniz.

---

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!**
