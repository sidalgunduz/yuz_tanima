# -*- coding: utf-8 -*-
"""
==============================================================================
UTILS.PY - YARDIMCI FONKSİYONLAR MODÜLÜ
==============================================================================
Bu modül, Yüz Tanıma Yoklama Sistemi için yardımcı fonksiyonları içerir.

İçerik:
- Excel dosya işlemleri (oluşturma, okuma, yazma)
- Dosya yönetimi fonksiyonları
- Tarih/saat formatlama
- Yüz tanıma yardımcı fonksiyonları

Yazar: Senior Python Computer Vision Engineer
Tarih: 2025
Python Sürümü: 3.10+
==============================================================================
"""

# ============================================================================
# KÜTÜPHANE İMPORTLARI
# ============================================================================
import os
import pickle
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

import pandas as pd
import numpy as np

# ============================================================================
# SABİT DEĞERLER (CONSTANTS)
# ============================================================================
# Proje ana dizini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Alt klasör yolları
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
ENCODINGS_DIR = os.path.join(BASE_DIR, "encodings")
ATTENDANCE_DIR = os.path.join(BASE_DIR, "attendance")

# Dosya isimleri
ENCODINGS_FILE = os.path.join(ENCODINGS_DIR, "face_encodings.pickle")

# Excel sütun başlıkları
EXCEL_COLUMNS = ["Ad Soyad", "Numara", "Tarih", "Saat", "Durum"]

# Durum mesajları
STATUS_PRESENT = "Geldi"
STATUS_ABSENT = "Gelmedi"
STATUS_DUPLICATE = "Tekrar Giriş Engellendi"


# ============================================================================
# KLASÖR YÖNETİMİ FONKSİYONLARI
# ============================================================================
def ensure_directories_exist() -> None:
    """
    Proje için gerekli tüm klasörlerin var olduğundan emin olur.
    Eğer klasörler yoksa otomatik olarak oluşturur.
    
    Returns:
        None
        
    Raises:
        OSError: Klasör oluşturma başarısız olursa
    """
    directories = [DATASET_DIR, ENCODINGS_DIR, ATTENDANCE_DIR]
    
    for directory in directories:
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"[INFO] Klasör oluşturuldu: {directory}")
            else:
                print(f"[INFO] Klasör mevcut: {directory}")
        except OSError as e:
            print(f"[HATA] Klasör oluşturulamadı: {directory}")
            print(f"[HATA] Detay: {str(e)}")
            raise


# ============================================================================
# TARİH/SAAT FONKSİYONLARI
# ============================================================================
def get_current_date() -> str:
    """
    Güncel tarihi YYYY_MM_DD formatında döndürür.
    Excel dosya isimlendirmesi için kullanılır.
    
    Returns:
        str: "2025_01_03" formatında tarih
    """
    return datetime.now().strftime("%Y_%m_%d")


def get_current_date_formatted() -> str:
    """
    Güncel tarihi DD.MM.YYYY formatında döndürür.
    Excel içeriği için kullanılır.
    
    Returns:
        str: "03.01.2025" formatında tarih
    """
    return datetime.now().strftime("%d.%m.%Y")


def get_current_time() -> str:
    """
    Güncel saati HH:MM:SS formatında döndürür.
    
    Returns:
        str: "14:30:45" formatında saat
    """
    return datetime.now().strftime("%H:%M:%S")


def get_current_datetime() -> Tuple[str, str]:
    """
    Güncel tarih ve saati tuple olarak döndürür.
    
    Returns:
        Tuple[str, str]: (tarih, saat) formatında tuple
    """
    return get_current_date_formatted(), get_current_time()


# ============================================================================
# EXCEL DOSYA İŞLEMLERİ
# ============================================================================
def get_attendance_file_path() -> str:
    """
    Günün yoklama dosyasının tam yolunu döndürür.
    Dosya formatı: yoklama_YYYY_MM_DD.xlsx
    
    Returns:
        str: Excel dosyasının tam yolu
    """
    filename = f"yoklama_{get_current_date()}.xlsx"
    return os.path.join(ATTENDANCE_DIR, filename)


def create_or_load_attendance_excel() -> pd.DataFrame:
    """
    Günün yoklama Excel dosyasını yükler veya yeni oluşturur.
    
    Eğer dosya mevcutsa:
        - Mevcut veriyi DataFrame olarak yükler
    Eğer dosya yoksa:
        - Boş DataFrame oluşturur
        - Sütun başlıklarını ekler
    
    Returns:
        pd.DataFrame: Yoklama verileri içeren DataFrame
        
    Raises:
        Exception: Dosya okuma/yazma hatası
    """
    file_path = get_attendance_file_path()
    
    try:
        if os.path.exists(file_path):
            # Mevcut Excel dosyasını oku
            df = pd.read_excel(file_path, engine='openpyxl')
            print(f"[INFO] Mevcut yoklama dosyası yüklendi: {file_path}")
            return df
        else:
            # Yeni boş DataFrame oluştur
            df = pd.DataFrame(columns=EXCEL_COLUMNS)
            # Dosyayı kaydet
            df.to_excel(file_path, index=False, engine='openpyxl')
            print(f"[INFO] Yeni yoklama dosyası oluşturuldu: {file_path}")
            return df
            
    except Exception as e:
        print(f"[HATA] Excel dosyası işlenirken hata: {str(e)}")
        # Hata durumunda boş DataFrame döndür
        return pd.DataFrame(columns=EXCEL_COLUMNS)


def is_already_marked(df: pd.DataFrame, student_id: str) -> bool:
    """
    Öğrencinin bugün için zaten yoklamaya kaydedilip kaydedilmediğini kontrol eder.
    Çift kayıt engelleme mekanizması.
    
    Args:
        df: Yoklama DataFrame'i
        student_id: Öğrenci numarası (string)
        
    Returns:
        bool: True ise zaten kayıtlı, False ise kayıtlı değil
    """
    if df.empty:
        return False
    
    # Öğrenci numarasını string olarak karşılaştır
    # ve bugünün tarihiyle eşleşen kayıt var mı kontrol et
    today = get_current_date_formatted()
    
    # Numara sütununu string'e çevir
    df['Numara'] = df['Numara'].astype(str)
    
    # Bugün bu öğrenci kaydedilmiş mi?
    existing = df[(df['Numara'] == str(student_id)) & (df['Tarih'] == today)]
    
    return len(existing) > 0


def mark_attendance(
    student_name: str, 
    student_id: str, 
    status: str = STATUS_PRESENT
) -> Tuple[bool, str]:
    """
    Öğrenci yoklamasını Excel'e kaydeder.
    
    İşlem adımları:
    1. Mevcut Excel dosyasını yükle veya oluştur
    2. Öğrencinin bugün zaten kaydedilip kaydedilmediğini kontrol et
    3. Kayıtlı değilse yeni satır ekle
    4. Excel dosyasını kaydet
    
    Args:
        student_name: Öğrenci ad soyad
        student_id: Öğrenci numarası
        status: Durum mesajı (varsayılan: "Geldi")
        
    Returns:
        Tuple[bool, str]: (başarı_durumu, mesaj)
        
    Example:
        >>> success, msg = mark_attendance("Ali Yılmaz", "123")
        >>> print(msg)
        "Ali Yılmaz yoklamaya kaydedildi."
    """
    try:
        # Excel dosyasını yükle
        df = create_or_load_attendance_excel()
        
        # Çift kayıt kontrolü
        if is_already_marked(df, student_id):
            message = f"[UYARI] {student_name} ({student_id}) bugün zaten kayıtlı!"
            print(message)
            return False, message
        
        # Tarih ve saat bilgisini al
        current_date, current_time = get_current_datetime()
        
        # Yeni kayıt oluştur
        new_record = {
            "Ad Soyad": student_name,
            "Numara": student_id,
            "Tarih": current_date,
            "Saat": current_time,
            "Durum": status
        }
        
        # DataFrame'e ekle
        df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
        
        # Excel'e kaydet
        file_path = get_attendance_file_path()
        df.to_excel(file_path, index=False, engine='openpyxl')
        
        message = f"[BAŞARILI] {student_name} ({student_id}) yoklamaya kaydedildi."
        print(message)
        return True, message
        
    except Exception as e:
        message = f"[HATA] Yoklama kaydedilemedi: {str(e)}"
        print(message)
        return False, message


def get_attendance_summary() -> Dict[str, Any]:
    """
    Günün yoklama özetini döndürür.
    
    Returns:
        Dict: {
            'total': Toplam kayıt sayısı,
            'present': Gelen öğrenci sayısı,
            'file_path': Dosya yolu,
            'students': Kayıtlı öğrenci listesi
        }
    """
    try:
        df = create_or_load_attendance_excel()
        
        summary = {
            'total': len(df),
            'present': len(df[df['Durum'] == STATUS_PRESENT]) if not df.empty else 0,
            'file_path': get_attendance_file_path(),
            'students': df['Ad Soyad'].tolist() if not df.empty else []
        }
        
        return summary
        
    except Exception as e:
        print(f"[HATA] Özet alınamadı: {str(e)}")
        return {
            'total': 0,
            'present': 0,
            'file_path': get_attendance_file_path(),
            'students': []
        }


# ============================================================================
# YÜZ ENCODING İŞLEMLERİ
# ============================================================================
def save_encodings(
    encodings: List[np.ndarray], 
    names: List[str], 
    ids: List[str]
) -> bool:
    """
    Yüz encoding'lerini pickle dosyasına kaydeder.
    
    Args:
        encodings: 128-D yüz encoding vektörleri listesi
        names: Öğrenci isimleri listesi
        ids: Öğrenci numaraları listesi
        
    Returns:
        bool: Başarılı ise True
    """
    try:
        # Klasörün var olduğundan emin ol
        ensure_directories_exist()
        
        # Veri yapısını oluştur
        data = {
            "encodings": encodings,
            "names": names,
            "ids": ids
        }
        
        # Pickle olarak kaydet
        with open(ENCODINGS_FILE, "wb") as f:
            pickle.dump(data, f)
        
        print(f"[BAŞARILI] {len(encodings)} yüz encoding'i kaydedildi: {ENCODINGS_FILE}")
        return True
        
    except Exception as e:
        print(f"[HATA] Encoding'ler kaydedilemedi: {str(e)}")
        return False


def load_encodings() -> Optional[Dict[str, List]]:
    """
    Kaydedilmiş yüz encoding'lerini pickle dosyasından yükler.
    
    Returns:
        Dict veya None: {
            'encodings': [encoding1, encoding2, ...],
            'names': ['Ad1', 'Ad2', ...],
            'ids': ['123', '124', ...]
        }
        Dosya yoksa veya hata olursa None döner.
    """
    try:
        if not os.path.exists(ENCODINGS_FILE):
            print(f"[UYARI] Encoding dosyası bulunamadı: {ENCODINGS_FILE}")
            print("[UYARI] Önce encode_faces.py çalıştırarak encoding'leri oluşturun.")
            return None
        
        with open(ENCODINGS_FILE, "rb") as f:
            data = pickle.load(f)
        
        print(f"[INFO] {len(data['encodings'])} yüz encoding'i yüklendi.")
        return data
        
    except Exception as e:
        print(f"[HATA] Encoding'ler yüklenemedi: {str(e)}")
        return None


# ============================================================================
# DATASET FONKSİYONLARI
# ============================================================================
def get_dataset_images() -> List[Tuple[str, str, str]]:
    """
    Dataset klasöründeki tüm resimleri listeler.
    
    Dosya adı formatı: NUMARA_ADSOYAD.jpg (örn: 123_Ali_Yilmaz.jpg)
    
    Returns:
        List[Tuple[str, str, str]]: [(dosya_yolu, numara, ad_soyad), ...]
        
    Raises:
        ValueError: Geçersiz dosya adı formatı
    """
    images = []
    
    # Desteklenen resim formatları
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    
    try:
        if not os.path.exists(DATASET_DIR):
            print(f"[UYARI] Dataset klasörü bulunamadı: {DATASET_DIR}")
            return images
        
        for filename in os.listdir(DATASET_DIR):
            # Uzantı kontrolü
            if not filename.lower().endswith(valid_extensions):
                continue
            
            # Dosya adını parse et (NUMARA_ADSOYAD.uzanti)
            name_part = os.path.splitext(filename)[0]
            parts = name_part.split('_', 1)
            
            if len(parts) >= 2:
                student_id = parts[0]
                student_name = parts[1].replace('_', ' ')
                file_path = os.path.join(DATASET_DIR, filename)
                
                images.append((file_path, student_id, student_name))
                print(f"[INFO] Bulundu: {student_name} ({student_id})")
            else:
                print(f"[UYARI] Geçersiz dosya adı formatı: {filename}")
                print("[UYARI] Format: NUMARA_ADSOYAD.jpg olmalı")
        
        print(f"[INFO] Toplam {len(images)} resim bulundu.")
        return images
        
    except Exception as e:
        print(f"[HATA] Dataset okunamadı: {str(e)}")
        return images


def parse_filename(filename: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Dosya adından öğrenci numarası ve adını çıkarır.
    
    Args:
        filename: Dosya adı (örn: "123_Ali_Yilmaz.jpg")
        
    Returns:
        Tuple[str, str]: (numara, ad_soyad) veya (None, None) hata durumunda
    """
    try:
        name_part = os.path.splitext(filename)[0]
        parts = name_part.split('_', 1)
        
        if len(parts) >= 2:
            student_id = parts[0]
            student_name = parts[1].replace('_', ' ')
            return student_id, student_name
        else:
            return None, None
            
    except Exception:
        return None, None


# ============================================================================
# GÖRÜNTÜ İŞLEME YARDIMCI FONKSİYONLARI
# ============================================================================
def resize_frame(frame: np.ndarray, scale: float = 0.25) -> np.ndarray:
    """
    Kamera karesini performans için küçültür.
    
    Args:
        frame: OpenCV görüntü dizisi
        scale: Küçültme oranı (varsayılan 0.25 = %25)
        
    Returns:
        np.ndarray: Küçültülmüş görüntü
    """
    import cv2
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    return cv2.resize(frame, (width, height))


def convert_bgr_to_rgb(frame: np.ndarray) -> np.ndarray:
    """
    OpenCV BGR formatını RGB formatına çevirir.
    face_recognition kütüphanesi RGB format kullanır.
    
    Args:
        frame: BGR formatında görüntü
        
    Returns:
        np.ndarray: RGB formatında görüntü
    """
    import cv2
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


# ============================================================================
# YARDIMCI YAZDIRMA FONKSİYONLARI
# ============================================================================
def print_header(text: str) -> None:
    """
    Formatlı başlık yazdırır.
    """
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)


def print_info(text: str) -> None:
    """
    Bilgi mesajı yazdırır.
    """
    print(f"[INFO] {text}")


def print_success(text: str) -> None:
    """
    Başarı mesajı yazdırır.
    """
    print(f"[BAŞARILI] {text}")


def print_warning(text: str) -> None:
    """
    Uyarı mesajı yazdırır.
    """
    print(f"[UYARI] {text}")


def print_error(text: str) -> None:
    """
    Hata mesajı yazdırır.
    """
    print(f"[HATA] {text}")


# ============================================================================
# MODÜL TEST KODU
# ============================================================================
if __name__ == "__main__":
    """
    Bu dosya doğrudan çalıştırıldığında test işlemleri yapar.
    """
    print_header("UTILS.PY TEST")
    
    # Klasörleri oluştur
    print("\n[TEST] Klasör yapısı kontrol ediliyor...")
    ensure_directories_exist()
    
    # Tarih/saat test
    print("\n[TEST] Tarih/Saat fonksiyonları:")
    print(f"  Tarih (dosya): {get_current_date()}")
    print(f"  Tarih (görüntü): {get_current_date_formatted()}")
    print(f"  Saat: {get_current_time()}")
    
    # Excel test
    print("\n[TEST] Excel dosyası:")
    print(f"  Dosya yolu: {get_attendance_file_path()}")
    
    # Özet
    print("\n[TEST] Yoklama özeti:")
    summary = get_attendance_summary()
    print(f"  Toplam kayıt: {summary['total']}")
    print(f"  Gelen öğrenci: {summary['present']}")
    
    print("\n" + "=" * 60)
    print(" TEST TAMAMLANDI")
    print("=" * 60)
