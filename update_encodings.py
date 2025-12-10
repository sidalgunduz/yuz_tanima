# -*- coding: utf-8 -*-
"""Tüm öğrenciler için encoding güncelleme scripti"""

import os
import sys

# Çalışma dizinini ayarla
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import face_recognition
from utils import get_dataset_images, save_encodings

def main():
    images = get_dataset_images()
    all_encodings, all_names, all_ids = [], [], []

    for file_path, student_id, student_name in images:
        print(f'Processing: {student_name}...', end=' ')
        try:
            image = face_recognition.load_image_file(file_path)
            face_locations = face_recognition.face_locations(image, model='hog')
            if face_locations:
                encodings = face_recognition.face_encodings(image, face_locations)
                if encodings:
                    all_encodings.append(encodings[0])
                    all_names.append(student_name)
                    all_ids.append(student_id)
                    print('OK')
                else:
                    print('ENCODING FAILED')
            else:
                print('NO FACE FOUND')
        except Exception as e:
            print(f'ERROR: {e}')

    print(f'\n{len(all_encodings)} encodings created')
    
    if all_encodings:
        save_encodings(all_encodings, all_names, all_ids)
        print('Encodings saved successfully!')
    else:
        print('No encodings to save!')

if __name__ == '__main__':
    main()
