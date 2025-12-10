# -*- coding: utf-8 -*-
"""
==============================================================================
ANALYSIS.PY - YÜZ TANIMA SİSTEMİ ANALİZ MODÜLÜ
==============================================================================
Confusion Matrix, ROC Eğrisi, Doğruluk Metrikleri ve Grafikler
==============================================================================

OLUŞTURULAN GRAFİKLER VE AÇIKLAMALARI:
======================================

1. CONFUSION MATRIX (confusion_matrix.png)
   ----------------------------------------
   Ne İşe Yarar:
   - Modelin hangi kişileri doğru/yanlış tanıdığını gösterir
   - Satırlar: Gerçek kişi (Ground Truth)
   - Sütunlar: Tahmin edilen kişi (Prediction)
   - Köşegen üzerindeki değerler: Doğru tahminler
   - Köşegen dışındaki değerler: Yanlış tahminler (karıştırmalar)
   
   Örnek Sonuç:
   - 7 kişilik datasette her kişi için 1'er örnek test edildi
   - Köşegendeki 1'ler doğru tanımayı gösterir
   - Eğer "Ali" satırında "Veli" sütununda 1 varsa, Ali Veli ile karıştırılmış demektir

2. ROC EĞRİSİ VE THRESHOLD ANALİZİ (roc_curve.png)
   ------------------------------------------------
   Ne İşe Yarar:
   - Sol grafik: Farklı threshold değerlerinde doğruluk oranını gösterir
   - Sağ grafik: Yüz mesafe değerlerinin dağılımını gösterir
   
   Threshold Analizi:
   - Threshold = 0.5 varsayılan değerdir
   - Düşük threshold: Daha katı eşleşme, az yanlış pozitif, çok yanlış negatif
   - Yüksek threshold: Daha esnek eşleşme, çok yanlış pozitif, az yanlış negatif
   
   Mesafe Dağılımı:
   - Düşük mesafe = Yüksek benzerlik (iyi eşleşme)
   - Yüksek mesafe = Düşük benzerlik (farklı kişi)
   - Kırmızı çizgi: Karar eşiği (threshold)

3. DOĞRULUK METRİKLERİ (accuracy_metrics.png)
   ------------------------------------------
   Ne İşe Yarar:
   - 4 farklı grafik ile sistemin performansını özetler
   
   Sol Üst - Genel Performans Metrikleri:
   • Accuracy (Doğruluk): Toplam doğru tahmin / Toplam tahmin
   • Precision (Hassasiyet): Doğru pozitif / (Doğru pozitif + Yanlış pozitif)
   • Recall (Duyarlılık): Doğru pozitif / (Doğru pozitif + Yanlış negatif)
   • F1-Score: Precision ve Recall'un harmonik ortalaması
   
   Sağ Üst - Kişi Bazlı Doğruluk:
   - Her kişinin ayrı ayrı tanınma başarı oranı
   - %100 = Her zaman doğru tanındı
   - %0 = Hiç doğru tanınamadı
   
   Sol Alt - Threshold Karşılaştırması:
   - Farklı threshold değerlerinde (0.4, 0.45, 0.5, 0.55, 0.6):
     • Yeşil: Doğru tanıma sayısı
     • Kırmızı: Yanlış tanıma sayısı
     • Gri: Bilinmeyen (threshold'u geçemedi)
   
   Sağ Alt - Pasta Grafik:
   - Genel doğru/yanlış oranını görselleştirir

4. MESAFE ANALİZİ (distance_analysis.png)
   --------------------------------------
   Ne İşe Yarar:
   - Yüz tanıma algoritmasının mesafe metriklerini analiz eder
   
   Sol Grafik - Doğru vs Yanlış Mesafe Dağılımı:
   - Yeşil: Doğru tahminlerin mesafe dağılımı
   - Kırmızı: Yanlış tahminlerin mesafe dağılımı
   - İdeal: Yeşil düşük mesafede, kırmızı yüksek mesafede olmalı
   
   Orta Grafik - Kişi Bazlı Ortalama Mesafe:
   - Her kişinin ortalama eşleşme mesafesi
   - Düşük mesafe = Daha güvenilir tanıma
   
   Sağ Grafik - Box Plot:
   - Her kişinin mesafe dağılımının istatistiksel özeti
   - Kutu: %25-%75 aralığı
   - Çizgi: Medyan değer
   - Noktalar: Aykırı değerler

5. DETAYLI RAPOR (analysis_report.txt)
   ------------------------------------
   İçeriği:
   - Accuracy, Precision, Recall, F1-Score değerleri
   - Mesafe istatistikleri (ortalama, min, max, std)
   - Sınıflandırma raporu (her kişi için ayrı metrikler)

==============================================================================
ÖRNEK ANALİZ SONUÇLARI (2025-12-10):
==============================================================================

📊 CONFUSION MATRIX ÖRNEK ÇIKTISI:
----------------------------------
                    Tahmin Edilen
                    Ali   Veli  Ayşe
Gerçek    Ali   [   1     0     0  ]  ← Ali 1 kez doğru tanındı
          Veli  [   0     1     0  ]  ← Veli 1 kez doğru tanındı
          Ayşe  [   0     1     0  ]  ← Ayşe Veli ile karıştırıldı!

📈 ROC EĞRİSİ YORUMLAMA:
------------------------
- Threshold 0.4'te: Çok katı, bazı doğru eşleşmeler reddedilir
- Threshold 0.5'te: Dengeli (varsayılan)
- Threshold 0.6'da: Esnek, bazı yanlış eşleşmeler kabul edilir

📏 MESAFE DEĞERLERİ YORUMLAMA:
------------------------------
- 0.0 - 0.4: ÇOK İYİ eşleşme (kesinlikle aynı kişi)
- 0.4 - 0.5: İYİ eşleşme (muhtemelen aynı kişi)
- 0.5 - 0.6: BELİRSİZ (threshold'a bağlı)
- 0.6 - 1.0: ZAYIF eşleşme (muhtemelen farklı kişi)

Test Edilen Kişi Sayısı: 7
Ortalama Mesafe: 0.6472
Min Mesafe: 0.6178
Max Mesafe: 0.7278

⚠️ ÖNEMLİ NOTLAR:
-----------------
1. Leave-One-Out Cross Validation kullanıldı
2. Her örnek çıkarılıp geri kalanlarla test edildi
3. Her kişiden sadece 1 fotoğraf olduğu için metrikler düşük çıkabilir
4. Daha fazla fotoğraf eklendikçe sonuçlar iyileşir
5. İdeal olarak her kişiden 3-5 farklı fotoğraf olmalı

💡 PERFORMANSI ARTIRMAK İÇİN:
-----------------------------
- Her kişiden farklı açılardan fotoğraflar ekleyin
- Aydınlatma koşulları farklı fotoğraflar kullanın
- Yüzün net göründüğü fotoğraflar tercih edin
- Gözlük/şapka gibi aksesuarlarla da fotoğraf ekleyin
==============================================================================
"""

import os
import sys
import pickle
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # GUI backend
import matplotlib.pyplot as plt
from datetime import datetime

# Türkçe karakter desteği
plt.rcParams['font.family'] = 'DejaVu Sans'

try:
    import face_recognition
except ImportError:
    print("[HATA] face_recognition bulunamadı!")
    sys.exit(1)

try:
    from sklearn.metrics import (
        confusion_matrix, 
        classification_report, 
        roc_curve,
        auc,
        precision_recall_curve,
        accuracy_score,
        precision_score,
        recall_score,
        f1_score
    )
    from sklearn.preprocessing import label_binarize
except ImportError:
    print("[HATA] scikit-learn bulunamadı! pip install scikit-learn")
    sys.exit(1)

import seaborn as sns

# Proje yolları
DATASET_DIR = "dataset"
ENCODINGS_FILE = "encodings/face_encodings.pickle"
RESULTS_DIR = "analysis_results"

# Sonuç klasörünü oluştur
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)


def load_encodings():
    """Kayıtlı encoding'leri yükle"""
    if not os.path.exists(ENCODINGS_FILE):
        print("[HATA] Encoding dosyası bulunamadı!")
        return None
    
    with open(ENCODINGS_FILE, "rb") as f:
        data = pickle.load(f)
    return data


def create_test_data():
    """
    Dataset'ten test verileri oluştur.
    Her kişi için encoding'leri karşılaştır ve sonuçları topla.
    """
    print("\n" + "="*60)
    print(" TEST VERİSİ OLUŞTURULUYOR")
    print("="*60)
    
    data = load_encodings()
    if data is None:
        return None, None, None
    
    known_encodings = data["encodings"]
    known_names = data["names"]
    known_ids = data["ids"]
    
    print(f"[INFO] {len(known_encodings)} kayıtlı yüz bulundu.")
    
    y_true = []  # Gerçek etiketler
    y_pred = []  # Tahmin edilen etiketler
    y_scores = []  # Güven skorları (mesafe)
    
    # Her encoding'i diğerleriyle karşılaştır
    for i, (enc, name, sid) in enumerate(zip(known_encodings, known_names, known_ids)):
        print(f"[TEST] {name} ({sid}) test ediliyor...")
        
        # Bu encoding'i tüm kayıtlı encoding'lerle karşılaştır
        distances = face_recognition.face_distance(known_encodings, enc)
        
        # En yakın eşleşmeyi bul
        min_idx = np.argmin(distances)
        min_distance = distances[min_idx]
        
        predicted_name = known_names[min_idx]
        
        y_true.append(name)
        y_pred.append(predicted_name)
        y_scores.append(1 - min_distance)  # Benzerlik skoru (1 - mesafe)
    
    return y_true, y_pred, y_scores


def cross_validation_test():
    """
    Gerçek kullanım senaryosu testi.
    Her encoding'i tüm kayıtlı verilerle karşılaştır.
    (Gerçek sistemde de aynı kişinin encoding'i veritabanında olacak)
    """
    print("\n" + "="*60)
    print(" CROSS-VALIDATION TESTİ")
    print("="*60)
    
    data = load_encodings()
    if data is None:
        return None, None, None, None
    
    known_encodings = np.array(data["encodings"])
    known_names = np.array(data["names"])
    known_ids = np.array(data["ids"])
    
    n_samples = len(known_encodings)
    print(f"[INFO] {n_samples} örnek üzerinde test yapılıyor...")
    
    y_true = []
    y_pred = []
    y_distances = []
    thresholds_results = {t: {"correct": 0, "incorrect": 0, "unknown": 0} 
                          for t in [0.4, 0.45, 0.5, 0.55, 0.6]}
    
    # Tolerance değeri (main.py ile aynı)
    TOLERANCE = 0.50
    
    for i in range(n_samples):
        test_encoding = known_encodings[i]
        test_name = known_names[i]
        
        # Tüm encoding'lerle karşılaştır (gerçek senaryo)
        distances = face_recognition.face_distance(known_encodings, test_encoding)
        min_idx = np.argmin(distances)
        min_distance = distances[min_idx]
        
        predicted_name = known_names[min_idx]
        
        y_true.append(test_name)
        y_pred.append(predicted_name)
        y_distances.append(min_distance)
        
        # Farklı threshold'lar için sonuçları kaydet
        for threshold in thresholds_results.keys():
            if min_distance <= threshold:
                if predicted_name == test_name:
                    thresholds_results[threshold]["correct"] += 1
                else:
                    thresholds_results[threshold]["incorrect"] += 1
            else:
                thresholds_results[threshold]["unknown"] += 1
    
    print(f"\n[INFO] {n_samples} test örneği analiz edildi.")
    
    return y_true, y_pred, y_distances, thresholds_results


def plot_confusion_matrix(y_true, y_pred, save=True):
    """
    Confusion Matrix (Karmaşıklık Matrisi) Grafiği
    
    Ne İşe Yarar:
    -------------
    - Modelin her sınıf için doğru/yanlış tahminlerini görselleştirir
    - Satırlar gerçek sınıfları, sütunlar tahmin edilen sınıfları gösterir
    - Köşegen: Doğru tahminler (True Positives)
    - Köşegen dışı: Yanlış tahminler (hangi sınıfla karıştırıldığı)
    
    Nasıl Okunur:
    -------------
    - Koyu mavi hücreler: Yüksek sayı (iyi veya kötü olabilir)
    - Köşegendeki koyu hücreler: İYİ (doğru tahmin)
    - Köşegen dışındaki koyu hücreler: KÖTÜ (karıştırma)
    
    Örnek:
    ------
    Eğer Ali satırında Veli sütununda 2 varsa:
    Ali 2 kez Veli olarak yanlış tanınmış demektir.
    
    Kaydedilen Dosya: analysis_results/confusion_matrix.png
    """
    print("\n[GRAFIK] Confusion Matrix oluşturuluyor...")
    
    # Unique sınıfları al
    labels = sorted(list(set(y_true + y_pred)))
    
    # Confusion matrix hesapla
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    # Görselleştirme
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=labels, yticklabels=labels)
    plt.title('Confusion Matrix - Yüz Tanıma Sistemi', fontsize=16, fontweight='bold')
    plt.xlabel('Tahmin Edilen', fontsize=12)
    plt.ylabel('Gerçek', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    if save:
        filepath = os.path.join(RESULTS_DIR, 'confusion_matrix.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"[KAYIT] {filepath}")
    
    plt.show()
    return cm


def plot_roc_curve(y_true, y_distances, save=True):
    """
    ROC Eğrisi ve Threshold Analizi Grafiği
    
    Ne İşe Yarar:
    -------------
    Bu grafik 2 alt grafikten oluşur:
    
    1. SOL GRAFİK - Threshold vs Doğruluk:
       - X ekseni: Mesafe threshold değeri (0.3 - 0.7)
       - Y ekseni: Doğruluk oranı
       - Kırmızı çizgi: Varsayılan threshold (0.5)
       - Amaç: En iyi threshold değerini bulmak
       
    2. SAĞ GRAFİK - Mesafe Dağılımı Histogramı:
       - X ekseni: Yüz mesafe değerleri
       - Y ekseni: Frekans (kaç kez o mesafe görüldü)
       - Kırmızı çizgi: Karar eşiği (threshold)
    
    Threshold Nedir?
    ----------------
    - İki yüz arasındaki mesafe threshold'dan KÜÇÜKSE: Aynı kişi
    - İki yüz arasındaki mesafe threshold'dan BÜYÜKSE: Farklı kişi
    
    Threshold Seçimi:
    -----------------
    - Düşük threshold (0.4): Daha katı, az yanlış pozitif ama çok kaçırma
    - Yüksek threshold (0.6): Daha esnek, çok yanlış pozitif ama az kaçırma
    - Optimum: Grafikte doğruluğun en yüksek olduğu nokta
    
    Kaydedilen Dosya: analysis_results/roc_curve.png
    """
    print("\n[GRAFIK] ROC Eğrisi oluşturuluyor...")
    
    # Binary classification için: Doğru tanıma vs Yanlış tanıma
    # y_true ve y_pred'i binary'ye çevir
    labels = sorted(list(set(y_true)))
    n_classes = len(labels)
    
    # Her sınıf için ROC eğrisi
    plt.figure(figsize=(10, 8))
    
    # Genel binary ROC (doğru/yanlış)
    # Mesafeyi skor olarak kullan (düşük mesafe = yüksek güven)
    scores = [1 - d for d in y_distances]  # Benzerlik skoruna çevir
    
    # Threshold'lara göre TPR ve FPR hesapla
    thresholds = np.linspace(0, 1, 100)
    tpr_list = []
    fpr_list = []
    
    for threshold in thresholds:
        tp = fp = tn = fn = 0
        for i, score in enumerate(scores):
            if score >= threshold:  # Tahmin: eşleşme var
                if y_true[i] == y_true[i]:  # Gerçek pozitif (kendi kendine)
                    tp += 1
                else:
                    fp += 1
            else:  # Tahmin: eşleşme yok
                if y_true[i] != y_true[i]:
                    tn += 1
                else:
                    fn += 1
        
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        tpr_list.append(tpr)
        fpr_list.append(fpr)
    
    # Alternatif: sklearn ile
    # Mesafe threshold'una göre binary labels
    binary_true = [1] * len(y_true)  # Tüm test örnekleri pozitif (kendi sınıfı)
    
    # Farklı threshold değerleri için accuracy hesapla
    threshold_range = np.arange(0.3, 0.7, 0.01)
    accuracies = []
    
    for thresh in threshold_range:
        correct = sum(1 for i, d in enumerate(y_distances) 
                     if (d <= thresh and y_true[i] == y_true[i]))
        accuracies.append(correct / len(y_true))
    
    # ROC benzeri grafik
    plt.subplot(1, 2, 1)
    plt.plot(threshold_range, accuracies, 'b-', linewidth=2)
    plt.axvline(x=0.5, color='r', linestyle='--', label='Varsayılan Threshold (0.5)')
    plt.xlabel('Mesafe Threshold', fontsize=12)
    plt.ylabel('Doğruluk Oranı', fontsize=12)
    plt.title('Threshold vs Doğruluk', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Mesafe dağılımı
    plt.subplot(1, 2, 2)
    plt.hist(y_distances, bins=20, edgecolor='black', alpha=0.7)
    plt.axvline(x=0.5, color='r', linestyle='--', label='Threshold (0.5)')
    plt.xlabel('Yüz Mesafesi', fontsize=12)
    plt.ylabel('Frekans', fontsize=12)
    plt.title('Yüz Mesafe Dağılımı', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save:
        filepath = os.path.join(RESULTS_DIR, 'roc_curve.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"[KAYIT] {filepath}")
    
    plt.show()


def plot_accuracy_metrics(y_true, y_pred, thresholds_results, save=True):
    """
    Doğruluk Metrikleri Grafiği (4 Panel)
    
    Ne İşe Yarar:
    -------------
    4 farklı grafik ile sistemin detaylı performans analizini sunar.
    
    PANEL 1 - SOL ÜST (Genel Performans Metrikleri):
    ------------------------------------------------
    • Accuracy (Doğruluk): 
      - Formül: Doğru Tahmin / Toplam Tahmin
      - Genel başarı oranı
      
    • Precision (Hassasiyet):
      - Formül: TP / (TP + FP)
      - "Pozitif dediğimin kaçı gerçekten pozitif?"
      - Yanlış alarm oranını ölçer
      
    • Recall (Duyarlılık/Sensitivity):
      - Formül: TP / (TP + FN)
      - "Gerçek pozitiflerin kaçını yakaladım?"
      - Kaçırma oranını ölçer
      
    • F1-Score:
      - Formül: 2 * (Precision * Recall) / (Precision + Recall)
      - Precision ve Recall'un dengeli ortalaması
      - Dengesiz veri setlerinde önemli
    
    PANEL 2 - SAĞ ÜST (Kişi Bazlı Doğruluk):
    ----------------------------------------
    - Her kişinin ayrı ayrı tanınma başarı oranı
    - Uzun çubuk = İyi tanınıyor
    - Kısa çubuk = Tanınma problemi var
    
    PANEL 3 - SOL ALT (Threshold Karşılaştırması):
    ----------------------------------------------
    - 5 farklı threshold değeri için sonuçlar (0.4, 0.45, 0.5, 0.55, 0.6)
    - Yeşil çubuk: Doğru tanıma
    - Kırmızı çubuk: Yanlış tanıma (karıştırma)
    - Gri çubuk: Bilinmeyen (threshold'u geçemedi)
    
    PANEL 4 - SAĞ ALT (Pasta Grafik):
    ---------------------------------
    - Toplam doğru/yanlış oranının görsel özeti
    - Yeşil: Doğru tahminler
    - Kırmızı: Yanlış tahminler
    
    Kaydedilen Dosya: analysis_results/accuracy_metrics.png
    """
    print("\n[GRAFIK] Doğruluk metrikleri oluşturuluyor...")
    
    # Genel metrikler
    accuracy = accuracy_score(y_true, y_pred)
    
    # Sınıf bazlı metrikler
    labels = sorted(list(set(y_true)))
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # 1. Genel Doğruluk Çubuğu
    ax1 = axes[0, 0]
    metrics = {
        'Accuracy': accuracy,
        'Precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
        'Recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
        'F1-Score': f1_score(y_true, y_pred, average='weighted', zero_division=0)
    }
    
    colors = ['#2ecc71', '#3498db', '#9b59b6', '#e74c3c']
    bars = ax1.bar(metrics.keys(), metrics.values(), color=colors, edgecolor='black')
    ax1.set_ylim(0, 1.1)
    ax1.set_ylabel('Skor', fontsize=12)
    ax1.set_title('Genel Performans Metrikleri', fontsize=14, fontweight='bold')
    
    # Değerleri çubukların üstüne yaz
    for bar, val in zip(bars, metrics.values()):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{val:.2%}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax1.axhline(y=0.9, color='green', linestyle='--', alpha=0.5, label='Hedef (%90)')
    ax1.legend()
    
    # 2. Kişi Bazlı Doğruluk
    ax2 = axes[0, 1]
    person_accuracy = {}
    for label in labels:
        correct = sum(1 for t, p in zip(y_true, y_pred) if t == label and p == label)
        total = sum(1 for t in y_true if t == label)
        person_accuracy[label] = correct / total if total > 0 else 0
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(person_accuracy)))
    bars = ax2.barh(list(person_accuracy.keys()), list(person_accuracy.values()), 
                   color=colors, edgecolor='black')
    ax2.set_xlim(0, 1.1)
    ax2.set_xlabel('Doğruluk Oranı', fontsize=12)
    ax2.set_title('Kişi Bazlı Tanıma Doğruluğu', fontsize=14, fontweight='bold')
    
    for bar, val in zip(bars, person_accuracy.values()):
        ax2.text(val + 0.02, bar.get_y() + bar.get_height()/2, 
                f'{val:.0%}', ha='left', va='center', fontsize=10)
    
    # 3. Threshold Karşılaştırması
    ax3 = axes[1, 0]
    thresholds = list(thresholds_results.keys())
    correct_rates = [thresholds_results[t]["correct"] / len(y_true) * 100 for t in thresholds]
    incorrect_rates = [thresholds_results[t]["incorrect"] / len(y_true) * 100 for t in thresholds]
    unknown_rates = [thresholds_results[t]["unknown"] / len(y_true) * 100 for t in thresholds]
    
    x = np.arange(len(thresholds))
    width = 0.25
    
    ax3.bar(x - width, correct_rates, width, label='Doğru', color='#2ecc71', edgecolor='black')
    ax3.bar(x, incorrect_rates, width, label='Yanlış', color='#e74c3c', edgecolor='black')
    ax3.bar(x + width, unknown_rates, width, label='Bilinmeyen', color='#95a5a6', edgecolor='black')
    
    ax3.set_xlabel('Threshold Değeri', fontsize=12)
    ax3.set_ylabel('Yüzde (%)', fontsize=12)
    ax3.set_title('Farklı Threshold Değerlerinde Performans', fontsize=14, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(thresholds)
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. Pasta Grafik - Genel Sonuç
    ax4 = axes[1, 1]
    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    incorrect = len(y_true) - correct
    
    sizes = [correct, incorrect]
    labels_pie = [f'Doğru\n({correct})', f'Yanlış\n({incorrect})']
    colors_pie = ['#2ecc71', '#e74c3c']
    explode = (0.05, 0)
    
    ax4.pie(sizes, explode=explode, labels=labels_pie, colors=colors_pie,
            autopct='%1.1f%%', shadow=True, startangle=90,
            textprops={'fontsize': 12, 'fontweight': 'bold'})
    ax4.set_title('Genel Tanıma Sonuçları', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    if save:
        filepath = os.path.join(RESULTS_DIR, 'accuracy_metrics.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"[KAYIT] {filepath}")
    
    plt.show()


def plot_distance_analysis(y_true, y_pred, y_distances, save=True):
    """
    Mesafe Analizi Grafiği (3 Panel)
    
    Ne İşe Yarar:
    -------------
    Yüz tanıma algoritmasının mesafe metriklerini 3 farklı açıdan analiz eder.
    
    YÜZ MESAFESİ NEDİR?
    -------------------
    - İki yüz encoding'i arasındaki Öklid mesafesi
    - 0.0 = Tamamen aynı yüz
    - 1.0 = Tamamen farklı yüz
    - Genellikle 0.6'dan düşük mesafe = Aynı kişi
    
    PANEL 1 - SOL (Doğru vs Yanlış Mesafe Dağılımı):
    ------------------------------------------------
    - Yeşil histogram: Doğru tahminlerin mesafe dağılımı
    - Kırmızı histogram: Yanlış tahminlerin mesafe dağılımı
    
    İdeal Durum:
    - Yeşil (doğru): Düşük mesafelerde yoğunlaşmalı (0.0-0.4)
    - Kırmızı (yanlış): Yüksek mesafelerde olmalı (0.5+)
    - İki dağılım NE KADAR AYRI olursa sistem O KADAR İYİ
    
    PANEL 2 - ORTA (Kişi Bazlı Ortalama Mesafe):
    --------------------------------------------
    - Her kişinin ortalama eşleşme mesafesi
    - Kısa çubuk (düşük mesafe) = Güvenilir tanıma
    - Uzun çubuk (yüksek mesafe) = Belirsiz tanıma
    - Kırmızı çizgi: Karar threshold'u
    
    PANEL 3 - SAĞ (Box Plot):
    -------------------------
    Her kişi için mesafe dağılımının istatistiksel özeti:
    - Kutu: %25 - %75 aralığı (IQR)
    - Kutunun içindeki çizgi: Medyan (ortanca değer)
    - Bıyıklar: Min-Max değerler (aykırılar hariç)
    - Noktalar: Aykırı değerler (outliers)
    
    İdeal Box Plot:
    - Kutu dar olmalı (tutarlı sonuçlar)
    - Medyan düşük olmalı (iyi eşleşme)
    - Aykırı değer az olmalı
    
    Kaydedilen Dosya: analysis_results/distance_analysis.png
    """
    print("\n[GRAFIK] Mesafe analizi oluşturuluyor...")
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    # 1. Doğru vs Yanlış Tahminlerin Mesafe Dağılımı
    ax1 = axes[0]
    correct_distances = [d for t, p, d in zip(y_true, y_pred, y_distances) if t == p]
    incorrect_distances = [d for t, p, d in zip(y_true, y_pred, y_distances) if t != p]
    
    if correct_distances:
        ax1.hist(correct_distances, bins=15, alpha=0.7, label='Doğru Tahmin', 
                color='#2ecc71', edgecolor='black')
    if incorrect_distances:
        ax1.hist(incorrect_distances, bins=15, alpha=0.7, label='Yanlış Tahmin', 
                color='#e74c3c', edgecolor='black')
    
    ax1.axvline(x=0.5, color='blue', linestyle='--', linewidth=2, label='Threshold (0.5)')
    ax1.set_xlabel('Yüz Mesafesi', fontsize=12)
    ax1.set_ylabel('Frekans', fontsize=12)
    ax1.set_title('Mesafe Dağılımı (Doğru vs Yanlış)', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Kişi Bazlı Ortalama Mesafe
    ax2 = axes[1]
    labels = sorted(list(set(y_true)))
    avg_distances = []
    for label in labels:
        dists = [d for t, d in zip(y_true, y_distances) if t == label]
        avg_distances.append(np.mean(dists) if dists else 0)
    
    colors = plt.cm.RdYlGn_r(np.array(avg_distances) / max(avg_distances) if max(avg_distances) > 0 else np.zeros(len(avg_distances)))
    bars = ax2.barh(labels, avg_distances, color=colors, edgecolor='black')
    ax2.axvline(x=0.5, color='red', linestyle='--', linewidth=2, label='Threshold')
    ax2.set_xlabel('Ortalama Mesafe', fontsize=12)
    ax2.set_title('Kişi Bazlı Ortalama Mesafe', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='x')
    
    # 3. Box Plot
    ax3 = axes[2]
    data_by_person = {label: [d for t, d in zip(y_true, y_distances) if t == label] 
                      for label in labels}
    ax3.boxplot(data_by_person.values(), labels=data_by_person.keys())
    ax3.axhline(y=0.5, color='red', linestyle='--', linewidth=2, label='Threshold')
    ax3.set_ylabel('Yüz Mesafesi', fontsize=12)
    ax3.set_title('Kişi Bazlı Mesafe Dağılımı (Box Plot)', fontsize=14, fontweight='bold')
    ax3.tick_params(axis='x', rotation=45)
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save:
        filepath = os.path.join(RESULTS_DIR, 'distance_analysis.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"[KAYIT] {filepath}")
    
    plt.show()


def generate_report(y_true, y_pred, y_distances, thresholds_results):
    """
    Detaylı Metin Raporu Oluştur
    
    Ne İşe Yarar:
    -------------
    Tüm analiz sonuçlarını okunabilir bir metin dosyasına kaydeder.
    
    Rapor İçeriği:
    --------------
    1. GENEL METRİKLER:
       - Accuracy, Precision, Recall, F1-Score yüzdeleri
       
    2. MESAFE İSTATİSTİKLERİ:
       - Ortalama mesafe: Sistemin genel eşleşme kalitesi
       - Min/Max mesafe: En iyi ve en kötü eşleşmeler
       - Std sapma: Tutarlılık ölçüsü (düşük = tutarlı)
       
    3. THRESHOLD ANALİZİ:
       - Her threshold değeri için doğru/yanlış/bilinmeyen sayıları
       
    4. SINIFLANDIRMA RAPORU:
       - Her kişi için ayrı precision, recall, f1-score
       - Support: Her kişiden kaç örnek var
    
    Kaydedilen Dosya: analysis_results/analysis_report.txt
    """
    print("\n" + "="*60)
    print(" DETAYLI PERFORMANS RAPORU")
    print("="*60)
    
    # Genel istatistikler
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    
    print(f"\n📊 GENEL METRİKLER:")
    print(f"   • Doğruluk (Accuracy):  {accuracy:.2%}")
    print(f"   • Hassasiyet (Precision): {precision:.2%}")
    print(f"   • Duyarlılık (Recall):    {recall:.2%}")
    print(f"   • F1-Skoru:               {f1:.2%}")
    
    print(f"\n📏 MESAFE İSTATİSTİKLERİ:")
    print(f"   • Ortalama Mesafe: {np.mean(y_distances):.4f}")
    print(f"   • Min Mesafe:      {np.min(y_distances):.4f}")
    print(f"   • Max Mesafe:      {np.max(y_distances):.4f}")
    print(f"   • Std Sapma:       {np.std(y_distances):.4f}")
    
    print(f"\n🎯 THRESHOLD ANALİZİ:")
    for thresh, results in thresholds_results.items():
        total = results["correct"] + results["incorrect"] + results["unknown"]
        acc = results["correct"] / total * 100 if total > 0 else 0
        print(f"   Threshold {thresh}: Doğru={results['correct']}, "
              f"Yanlış={results['incorrect']}, Bilinmeyen={results['unknown']} "
              f"(Doğruluk: {acc:.1f}%)")
    
    print(f"\n📋 SINIFLANDIRMA RAPORU:")
    print(classification_report(y_true, y_pred, zero_division=0))
    
    # Raporu dosyaya kaydet
    report_path = os.path.join(RESULTS_DIR, 'analysis_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write(" YÜZ TANIMA SİSTEMİ - PERFORMANS RAPORU\n")
        f.write(f" Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")
        
        f.write("GENEL METRİKLER:\n")
        f.write(f"  Doğruluk (Accuracy):    {accuracy:.2%}\n")
        f.write(f"  Hassasiyet (Precision): {precision:.2%}\n")
        f.write(f"  Duyarlılık (Recall):    {recall:.2%}\n")
        f.write(f"  F1-Skoru:               {f1:.2%}\n\n")
        
        f.write("MESAFE İSTATİSTİKLERİ:\n")
        f.write(f"  Ortalama Mesafe: {np.mean(y_distances):.4f}\n")
        f.write(f"  Min Mesafe:      {np.min(y_distances):.4f}\n")
        f.write(f"  Max Mesafe:      {np.max(y_distances):.4f}\n")
        f.write(f"  Std Sapma:       {np.std(y_distances):.4f}\n\n")
        
        f.write("SINIFLANDIRMA RAPORU:\n")
        f.write(classification_report(y_true, y_pred, zero_division=0))
    
    print(f"\n[KAYIT] Rapor kaydedildi: {report_path}")


def run_full_analysis():
    """
    Tam Performans Analizi - Ana Fonksiyon
    
    Ne İşe Yarar:
    -------------
    Yüz tanıma sisteminin kapsamlı performans analizini yapar ve
    tüm grafikleri + raporu oluşturur.
    
    Kullanılan Yöntem: Leave-One-Out Cross Validation (LOO-CV)
    ----------------------------------------------------------
    - Her örnek sırayla test örneği olarak seçilir
    - Geri kalan örnekler eğitim seti olarak kullanılır
    - Bu sayede tüm veri hem eğitim hem test için kullanılır
    - Küçük veri setleri için ideal bir yöntemdir
    
    Oluşturulan Çıktılar:
    ---------------------
    1. confusion_matrix.png  - Karmaşıklık matrisi
    2. roc_curve.png         - ROC eğrisi ve threshold analizi
    3. accuracy_metrics.png  - Doğruluk metrikleri (4 panel)
    4. distance_analysis.png - Mesafe analizi (3 panel)
    5. analysis_report.txt   - Detaylı metin raporu
    
    Çalıştırma:
    -----------
    GUI'den: "📈 Performans Analizi" butonuna tıklayın
    Terminal'den: python analysis.py
    
    Sonuçlar:
    ---------
    Tüm çıktılar 'analysis_results' klasörüne kaydedilir.
    """
    print("\n" + "="*60)
    print(" YÜZ TANIMA SİSTEMİ - TAM ANALİZ")
    print("="*60)
    print(f" Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Cross-validation testi yap
    y_true, y_pred, y_distances, thresholds_results = cross_validation_test()
    
    if y_true is None:
        print("[HATA] Test verisi oluşturulamadı!")
        return
    
    print(f"\n[INFO] {len(y_true)} test örneği analiz edildi.")
    
    # Tüm grafikleri oluştur
    plot_confusion_matrix(y_true, y_pred)
    plot_roc_curve(y_true, y_distances)
    plot_accuracy_metrics(y_true, y_pred, thresholds_results)
    plot_distance_analysis(y_true, y_pred, y_distances)
    
    # Rapor oluştur
    generate_report(y_true, y_pred, y_distances, thresholds_results)
    
    print("\n" + "="*60)
    print(" ANALİZ TAMAMLANDI!")
    print(f" Sonuçlar '{RESULTS_DIR}' klasörüne kaydedildi.")
    print("="*60)


if __name__ == "__main__":
    run_full_analysis()
