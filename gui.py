import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import shutil
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Yüz Tanıma Yoklama Sistemi")
        self.geometry("980x620")
        self.resizable(False, False)

        # SOL MENÜ
        self.sidebar = ctk.CTkFrame(self, width=220)
        self.sidebar.pack(side="left", fill="y")

        title = ctk.CTkLabel(self.sidebar, text="Menü", font=("Arial", 26, "bold"))
        title.pack(pady=25)

        # KAMERAYI BAŞLAT
        self.btn_start = ctk.CTkButton(
            self.sidebar, 
            text="📷 Kamerayı Başlat",
            height=45,
            command=self.start_camera
        )
        self.btn_start.pack(pady=12, fill="x", padx=20)

        # RAPORLARI AÇ
        self.btn_reports = ctk.CTkButton(
            self.sidebar, 
            text="📊 Yoklama Raporları",
            height=45,
            command=self.open_reports
        )
        self.btn_reports.pack(pady=12, fill="x", padx=20)

        # ÖĞRENCİ EKLEME FORMU
        self.btn_add_student = ctk.CTkButton(
            self.sidebar,
            text="➕ Öğrenci Ekle",
            height=45,
            command=self.show_add_student_page
        )
        self.btn_add_student.pack(pady=12, fill="x", padx=20)

        # ÇIKIŞ
        self.btn_exit = ctk.CTkButton(
            self.sidebar, 
            text="❌ Çıkış",
            fg_color="red",
            hover_color="#8b0000",
            height=45,
            command=self.quit
        )
        self.btn_exit.pack(pady=40, fill="x", padx=20)

        # ANA PANEL
        self.main_panel = ctk.CTkFrame(self)
        self.main_panel.pack(side="right", fill="both", expand=True)

        self.show_home_page()


    # ===================== ANA SAYFA =====================
    def show_home_page(self):
        self.clear_panel()

        welcome = ctk.CTkLabel(
            self.main_panel,
            text="Yüz Tanıma Yoklama Sistemine Hoş Geldiniz",
            font=("Arial", 30, "bold")
        )
        welcome.pack(pady=50)

        desc = ctk.CTkLabel(
            self.main_panel,
            text="Kamerayı başlatarak yoklama alabilir,\n"
                 "yeni öğrenci ekleyebilir veya raporlara ulaşabilirsiniz.",
            font=("Arial", 17),
            text_color="lightgray"
        )
        desc.pack(pady=10)


    # ===================== ÖĞRENCİ EKLE =====================
    def show_add_student_page(self):
        self.clear_panel()

        title = ctk.CTkLabel(
            self.main_panel,
            text="Öğrenci Ekleme",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=30)

        # AD
        lbl_name = ctk.CTkLabel(self.main_panel, text="Öğrenci Adı:", font=("Arial", 16))
        lbl_name.pack(pady=5)

        self.entry_name = ctk.CTkEntry(self.main_panel, width=300)
        self.entry_name.pack(pady=5)

        # NUMARA
        lbl_id = ctk.CTkLabel(self.main_panel, text="Öğrenci Numarası:", font=("Arial", 16))
        lbl_id.pack(pady=5)

        self.entry_id = ctk.CTkEntry(self.main_panel, width=300)
        self.entry_id.pack(pady=5)

        # FOTOĞRAF SEÇ
        self.photo_path = None

        btn_select_photo = ctk.CTkButton(
            self.main_panel,
            text="📁 Fotoğraf Seç",
            command=self.select_photo
        )
        btn_select_photo.pack(pady=15)

        # KAYDET BUTONU
        btn_save = ctk.CTkButton(
            self.main_panel,
            text="💾 Öğrenciyi Kaydet",
            color="green",
            command=self.save_student
        )
        btn_save.pack(pady=25)


    def select_photo(self):
        file_path = filedialog.askopenfilename(
            title="Fotoğraf Seç",
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
        )
        if file_path:
            self.photo_path = file_path
            messagebox.showinfo("Tamam", "Fotoğraf seçildi!")


    def save_student(self):
        name = self.entry_name.get().strip()
        student_id = self.entry_id.get().strip()

        if not name or not student_id or not self.photo_path:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
            return

        # Fotoğrafı dataset klasörüne kopyala
        filename = f"{student_id}_{name.replace(' ', '_')}.jpg"
        dest_path = os.path.join("dataset", filename)
        shutil.copy(self.photo_path, dest_path)

        messagebox.showinfo("Başarılı", "Öğrenci kaydedildi!\nEncoding yenileniyor...")

        # encode_faces.py çalıştır
        subprocess.Popen(["python", "encode_faces.py"])

        messagebox.showinfo("Tamam", "İşlem tamamlandı! Artık öğrenci tanınabilir.")

        self.show_home_page()


    # ===================== DİĞER İŞLEVLER =====================
    def clear_panel(self):
        for widget in self.main_panel.winfo_children():
            widget.destroy()


    def start_camera(self):
        subprocess.Popen(["python", "main.py"])

    def open_reports(self):
        os.startfile("attendance")


if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
