# -*- coding: utf-8 -*-
"""
==============================================================================
ENCODE_FACES.PY - YÜZ ENCODING OLUŞTURMA MODÜLÜ
==============================================================================
Bu modül, dataset klasöründeki öğrenci fotoğraflarından yüz encoding'leri 
oluşturur ve pickle dosyasına kaydeder.

İşlem Adımları:
1. Dataset klasöründeki tüm resimleri tara
2. Her resimden yüz bul
3. 128-D yüz encoding vektörü oluştur
4. Tüm encoding'leri pickle dosyasına kaydet

Dosya Adı Formatı:
- Dataset'teki dosyalar: NUMARA_ADSOYAD.jpg
- Örnek: 123_Ali_Yilmaz.jpg, 124_Ayse_Kaya.png

Yazar: Senior Python Computer Vision Engineer
Tarih: 2025
Python Sürümü: 3.10+
==============================================================================
"""

# ============================================================================
# KÜTÜPHANE İMPORTLARI
# ============================================================================
import os
import sys
import cv2
import numpy as np

# face_recognition kütüphanesini import et
# Bu kütüphane yüz algılama ve encoding işlemleri için kullanılır
try:
    import face_recognition
except ImportError:
    print("[HATA] face_recognition kütüphanesi bulunamadı!")
    print("[ÇÖZÜM] Kurulum için: pip install face_recognition")
    print("[NOT] Windows'ta cmake ve dlib kurulumu gerekebilir.")
    sys.exit(1)

# Proje yardımcı fonksiyonlarını import et
from utils import (
    DATASET_DIR,
    get_dataset_images,
    save_encodings,
    ensure_directories_exist,
    print_header,
    print_info,
    print_success,
    print_warning,
    print_error
)


# ============================================================================
# ANA ENCODING FONKSİYONU
# ============================================================================
def encode_faces_from_dataset() -> tuple:
    """
    Dataset klasöründeki tüm resimlerden yüz encoding'leri oluşturur.
    
    İşlem Akışı:
    1. Dataset klasörünü tara
    2. Her resim için:
       a. Resmi yükle
       b. Yüz lokasyonunu bul
       c. 128-D encoding vektörü hesapla
       d. Listeye ekle
    3. Tüm encoding'leri pickle'a kaydet
    
    Returns:
        tuple: (encodings_list, names_list, ids_list)
        
    Raises:
        ValueError: Hiç yüz bulunamazsa
    """
    print_header("YÜZ ENCODING OLUŞTURMA")
    
    # Klasörlerin var olduğundan emin ol
    ensure_directories_exist()
    
    # Dataset'teki resimleri al
    images = get_dataset_images()
    
    if not images:
        print_error("Dataset klasöründe hiç resim bulunamadı!")
        print_info(f"Lütfen {DATASET_DIR} klasörüne öğrenci fotoğrafları ekleyin.")
        print_info("Dosya formatı: NUMARA_ADSOYAD.jpg")
        print_info("Örnek: 123_Ali_Yilmaz.jpg")
        return [], [], []
    
    # Encoding'leri saklamak için listeler
    all_encodings = []
    all_names = []
    all_ids = []
    
    # İşlem sayaçları
    success_count = 0
    fail_count = 0
    
    print(f"\n[INFO] {len(images)} resim işlenecek...\n")
    print("-" * 60)
    
    # Her resmi işle
    for idx, (file_path, student_id, student_name) in enumerate(images, 1):
        try:
            print(f"\n[{idx}/{len(images)}] İşleniyor: {student_name} ({student_id})")
            
            # ================================================================
            # ADIM 1: RESMİ YÜKLE
            # ================================================================
            # face_recognition.load_image_file() RGB formatında yükler
            image = face_recognition.load_image_file(file_path)
            print(f"  [✓] Resim yüklendi: {os.path.basename(file_path)}")
            
            # ================================================================
            # ADIM 2: YÜZ LOKASYONLARINI BUL
            # ================================================================
            # face_locations() fonksiyonu resimdeki tüm yüzleri bulur
            # model="hog" CPU için hızlı, model="cnn" GPU için daha doğru
            face_locations = face_recognition.face_locations(image, model="hog")
            
            if not face_locations:
                print(f"  [✗] UYARI: Bu resimde yüz bulunamadı!")
                print(f"  [!] Dosya atlanıyor: {file_path}")
                fail_count += 1
                continue
            
            if len(face_locations) > 1:
                print(f"  [!] UYARI: {len(face_locations)} yüz bulundu, ilki kullanılacak.")
            
            print(f"  [✓] Yüz lokasyonu bulundu")
            
            # ================================================================
            # ADIM 3: 128-D ENCODING VEKTÖRÜ OLUŞTUR
            # ================================================================
            # face_encodings() fonksiyonu her yüz için 128 boyutlu 
            # benzersiz bir vektör oluşturur
            encodings = face_recognition.face_encodings(image, face_locations)
            
            if not encodings:
                print(f"  [✗] UYARI: Encoding oluşturulamadı!")
                fail_count += 1
                continue
            
            # İlk yüzün encoding'ini al
            face_encoding = encodings[0]
            print(f"  [✓] 128-D encoding vektörü oluşturuldu")
            
            # ================================================================
            # ADIM 4: LİSTELERE EKLE
            # ================================================================
            all_encodings.append(face_encoding)
            all_names.append(student_name)
            all_ids.append(student_id)
            
            success_count += 1
            print(f"  [✓] Başarıyla kaydedildi!")
            
        except FileNotFoundError:
            print_error(f"Dosya bulunamadı: {file_path}")
            fail_count += 1
            
        except Exception as e:
            print_error(f"İşlem hatası: {str(e)}")
            fail_count += 1
    
    # ================================================================
    # ÖZET VE KAYIT
    # ================================================================
    print("\n" + "-" * 60)
    print_header("ENCODING İŞLEMİ TAMAMLANDI")
    
    print(f"\n  Toplam resim sayısı:    {len(images)}")
    print(f"  Başarılı encoding:      {success_count}")
    print(f"  Başarısız/Atlanan:      {fail_count}")
    
    if all_encodings:
        # Encoding'leri pickle dosyasına kaydet
        save_success = save_encodings(all_encodings, all_names, all_ids)
        
        if save_success:
            print_success(f"\n{success_count} öğrenci encoding'i başarıyla kaydedildi!")
            print_info("Artık main.py ile yüz tanıma yapabilirsiniz.")
        else:
            print_error("Encoding'ler kaydedilemedi!")
    else:
        print_warning("Hiçbir encoding oluşturulamadı!")
        print_info("Dataset klasörüne yüz içeren fotoğraflar eklediğinizden emin olun.")
    
    return all_encodings, all_names, all_ids


def validate_dataset() -> bool:
    """
    Dataset klasörünün geçerli olup olmadığını kontrol eder.
    
    Kontroller:
    1. Klasör var mı?
    2. İçinde resim dosyası var mı?
    3. Dosya isimleri doğru formatta mı?
    
    Returns:
        bool: Geçerli ise True
    """
    print_info("Dataset doğrulanıyor...")
    
    # Klasör kontrolü
    if not os.path.exists(DATASET_DIR):
        print_error(f"Dataset klasörü bulunamadı: {DATASET_DIR}")
        return False
    
    # İçerik kontrolü
    files = os.listdir(DATASET_DIR)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    
    if not image_files:
        print_error("Dataset klasöründe resim dosyası bulunamadı!")
        return False
    
    print_success(f"{len(image_files)} resim dosyası bulundu.")
    
    # Format kontrolü
    valid_count = 0
    for filename in image_files:
        name_part = os.path.splitext(filename)[0]
        parts = name_part.split('_', 1)
        
        if len(parts) >= 2 and parts[0].isdigit():
            valid_count += 1
        else:
            print_warning(f"Geçersiz format: {filename}")
            print_info("  Beklenen format: NUMARA_ADSOYAD.jpg")
    
    if valid_count == 0:
        print_error("Hiçbir dosya geçerli formatta değil!")
        return False
    
    print_success(f"{valid_count}/{len(image_files)} dosya geçerli formatta.")
    return True


def show_dataset_info():
    """
    Dataset hakkında bilgi gösterir.
    """
    print_header("DATASET BİLGİSİ")
    
    print(f"\n  Klasör: {DATASET_DIR}")
    
    images = get_dataset_images()
    
    if images:
        print(f"\n  Kayıtlı Öğrenciler ({len(images)} kişi):")
        print("  " + "-" * 40)
        
        for file_path, student_id, student_name in images:
            print(f"  • {student_name} (No: {student_id})")
    else:
        print("\n  [!] Dataset klasörü boş veya resim bulunamadı.")
        print("\n  Kullanım:")
        print(f"  1. {DATASET_DIR} klasörüne fotoğraf ekleyin")
        print("  2. Dosya adı formatı: NUMARA_ADSOYAD.jpg")
        print("  3. Örnek: 123_Ali_Yilmaz.jpg, 124_Ayse_Kaya.png")


# ============================================================================
# ANA PROGRAM
# ============================================================================
if __name__ == "__main__":
    """
    Script doğrudan çalıştırıldığında encoding işlemini başlatır.
    
    Kullanım:
        python encode_faces.py
        
    veya
        python encode_faces.py --info    # Dataset bilgisi göster
        python encode_faces.py --validate # Dataset'i doğrula
    """
    print("\n" + "=" * 60)
    print(" YÜZ TANIMA YOKLAMA SİSTEMİ - ENCODING MODÜLÜ")
    print("=" * 60)
    
    # Komut satırı argümanları
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--info', '-i']:
            show_dataset_info()
            sys.exit(0)
            
        elif arg in ['--validate', '-v']:
            is_valid = validate_dataset()
            sys.exit(0 if is_valid else 1)
            
        elif arg in ['--help', '-h']:
            print("\nKullanım:")
            print("  python encode_faces.py           # Encoding oluştur")
            print("  python encode_faces.py --info    # Dataset bilgisi")
            print("  python encode_faces.py --validate # Dataset doğrula")
            print("  python encode_faces.py --help    # Bu yardım")
            sys.exit(0)
    
    # Dataset kontrolü
    if not validate_dataset():
        print("\n[!] Dataset hazır değil. Lütfen fotoğrafları ekleyin.")
        print(f"[!] Klasör: {DATASET_DIR}")
        print("[!] Format: NUMARA_ADSOYAD.jpg")
        sys.exit(1)
    
    # Kullanıcı onayı
    print("\n[?] Encoding işlemi başlatılsın mı? (E/h): ", end="")
    try:
        response = input().strip().lower()
        if response in ['', 'e', 'evet', 'y', 'yes']:
            # Encoding işlemini başlat
            encodings, names, ids = encode_faces_from_dataset()
            
            if encodings:
                print("\n" + "=" * 60)
                print(" İŞLEM BAŞARILI!")
                print(" Artık 'python main.py' ile yüz tanıma yapabilirsiniz.")
                print("=" * 60 + "\n")
            else:
                print("\n[!] Encoding oluşturulamadı. Lütfen hataları kontrol edin.\n")
        else:
            print("[INFO] İşlem iptal edildi.")
            
    except KeyboardInterrupt:
        print("\n\n[INFO] İşlem kullanıcı tarafından iptal edildi.")
        sys.exit(0)
