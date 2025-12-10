import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import shutil
import os
import sys

# Sanal ortamdaki Python yorumlayıcısı
PYTHON_EXE = sys.executable

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Yüz Tanıma Yoklama Sistemi")
        self.geometry("980x620")
        self.resizable(False, False)

        # ======== SOL MENÜ ========
        self.sidebar = ctk.CTkFrame(self, width=220)
        self.sidebar.pack(side="left", fill="y")

        title = ctk.CTkLabel(self.sidebar, text="Menü", font=("Arial", 26, "bold"))
        title.pack(pady=25)

        # Kamerayı Başlat
        self.btn_start = ctk.CTkButton(
            self.sidebar,
            text="📷 Kamerayı Başlat",
            height=45,
            fg_color="#3A7FF6",
            hover_color="#2E67C7",
            command=self.start_camera,
        )
        self.btn_start.pack(pady=12, fill="x", padx=20)

        # Raporlar
        self.btn_reports = ctk.CTkButton(
            self.sidebar,
            text="📊 Yoklama Raporları",
            height=45,
            fg_color="#3A7FF6",
            hover_color="#2E67C7",
            command=self.open_reports,
        )
        self.btn_reports.pack(pady=12, fill="x", padx=20)

        # Öğrenci Ekle
        self.btn_add_student = ctk.CTkButton(
            self.sidebar,
            text="➕ Öğrenci Ekle",
            height=45,
            fg_color="#3A7FF6",
            hover_color="#2E67C7",
            command=self.show_add_student_page,
        )
        self.btn_add_student.pack(pady=12, fill="x", padx=20)

        # Encoding Güncelle
        self.btn_update_encoding = ctk.CTkButton(
            self.sidebar,
            text="🔄 Encoding Güncelle",
            height=45,
            fg_color="#28A745",
            hover_color="#1E7B34",
            command=self.update_encodings,
        )
        self.btn_update_encoding.pack(pady=12, fill="x", padx=20)

        # Çıkış
        self.btn_exit = ctk.CTkButton(
            self.sidebar,
            text="❌ Çıkış",
            height=45,
            fg_color="#D9534F",
            hover_color="#B52B27",
            command=self.quit,
        )
        self.btn_exit.pack(pady=40, fill="x", padx=20)

        # ======== ANA PANEL ========
        self.main_panel = ctk.CTkFrame(self)
        self.main_panel.pack(side="right", fill="both", expand=True)

        self.show_home_page()

    # =====================================================
    # ANA SAYFA
    # =====================================================
    def show_home_page(self):
        self.clear_panel()

        welcome = ctk.CTkLabel(
            self.main_panel,
            text="Yüz Tanıma Yoklama Sistemine Hoş Geldiniz",
            font=("Arial", 30, "bold"),
        )
        welcome.pack(pady=50)

        desc = ctk.CTkLabel(
            self.main_panel,
            text="Kamerayı başlatarak yoklama alabilir,\n"
                 "yeni öğrenci ekleyebilir veya raporlara ulaşabilirsiniz.",
            font=("Arial", 17),
            text_color="lightgray",
        )
        desc.pack(pady=10)

    # =====================================================
    # ÖĞRENCİ EKLEME SAYFASI
    # =====================================================
    def show_add_student_page(self):
        self.clear_panel()

        title = ctk.CTkLabel(
            self.main_panel, text="Öğrenci Ekleme", font=("Arial", 28, "bold")
        )
        title.pack(pady=30)

        # Öğrenci Adı
        lbl_name = ctk.CTkLabel(self.main_panel, text="Öğrenci Adı:", font=("Arial", 16))
        lbl_name.pack(pady=5)

        self.entry_name = ctk.CTkEntry(self.main_panel, width=300)
        self.entry_name.pack(pady=5)

        # Öğrenci No
        lbl_id = ctk.CTkLabel(self.main_panel, text="Öğrenci Numarası:", font=("Arial", 16))
        lbl_id.pack(pady=5)

        self.entry_id = ctk.CTkEntry(self.main_panel, width=300)
        self.entry_id.pack(pady=5)

        # Fotoğraf seç
        self.photo_path = None

        btn_select_photo = ctk.CTkButton(
            self.main_panel,
            text="📁 Fotoğraf Seç",
            fg_color="#3A7FF6",
            hover_color="#2E67C7",
            command=self.select_photo,
        )
        btn_select_photo.pack(pady=15)

        # Kaydet
        btn_save = ctk.CTkButton(
            self.main_panel,
            text="💾 Öğrenciyi Kaydet",
            fg_color="#28A745",
            hover_color="#1E7B34",
            command=self.save_student,
        )
        btn_save.pack(pady=25)

    # =====================================================
    # FOTOĞRAF SEÇ
    # =====================================================
    def select_photo(self):
        file_path = filedialog.askopenfilename(
            title="Fotoğraf Seç", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
        )
        if file_path:
            self.photo_path = file_path
            messagebox.showinfo("Tamam", "Fotoğraf seçildi!")

    # =====================================================
    # ÖĞRENCİ KAYDETME
    # =====================================================
    def save_student(self):
        name = self.entry_name.get().strip()
        student_id = self.entry_id.get().strip()

        if not name or not student_id or not self.photo_path:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
            return

        filename = f"{student_id}_{name.replace(' ', '_')}.jpg"
        dest_path = os.path.join("dataset", filename)
        shutil.copy(self.photo_path, dest_path)

        messagebox.showinfo("Başarılı", "Öğrenci kaydedildi! Encoding güncelleniyor...")

        subprocess.Popen([PYTHON_EXE, "encode_faces.py"])

        messagebox.showinfo("Tamam", "İşlem tamamlandı! Artık öğrenci tanınabilir.")
        self.show_home_page()

    # =====================================================
    # PANELİ TEMİZLE (HATASIZ)
    # =====================================================
    def clear_panel(self):
        for widget in self.main_panel.winfo_children():
            try:
                widget.grid_forget()
                widget.pack_forget()
                widget.place_forget()
            except:
                pass

            try:
                widget.destroy()
            except:
                pass

    # =====================================================
    # KAMERA BAŞLAT
    # =====================================================
    def start_camera(self):
        subprocess.call([PYTHON_EXE, "main.py"])

    # =====================================================
    # ENCODING GÜNCELLE
    # =====================================================
    def update_encodings(self):
        messagebox.showinfo("Bilgi", "Encoding güncelleme başlıyor...\nBu işlem biraz zaman alabilir.")
        subprocess.Popen([PYTHON_EXE, "update_encodings.py"])
        messagebox.showinfo("Başarılı", "Encoding güncelleme işlemi başlatıldı!\nTamamlandığında yeni öğrenciler tanınabilir olacak.")

    # =====================================================
    # RAPORLARI AÇ
    # =====================================================
    def open_reports(self):
        os.startfile("attendance")


if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
