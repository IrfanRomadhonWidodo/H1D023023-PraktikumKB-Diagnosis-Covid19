import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import webbrowser
import time
import math
import os
import sys

class COVIDExpertSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Pakar Deteksi COVID-19")
        self.root.geometry("1000x750")
        self.root.configure(bg="#f0f8ff")
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles
        self.style.configure("TFrame", background="#f0f8ff")
        self.style.configure("TLabel", background="#f0f8ff", font=("Helvetica", 10))
        self.style.configure("TButton", font=("Helvetica", 10, "bold"), padding=8)
        self.style.configure("Title.TLabel", font=("Helvetica", 18, "bold"), foreground="#006400")
        self.style.configure("Question.TLabel", font=("Helvetica", 12), foreground="#000080")
        self.style.configure("Result.TLabel", font=("Helvetica", 14, "bold"), foreground="#006400")
        self.style.configure("TProgressbar", thickness=20, troughcolor="#e0e0e0", background="#4CAF50")
        self.style.configure("Toolbutton", font=("Helvetica", 10))
        self.style.configure("Accent.TButton", 
                            font=("Helvetica", 11, "bold"), 
                            padding=10,
                            background="#4CAF50",
                            foreground="black")
        
        # Configure style maps
        self.style.map('TButton',
            foreground=[('active', 'black'), ('!disabled', 'black')],
            background=[('active', '#4CAF50'), ('!disabled', '#4CAF50')])
        self.style.map("Accent.TButton",
            background=[('active', '#45a049')])
        
        # Initialize scrolling text animation variables
        self.scrolling_text = "CEGAH COVID-19 • Gunakan masker dengan benar • Cuci tangan pakai sabun • Jaga jarak minimal 1 meter • Hindari menyentuh wajah • Segera vaksinasi • Isolasi mandiri jika bergejala • "
        self.scroll_position = 0
        self.animation_running = False
        self.scroll_label = None
        
        # Initialize loading spinner animation variables
        self.spinner_canvas = None
        self.spinner_angle = 0
        
        self.create_welcome_screen()
        
        # Data storage
        self.user_data = {}
        self.responses = {}
        self.questions = [
            "Apakah Anda mengalami demam (suhu > 37.5°C)?",
            "Apakah Anda mengalami batuk kering?",
            "Apakah Anda merasa sesak napas?",
            "Apakah Anda mengalami kelelahan yang tidak biasa?",
            "Apakah Anda kehilangan indera penciuman atau perasa?",
            "Apakah Anda mengalami sakit tenggorokan?",
            "Apakah Anda mengalami sakit kepala?",
            "Apakah Anda mengalami nyeri otot atau tubuh?",
            "Apakah Anda mengalami hidung tersumbat atau pilek?",
            "Apakah Anda mengalami mual atau muntah?",
            "Apakah Anda mengalami diare?",
            "Apakah Anda memiliki riwayat kontak dengan pasien COVID-19 dalam 14 hari terakhir?",
            "Apakah Anda pernah melakukan perjalanan ke zona merah COVID-19 dalam 14 hari terakhir?"
        ]
    
    def animate_scrolling_text(self):
        """Animates text scrolling from right to left"""
        if self.animation_running and self.scroll_label:
            # Calculate new position
            self.scroll_position = (self.scroll_position + 1) % len(self.scrolling_text)
            
            # Create scrolling effect by changing displayed text
            rotated_text = self.scrolling_text[self.scroll_position:] + self.scrolling_text[:self.scroll_position]
            self.scroll_label.config(text=rotated_text)
            
            # Continue animation
            self.root.after(90, self.animate_scrolling_text)
    
    def animate_spinner(self):
        """Animates a loading spinner"""
        if self.animation_running and self.spinner_canvas:
            # Update spinner angle
            self.spinner_angle = (self.spinner_angle + 15) % 360
            
            # Clear canvas
            self.spinner_canvas.delete("spinner")
            
            # Calculate coordinates for arc
            center_x, center_y = 50, 50
            radius = 30
            
            # Draw spinner arc
            self.spinner_canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=self.spinner_angle, extent=120,
                outline="#4CAF50", width=8, style=tk.ARC, tags="spinner"
            )
            
            # Continue animation
            self.root.after(50, self.animate_spinner)
    
    def create_welcome_screen(self):
        self.clear_screen()
        self.animation_running = False
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)
        
        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(pady=30)  # Increased padding to compensate for removed logo
        title_label = ttk.Label(title_frame, 
                                text="SISTEM PAKAR DETEKSI COVID-19", 
                                style="Title.TLabel")
        title_label.pack()
        
        # Scrolling text animation
        anim_frame = ttk.Frame(main_frame, padding=10)
        anim_frame.pack(pady=10)
        self.scroll_label = ttk.Label(anim_frame, 
                                    text=self.scrolling_text,
                                    font=("Helvetica", 14, "bold"),
                                    foreground="#4CAF50")
        self.scroll_label.pack()
        self.animation_running = True
        self.animate_scrolling_text()
        
        # Description
        desc_frame = ttk.Frame(main_frame)
        desc_frame.pack(pady=20)
        desc_label = ttk.Label(desc_frame, 
                                text="Sistem ini akan membantu Anda mengevaluasi kemungkinan terpapar virus COVID-19\nberdasarkan gejala yang Anda alami.",
                                font=("Helvetica", 11), 
                                justify=tk.CENTER)
        desc_label.pack()
        
        # Start button
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=30)
        start_button = ttk.Button(button_frame, 
                                    text="MULAI DIAGNOSIS", 
                                    command=self.create_user_info_screen, 
                                    style="Accent.TButton")
        start_button.pack(ipadx=30, ipady=10)
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(side=tk.BOTTOM, pady=20)
        footer_label = ttk.Label(footer_frame, 
                                text="Disclaimer: Hasil diagnosis ini tidak menggantikan pemeriksaan medis oleh tenaga kesehatan profesional.",
                                font=("Helvetica", 9), 
                                foreground="gray")
        footer_label.pack()
    
    def create_user_info_screen(self):
        self.clear_screen()
        self.animation_running = False
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
        
        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(pady=10)
        title_label = ttk.Label(title_frame, 
                                text="INFORMASI PENGGUNA", 
                                style="Title.TLabel")
        title_label.pack()
        
        # Form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)
        
        # Name field
        ttk.Label(form_frame, 
                    text="Nama Lengkap:", 
                    font=("Helvetica", 11)).grid(row=0, column=0, sticky=tk.W, pady=8, padx=10)
        self.name_entry = ttk.Entry(form_frame, 
                                    width=35, 
                                    font=("Helvetica", 11))
        self.name_entry.grid(row=0, column=1, pady=8, padx=10)
        
        # Age field
        ttk.Label(form_frame, 
                    text="Usia:", 
                    font=("Helvetica", 11)).grid(row=1, column=0, sticky=tk.W, pady=8, padx=10)
        self.age_entry = ttk.Entry(form_frame, 
                                    width=35, 
                                    font=("Helvetica", 11))
        self.age_entry.grid(row=1, column=1, pady=8, padx=10)
        
        # Gender field
        ttk.Label(form_frame, 
                    text="Jenis Kelamin:", 
                    font=("Helvetica", 11)).grid(row=2, column=0, sticky=tk.W, pady=8, padx=10)
        gender_frame = ttk.Frame(form_frame)
        gender_frame.grid(row=2, column=1, sticky=tk.W, pady=8, padx=10)
        self.gender_var = tk.StringVar()
        ttk.Radiobutton(gender_frame, 
                        text="Laki-laki", 
                        variable=self.gender_var, 
                        value="Laki-laki", 
                        style="Toolbutton").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(gender_frame, 
                        text="Perempuan", 
                        variable=self.gender_var, 
                        value="Perempuan", 
                        style="Toolbutton").pack(side=tk.LEFT, padx=5)
        
        # Phone field
        ttk.Label(form_frame, 
                    text="Nomor Telepon:", 
                    font=("Helvetica", 11)).grid(row=3, column=0, sticky=tk.W, pady=8, padx=10)
        self.phone_entry = ttk.Entry(form_frame, 
                                    width=35, 
                                    font=("Helvetica", 11))
        self.phone_entry.grid(row=3, column=1, pady=8, padx=10)
        
        # Email field
        ttk.Label(form_frame, 
                    text="Email:", 
                    font=("Helvetica", 11)).grid(row=4, column=0, sticky=tk.W, pady=8, padx=10)
        self.email_entry = ttk.Entry(form_frame, 
                                    width=35, 
                                    font=("Helvetica", 11))
        self.email_entry.grid(row=4, column=1, pady=8, padx=10)
        
        # Navigation buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=30)
        
        back_button = ttk.Button(button_frame, 
                                text="KEMBALI", 
                                command=self.create_welcome_screen,
                                style="Accent.TButton")
        back_button.grid(row=0, column=0, padx=15, ipadx=15, ipady=5)
        
        next_button = ttk.Button(button_frame, 
                                text="LANJUT", 
                                command=self.validate_user_info,
                                style="Accent.TButton")
        next_button.grid(row=0, column=1, padx=15, ipadx=15, ipady=5)
    
    def validate_user_info(self):
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        gender = self.gender_var.get()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        
        # Validation
        if not name:
            messagebox.showerror("Error", "Nama lengkap harus diisi")
            return
        if not age:
            messagebox.showerror("Error", "Usia harus diisi")
            return
        if not age.isdigit() or int(age) <= 0 or int(age) > 120:
            messagebox.showerror("Error", "Usia harus berupa angka antara 1-120")
            return
        if not gender:
            messagebox.showerror("Error", "Jenis kelamin harus dipilih")
            return
        
        # Store user data
        self.user_data = {
            "name": name,
            "age": age,
            "gender": gender,
            "phone": phone,
            "email": email
        }
        
        # Move to questions screen
        self.create_question_screen(0)
    
    def create_question_screen(self, question_idx):
        self.clear_screen()
        self.animation_running = False
        
        # Check if all questions answered
        if question_idx >= len(self.questions):
            self.process_responses()
            return
            
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
        
        # Progress information
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(pady=10, fill=tk.X)
        
        progress = (question_idx / len(self.questions)) * 100
        progress_label = ttk.Label(progress_frame, 
                                    text=f"Pertanyaan {question_idx+1} dari {len(self.questions)}",
                                    font=("Helvetica", 10, "bold"))
        progress_label.pack(side=tk.LEFT)
        
        percent_label = ttk.Label(progress_frame, 
                                    text=f"{progress:.0f}% selesai",
                                    font=("Helvetica", 10, "bold"))
        percent_label.pack(side=tk.RIGHT)
        
        progress_bar = ttk.Progressbar(main_frame, 
                                        orient=tk.HORIZONTAL, 
                                        length=600, 
                                        mode='determinate', 
                                        value=progress)
        progress_bar.pack(pady=10)
        
        # Question box
        question_frame = ttk.Frame(main_frame, 
                                    borderwidth=2, 
                                    relief="groove", 
                                    padding=20)
        question_frame.pack(pady=30, fill=tk.X)
        
        question_label = ttk.Label(question_frame, 
                                    text=self.questions[question_idx], 
                                    style="Question.TLabel", 
                                    wraplength=600, 
                                    justify=tk.CENTER,
                                    font=("Helvetica", 14))
        question_label.pack(pady=20)
        
        # Response buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=30)
        
        yes_button = ttk.Button(button_frame, 
                                text="YA", 
                                command=lambda: self.record_response(question_idx, "ya"),
                                style="Accent.TButton")
        yes_button.grid(row=0, column=0, padx=15, ipadx=20, ipady=8)
        
        no_button = ttk.Button(button_frame, 
                                text="TIDAK", 
                                command=lambda: self.record_response(question_idx, "tidak"),
                                style="Accent.TButton")
        no_button.grid(row=0, column=1, padx=15, ipadx=20, ipady=8)
        
        # Back button (not on first question)
        if question_idx > 0:
            back_button = ttk.Button(main_frame, 
                                    text="KEMBALI", 
                                    command=lambda: self.create_question_screen(question_idx-1),
                                    style="Accent.TButton")
            back_button.pack(side=tk.LEFT, padx=40, pady=20, ipadx=15, ipady=5)
    
    def record_response(self, question_idx, response):
        self.responses[f"q{question_idx+1}"] = response
        self.create_question_screen(question_idx + 1)
    
    def process_responses(self):
        # Show processing animation
        self.show_processing_screen()
        
        # Coba panggil Prolog terlebih dahulu
        try:
            prolog_query = self.build_prolog_query()
            result = self.execute_prolog_query(prolog_query)
            if result:
                self.show_results(result["Diagnosis"], result["Rekomendasi"])
                return
        except Exception as e:
            print(f"Error calling Prolog: {e}")
        
        # Fallback ke metode tanpa Prolog
        self.root.after(1500, self.diagnose_without_prolog)

    
    def show_processing_screen(self):
        self.clear_screen()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)
        
        title_label = ttk.Label(main_frame, 
                                text="MEMPROSES HASIL...", 
                                style="Title.TLabel")
        title_label.pack(pady=30)
        
        # Loading spinner animation
        spinner_frame = ttk.Frame(main_frame)
        spinner_frame.pack(pady=20)
        
        self.spinner_canvas = tk.Canvas(spinner_frame, width=100, height=100, bg="#f0f8ff", highlightthickness=0)
        self.spinner_canvas.pack()
        
        self.animation_running = True
        self.animate_spinner()
        
        loading_text = ttk.Label(main_frame, 
                                text="Sedang menganalisis gejala Anda...",
                                font=("Helvetica", 12))
        loading_text.pack(pady=10)
    
    def diagnose_without_prolog(self):
        """Fallback method that implements diagnosis logic directly in Python"""
        try:
            # Count "ya" responses for symptoms
            symptom_count = 0
            for i in range(1, 12):  # Q1-Q11 are symptoms
                if self.responses.get(f"q{i}", "tidak") == "ya":
                    symptom_count += 1
            
            # Count "ya" responses for risk factors
            risk_count = 0
            for i in range(12, 14):  # Q12-Q13 are risk factors
                if self.responses.get(f"q{i}", "tidak") == "ya":
                    risk_count += 1
            
            # Determine diagnosis and recommendation
            if symptom_count >= 8 and risk_count >= 1:
                diagnosis = "Tingkat Kecurigaan Tinggi COVID-19"
                recommendation = "Segera lakukan tes PCR dan isolasi mandiri. Hubungi fasilitas kesehatan terdekat untuk pemeriksaan lebih lanjut."
            elif symptom_count >= 5 and risk_count >= 1:
                diagnosis = "Tingkat Kecurigaan Sedang COVID-19"
                recommendation = "Lakukan tes antigen/PCR. Lakukan isolasi mandiri sambil menunggu hasil tes. Pantau gejala dan saturasi oksigen secara berkala."
            elif symptom_count >= 3 and risk_count >= 1:
                diagnosis = "Tingkat Kecurigaan Rendah COVID-19"
                recommendation = "Lakukan tes antigen jika memungkinkan. Istirahat yang cukup dan pantau perkembangan gejala. Jika gejala memburuk, segera periksakan diri."
            elif symptom_count >= 1:
                diagnosis = "Gejala Ringan Tidak Spesifik COVID-19"
                recommendation = "Istirahat yang cukup, minum air putih, dan pantau gejala. Jika gejala menetap atau memburuk dalam 3 hari, pertimbangkan untuk tes COVID-19."
            else:
                diagnosis = "Tidak Ada Gejala COVID-19 yang Signifikan"
                recommendation = "Tetap patuhi protokol kesehatan (memakai masker, mencuci tangan, menjaga jarak). Lakukan vaksinasi jika belum."
            
            self.show_results(diagnosis, recommendation)
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat memproses diagnosis: {str(e)}")
            self.create_welcome_screen()
    
    def execute_prolog_query(self, prolog_query):
        """Original method that tries to call Prolog if available"""
        try:
            # Check if SWI-Prolog is installed
            try:
                # Ensure the Prolog file exists
                if not os.path.exists("covid_rules.pl"):
                    raise FileNotFoundError("File covid_rules.pl tidak ditemukan")
                
                # Try running swipl with a simple query to check if it's installed
                test_cmd = ['swipl', '--version']
                subprocess.run(test_cmd, capture_output=True, check=True)
                
                # Call Prolog with our query
                cmd = ['swipl', '-q', '-s', 'covid_rules.pl', '-g', prolog_query, '-t', 'halt']
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                
                output = result.stdout.strip()
                if not output:
                    raise ValueError("Tidak ada hasil dari sistem pakar")
                    
                parts = output.split(',')
                diagnosis_part = parts[0].split('=')
                recommendation_part = parts[1].split('=')
                
                return {
                    "Diagnosis": diagnosis_part[1].strip(),
                    "Rekomendasi": recommendation_part[1].strip()
                }
            except (subprocess.SubprocessError, FileNotFoundError, ValueError) as e:
                print(f"Error with Prolog: {e}. Falling back to Python implementation.")
                self.diagnose_without_prolog()
                return None
        except Exception as e:
            print(f"Exception in execute_prolog_query: {e}")
            self.diagnose_without_prolog()
            return None
    
    def show_results(self, diagnosis, recommendation):
        self.clear_screen()
        self.animation_running = False
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
        
        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(pady=10)
        title_label = ttk.Label(title_frame, 
                                text="HASIL DIAGNOSIS COVID-19", 
                                style="Title.TLabel")
        title_label.pack()
        
        # User info box
        user_info_frame = ttk.Frame(main_frame, 
                                    borderwidth=1, 
                                    relief="solid", 
                                    padding=15)
        user_info_frame.pack(pady=15, fill=tk.X)
        
        ttk.Label(user_info_frame, 
                    text=f"Nama: {self.user_data['name']}", 
                    font=("Helvetica", 11)).pack(anchor=tk.W, pady=3)
        ttk.Label(user_info_frame, 
                    text=f"Usia: {self.user_data['age']} tahun", 
                    font=("Helvetica", 11)).pack(anchor=tk.W, pady=3)
        ttk.Label(user_info_frame, 
                    text=f"Jenis Kelamin: {self.user_data['gender']}", 
                    font=("Helvetica", 11)).pack(anchor=tk.W, pady=3)
        
        # Result box
        result_frame = ttk.Frame(main_frame, 
                                borderwidth=1, 
                                relief="solid", 
                                padding=15)
        result_frame.pack(pady=15, fill=tk.X)
        
        ttk.Label(result_frame, 
                    text="HASIL DIAGNOSIS:", 
                    style="Result.TLabel").pack(anchor=tk.W, pady=5)
        
        # Color code based on diagnosis level
        if "Tinggi" in diagnosis:
            diagnosis_color = "red"
        elif "Sedang" in diagnosis:
            diagnosis_color = "orange"
        elif "Rendah" in diagnosis:
            diagnosis_color = "#FFD700"  # gold
        else:
            diagnosis_color = "green"
        
        ttk.Label(result_frame, 
                    text=diagnosis, 
                    font=("Helvetica", 12, "bold"), 
                    foreground=diagnosis_color, 
                    wraplength=700).pack(anchor=tk.W, pady=5)
        
        ttk.Label(result_frame, 
                    text="REKOMENDASI:", 
                    style="Result.TLabel").pack(anchor=tk.W, pady=(15,5))
        ttk.Label(result_frame, 
                    text=recommendation, 
                    font=("Helvetica", 11), 
                    wraplength=700).pack(anchor=tk.W, pady=5)
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(pady=30)
        
        if "Tinggi" in diagnosis or "Sedang" in diagnosis:
            ttk.Button(action_frame, 
                        text="CARI RUMAH SAKIT TERDEKAT", 
                        command=lambda: webbrowser.open("https://www.google.com/maps/search/rumah+sakit"),
                        style="Accent.TButton").grid(row=0, column=0, padx=10, ipadx=10, ipady=5)
        
        ttk.Button(action_frame, 
                    text="PELAJARI TENTANG COVID-19", 
                    command=lambda: webbrowser.open("https://www.halodoc.com/kesehatan/coronavirus"),
                    style="Accent.TButton").grid(row=0, column=1, padx=10, ipadx=10, ipady=5)
        
        ttk.Button(action_frame, 
                    text="DIAGNOSIS ULANG", 
                    command=self.create_welcome_screen,
                    style="Accent.TButton").grid(row=0, column=2, padx=10, ipadx=10, ipady=5)
        
        # Important notice
        notice_frame = ttk.Frame(main_frame)
        notice_frame.pack(side=tk.BOTTOM, pady=20)
        
        if "Tinggi" in diagnosis or "Sedang" in diagnosis:
            notice_text = "PERINGATAN: Segera hubungi layanan kesehatan terdekat!"
            notice_color = "red"
        else:
            notice_text = "Jika gejala memburuk, segera hubungi layanan kesehatan terdekat."
            notice_color = "orange"
        
        ttk.Label(notice_frame, 
                    text=notice_text,
                    font=("Helvetica", 11, "bold"), 
                    foreground=notice_color).pack()
    
    def clear_screen(self):
        self.animation_running = False
        if hasattr(self, 'scroll_label'):
            self.scroll_label = None
        if hasattr(self, 'spinner_canvas'):
            self.spinner_canvas = None
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = COVIDExpertSystem(root)
    root.mainloop()