# -*- coding: utf-8 -*-
"""
==============================================================================
MAIN.PY - YÜZ TANIMA YOKLAMA SİSTEMİ ANA MODÜLÜ
==============================================================================
"""

import os
import sys
import cv2
import numpy as np
from typing import List, Tuple
from datetime import datetime

try:
    import face_recognition
except ImportError:
    print("[HATA] face_recognition bulunamadı! pip install face_recognition")
    sys.exit(1)

from utils import (
    load_encodings,
    mark_attendance,
    get_attendance_summary,
    ensure_directories_exist,
    print_header,
    print_info,
    print_success,
    print_warning,
    print_error,
)

# Kamera ayarları
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Performans
PROCESS_EVERY_N_FRAMES = 4
SCALE_FACTOR = 0.25

# Eşleşme hassasiyeti
FACE_MATCH_TOLERANCE = 0.50

# Renkler
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)

FONT = cv2.FONT_HERSHEY_SIMPLEX


# ============================================================
# 📌 GÖRÜNTÜ ÖN İŞLEME
# ============================================================
def preprocess_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    rgb = cv2.cvtColor(gray_bgr, cv2.COLOR_BGR2RGB)
    return rgb


# ============================================================
# ANA SINIF
# ============================================================
class FaceRecognitionAttendance:

    def __init__(self):
        print_header("YÜZ TANIMA YOKLAMA SİSTEMİ")
        ensure_directories_exist()

        if not os.path.exists("unknown"):
            os.makedirs("unknown")

        self.known_encodings = []
        self.known_names = []
        self.known_ids = []
        self.marked_today = set()  # 🔥 Bugün kaydedilenler
        self.unknown_saved = False  # 🔥 Bilinmeyen kişi kaydedildi mi
        self.camera = None
        self.frame_count = 0

        self._load_face_data()

    # --------------------------------------------------------
    def _load_face_data(self):
        print_info("Encoding verileri yükleniyor...")

        data = load_encodings()
        if data is None:
            print_error("Encoding dosyası bulunamadı!")
            return False

        self.known_encodings = data["encodings"]
        self.known_names = data["names"]
        self.known_ids = data["ids"]

        print_success(f"{len(self.known_encodings)} öğrenci yüklendi.")
        for name, sid in zip(self.known_names, self.known_ids):
            print(f"  • {name} (No: {sid})")
        return True

    # --------------------------------------------------------
    def _init_camera(self):
        self.camera = cv2.VideoCapture(CAMERA_INDEX)

        if not self.camera.isOpened():
            print_error("Kamera açılamadı!")
            return False

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        return True

    # --------------------------------------------------------
    # 🔥 YENİ — SADECE 1 KEZ KAYIT!
    def _mark_student_attendance(self, name, student_id):

        # ➤ Eğer öğrenci bugün zaten kaydedildiyse hiçbir şey yapma!
        if student_id in self.marked_today:
            return  

        # ➤ İlk defa görülüyorsa Excel’e Giriş yaz
        success, msg = mark_attendance(name, student_id, "Geldi")
        if success:
            self.marked_today.add(student_id)
            print_success(f"GİRİŞ → {name} ({student_id})")

    # --------------------------------------------------------
    def _process_frame(self, frame):
        small = cv2.resize(frame, (0, 0), fx=SCALE_FACTOR, fy=SCALE_FACTOR)
        rgb_small = preprocess_frame(small)

        face_locations = face_recognition.face_locations(rgb_small)
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

        recognized = []

        for encoding, loc in zip(face_encodings, face_locations):

            matches = face_recognition.compare_faces(
                self.known_encodings, encoding, tolerance=FACE_MATCH_TOLERANCE
            )

            name = "Bilinmeyen"
            sid = None

            distances = face_recognition.face_distance(self.known_encodings, encoding)
            if len(distances) > 0:
                best = np.argmin(distances)

                if matches[best]:
                    name = self.known_names[best]
                    sid = self.known_ids[best]
                    self._mark_student_attendance(name, sid)

                else:
                    # Bilinmeyeni sadece 1 kez kaydet
                    if not self.unknown_saved:
                        top, right, bottom, left = loc
                        top = int(top / SCALE_FACTOR)
                        right = int(right / SCALE_FACTOR)
                        bottom = int(bottom / SCALE_FACTOR)
                        left = int(left / SCALE_FACTOR)

                        face_img = frame[top:bottom, left:right]
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        cv2.imwrite(f"unknown/unknown_{timestamp}.jpg", face_img)

                        print_warning("Bilinmeyen kişi tespit edildi – fotoğraf kaydedildi.")
                        self.unknown_saved = True

            recognized.append((name, sid))

        scaled = []
        for (top, right, bottom, left) in face_locations:
            scaled.append(
                (
                    int(top / SCALE_FACTOR),
                    int(right / SCALE_FACTOR),
                    int(bottom / SCALE_FACTOR),
                    int(left / SCALE_FACTOR),
                )
            )

        return scaled, recognized

    # --------------------------------------------------------
    def _draw_results(self, frame, face_locations, recognized):
        for (top, right, bottom, left), (name, sid) in zip(face_locations, recognized):
            color = COLOR_GREEN if name != "Bilinmeyen" else COLOR_RED

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            label = name if sid is None else f"{name} ({sid})"

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, label, (left + 6, bottom - 6), FONT, 0.6, COLOR_WHITE, 2)

        return frame

    # --------------------------------------------------------
    def show_attendance_summary(self):
        print_header("YOKLAMA ÖZETİ")
        summary = get_attendance_summary()

        print("Dosya:", summary["file_path"])
        print("Toplam Kayıt:", summary["total"])
        print("Gelen Öğrenci:", summary["present"])
        print("\nBugün Gelenler:")
        for student in summary["students"]:
            print(" •", student)

    # --------------------------------------------------------
    def run(self):
        if not self._init_camera():
            return

        print_info("Sistem çalışıyor... Çıkış: Q, Özet: S")

        face_locations = []
        recognized = []

        while True:
            ret, frame = self.camera.read()
            if not ret:
                continue

            if self.frame_count % PROCESS_EVERY_N_FRAMES == 0:
                face_locations, recognized = self._process_frame(frame)

            self.frame_count += 1

            frame = self._draw_results(frame, face_locations, recognized)
            cv2.imshow("Yüz Tanıma Yoklama Sistemi", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or key == 27:
                break
            elif key == ord("s"):
                self.show_attendance_summary()

        self.camera.release()
        cv2.destroyAllWindows()


# ============================================================
def main():
    print("=== YÜZ TANIMA TABANLI YOKLAMA SİSTEMİ ===")
    system = FaceRecognitionAttendance()
    system.run()


if __name__ == "__main__":
    main()
