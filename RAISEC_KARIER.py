import json
from math import floor
import datetime
import os
from customtkinter import CTkFont
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton
from customtkinter import *
################################################################################
## COLOR CODES VARIABLE
################################################################################

class colors:
    def __init__(self):
        self.main_color = "#09E8AD"
        self.hover_main_color = "#0BA47C"
        self.background_dark = "#181818"
        self.surface_dark = "#2B2B2B"
        self.text_color_dark = "#ffffff"
        self.text_button_dark = "#1F1F1F"

        self.danger_button = "#B50404"
        self.hover_danger_button = "#6B0303"

        self.success_button = "#13B507"
        self.hover_success_button = "#0B6B04"

        
        self.surface_light = "#d1d1d1"
        self.background_light = "#ffffff"
        self.text_color_light = "#1e1e1e"

class font:
    def __init__(self):
        self.logo = CTkFont(family="Eras ITC",size=41, weight="normal")
        self.heading1 = CTkFont(family="Poppins",size=30,weight="bold")
        self.paragraf = CTkFont(family="Poppins",size=20,weight="bold")

########################################################################
## Method 
########################################################################


def Geometri(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    width = int(screen_width)
    height = int(screen_height)

    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)

    window.title("RIASEC App")
    window.geometry(f"{width}x{height}+{x}+{y}")

def load_pertanyaan():
    current_dir = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(current_dir, 'question.json'))
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Format file question.json tidak valid: harus berupa list.")
            return data
    except FileNotFoundError:
        raise FileNotFoundError("File question.json tidak ditemukan. Pastikan file ada di direktori yang benar.")
    except json.JSONDecodeError:
        raise ValueError("File question.json corrupt atau format tidak valid.")
    except Exception as e:
        raise RuntimeError(f"Gagal memuat pertanyaan: {str(e)}")

#Menentukan kode minat RIASEC. Menggunakan struktur tree dengan 3 level untuk menghasilkan kode 3 huruf.
class DecisionTree:
    class TreeNode:
        def __init__(self, kategori=None):
            self.kategori = kategori
            self.children = {}

    def __init__(self):
        self.root = self.TreeNode()
        self.priority_order = {'R': 0, 'I': 1, 'A': 2, 'S': 3, 'E': 4, 'C': 5}
        self._build_tree()

    def _build_tree(self):
        #Membangun struktur pohon keputusan 3 level:
        for k1 in "RIASEC": #Level 1: 6 kategori utama (R, I, A, S, E, C)
            node1 = self.TreeNode(k1)
            self.root.children[k1] = node1
            for k2 in "RIASEC":#Level 2: 5 kategori tersisa 
                if k2 != k1:
                    node2 = self.TreeNode(k2)
                    node1.children[k2] = node2
                    for k3 in "RIASEC":#Level 3: 4 kategori tersisa 
                        if k3 != k1 and k3 != k2:
                            node3 = self.TreeNode(k3)
                            node2.children[k3] = node3

    def traverse(self, skor):
        #Urutkan item: pertama berdasarkan skor (descending), 
        #Jika skor sama, diurutkan berdasarkan prioritas RIASEC (dari R ke C)
        sorted_items = sorted(
            skor.items(),
            key=lambda item: (-item[1], self.priority_order[item[0]])
        ) 
        
        kode = ""
        node = self.root
        
        for k, v in sorted_items:
            if k in node.children:
                kode += k
                node = node.children[k]
                if len(kode) == 3:
                    break
                    
        return kode

def get_rekomendasi(interest_code):
    try:
        if not os.path.exists("RIASEC.json"):
            raise FileNotFoundError("File RIASEC.json tidak ditemukan.")
        
        with open("RIASEC.json", "r", encoding="utf-8") as f:
            data_rekomendasi = json.load(f)
        
        if not isinstance(data_rekomendasi, dict):
            raise ValueError("Format file RIASEC.json tidak valid: harus berupa dictionary.")
        
        data = data_rekomendasi.get(interest_code.upper(), {})
        
        if not data:
            print(f"Peringatan: Kode minat '{interest_code}' tidak ditemukan dalam database.")
            return [], []  
        
        return data.get("jurusan", []), data.get("karier", [])
    
    except json.JSONDecodeError:
        raise ValueError("File RIASEC.json corrupt atau format tidak valid.")
    except Exception as e:
        raise RuntimeError(f"Gagal memuat rekomendasi: {str(e)}")


########################################################################
## GUI Class
########################################################################


class tampilan_awal:
    def __init__(self, master):
        self.window = master
        Geometri(self.window)

        self.main_frame = CTkFrame(
            master=self.window,
            bg_color=colors().background_dark,
            fg_color=colors().background_dark,
        )
        self.main_frame.pack(fill="both", expand=True)

        self.navbar_frame = CTkFrame(
            master=self.main_frame,
            height=78,
            fg_color=colors().surface_dark
        )
        self.navbar_frame.pack(fill="x", side="top", anchor="n", pady=0)

        self.text_RIASEC = CTkLabel(
            master=self.navbar_frame,
            text="RIASEC",
            text_color=colors().text_color_dark,
            font=CTkFont(family="Eras Bold ITC", size=41, weight="normal"),
            width=10, height=50
        )
        self.text_RIASEC.place(relx=.1, rely=.175)

        self.layout_grid = CTkFrame(
            master=self.main_frame,
            fg_color=colors().background_dark
        )
        self.layout_grid.pack(fill="both", expand=True, padx=120, pady=0)

        for col in range(12):
            self.layout_grid.grid_columnconfigure(col, weight=1, uniform="col", pad=20, minsize=40)
            self.layout_grid.grid_rowconfigure(0, weight=1)

        self.main_content = CTkFrame(
            master=self.layout_grid,
            fg_color=colors().background_dark,
        )
        self.main_content.grid(
            row=0, column=0, columnspan=5,  
            padx=0, pady=83,
            sticky = "n",
        )

        self.right_content = CTkFrame(
            master=self.layout_grid,
            fg_color=colors().background_dark,
        )
        self.right_content.grid(
            row=0, column=5, columnspan=6,  
            padx=0, pady=83,
            sticky = "n",
        )

        CTkFrame(self.right_content, fg_color="#4A90E2", width = 140, height=80).grid(row=0, column=0, columnspan=4, padx = 20, pady=20)
        CTkFrame(self.right_content, fg_color="#50E3C2", width = 140, height=80).grid(row=0, column=4, columnspan=4, padx = 20, pady=20)
        CTkFrame(self.right_content, fg_color="#F5A623", width = 140, height=80).grid(row=0, column=8, columnspan=4, padx = 20, pady=20)
        CTkFrame(self.right_content, fg_color="#7ED321", width = 140, height=80).grid(row=1, column=0, columnspan=4, padx = 20, pady=20)
        CTkFrame(self.right_content, fg_color="#D0021B", width = 140, height=80).grid(row=1, column=4, columnspan=4, padx = 20, pady=20)
        CTkFrame(self.right_content, fg_color="#9B9B9B", width = 140, height=80).grid(row=1, column=8, columnspan=4, padx = 20, pady=20)

    
        label_r = CTkLabel(master=self.right_content, text="R", text_color="#4A90E2", font=CTkFont(family="Franklin Gothic Demi", size=21, weight="normal",))
        label_r.grid(row=2, column=0, padx=5, pady=5)
    
        label_i = CTkLabel(master=self.right_content, text="I", text_color="#50E3C2", font=CTkFont(family="Franklin Gothic Demi", size=21, weight="normal",))
        label_i.grid(row=3, column=0, padx=5, pady=5)
      
        label_a = CTkLabel(master=self.right_content, text="A", text_color="#F5A623", font=CTkFont(family="Franklin Gothic Demi", size=21, weight="normal",))
        label_a.grid(row=4, column=0, padx=5, pady=5)
        
        label_s = CTkLabel(master=self.right_content, text="S", text_color="#7ED321", font=CTkFont(family="Franklin Gothic Demi", size=21, weight="normal",))
        label_s.grid(row=2, column=5, padx=5, pady=5)
        
        label_e = CTkLabel(master=self.right_content, text="E", text_color="#D0021B", font=CTkFont(family="Franklin Gothic Demi", size=21, weight="normal",))
        label_e.grid(row=3, column=5, padx=5, pady=5)
       
        label_c = CTkLabel(master=self.right_content, text="C", text_color="#9B9B9B", font=CTkFont(family="Franklin Gothic Demi", size=21, weight="normal",))
        label_c.grid(row=4, column=5, padx=5, pady=5)


      
        h_r = CTkLabel(master=self.right_content, text="ealistic", text_color="#4A90E2",justify="left", font=CTkFont(family="Franklin Gothic Demi", size=21, weight="normal"))
        h_r.grid(row=2, column=1, padx=0, pady=5, sticky="w")
      
        h_i = CTkLabel(master=self.right_content, text="nvestigative", text_color="#50E3C2", font=CTkFont(family="Franklin Gothic Demi", size=21, weight="normal",))
        h_i.grid(row=3, column=1, padx=0, pady=5, sticky="w")
      
        h_a = CTkLabel(master=self.right_content, text="rtistic", text_color="#F5A623", font=CTkFont(family="Franklin Gothic Demi", size=21, weight="normal",))
        h_a.grid(row=4, column=1, padx=0, pady=5, sticky="w")
      
        h_s = CTkLabel(master=self.right_content, text="ocial", text_color="#7ED321", font=CTkFont(family="Franklin Gothic Demi", size=21, weight="normal",))
        h_s.grid(row=2, column=6, padx=0, pady=5, sticky="w")
      
        h_e= CTkLabel(master=self.right_content, text="ntreprening", text_color="#D0021B", font=CTkFont(family="Franklin Gothic Demi", size=21, weight="normal",))
        h_e.grid(row=3, column=6, padx=0, pady=5, sticky="w")
      
        h_c = CTkLabel(master=self.right_content, text="onventional", text_color="#9B9B9B", font=CTkFont(family="Franklin Gothic Demi", size=21, weight="normal",))
        h_c.grid(row=4, column=6, padx=0, pady=5,sticky="w")


        CTkLabel(self.main_content, text="Selamat Datang di Tes Kecocokan Kerja RIASEC!", justify="left", font=CTkFont(family="Franklin Gothic Demi", size=41, weight="normal",), wraplength=407, text_color=colors().text_color_dark).pack(padx=0, pady=10, anchor="w")
        CTkLabel(self.main_content, text="Tes RIASEC (Realistic, Investigative, Artistic, Social, Enterprising, Conventional) membantu Anda memahami tipe pekerjaan yang cocok berdasarkan minat dan bakat alami Anda.", justify="left", font=CTkFont(family="Franklin Gothic Book", size=15, weight="normal"), wraplength=407, text_color=colors().text_color_dark).pack(padx=0, pady=5)
        CTkButton(master=self.main_content,fg_color=colors().main_color,
                            hover_color=colors().hover_main_color,
                            font=CTkFont(family="Franklin Gothic Demi", size=20),
                            text="Mulai Test Sekarang",
                            command=self.go_to_pertanyaan,
                            text_color=colors().text_button_dark,
                            ).pack(
                                expand="True", fill = "x",
                                pady=20,
            ipadx=50, ipady=20,
        )
        CTkLabel(self.main_content, text="Ayo, mulai petualangan kariermu di sini! 🚀", justify="left", font=CTkFont(family="Franklin Gothic Demi", size=18, weight="normal"), wraplength=407, text_color=colors().text_color_dark).pack(padx=0, pady=35, anchor="w")

    def go_to_pertanyaan(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        tampilan_pertanyaan(self.window, selesai_callback=self.go_to_selesai)

    def go_to_selesai(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        tampilan_selesai(self.window)


class tampilan_pertanyaan:  
    def __init__(self, master, selesai_callback=None):
        self.window = master    
        self.selesai_callback = selesai_callback
        self.index_pertanyaan = 0
        self.pertanyaan_list = load_pertanyaan()
        self.skor = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}

        Geometri(self.window)
        self.main_frame = CTkFrame(
            master=self.window,
            bg_color=colors().background_dark,
            fg_color=colors().background_dark,
        )
        self.main_frame.pack(fill="both", expand=True)

        self.navbar_frame = CTkFrame(
            master=self.main_frame,
            height=78,
            fg_color=colors().surface_dark
        )
        self.navbar_frame.pack(fill="x", side="top", anchor="n", pady=0)

        self.text_RIASEC = CTkLabel(
            master=self.navbar_frame,
            text="RIASEC",
            text_color=colors().text_color_dark,
            font=CTkFont(family="Eras Bold ITC", size=41, weight="normal"),
            width=10, height=50
        )
        self.text_RIASEC.place(relx=.1, rely=.175)

        self.layout_grid = CTkFrame(
            master=self.main_frame,
            fg_color=colors().background_dark
        )
        self.layout_grid.pack(fill="both", expand=True, padx=120, pady=0)

        for col in range(12):
            self.layout_grid.grid_columnconfigure(col, weight=1, uniform="col", pad=20, minsize=40)
            self.layout_grid.grid_rowconfigure(0, weight=1)
            self.layout_grid.grid_rowconfigure(1, weight=1)

        self.main_content = CTkFrame(
            master=self.layout_grid,
            fg_color=colors().background_light,
            width= 919,
            height=261,
            corner_radius=30,
        )
        self.main_content.grid(
            row=0, column=1, columnspan=10,  
            padx=0, pady=53,
            sticky = "nsew",
        )

        self.label_soal_ke = CTkLabel(
            master=self.main_content,
            text=f"Soal ke - {self.index_pertanyaan + 1}",
            font=CTkFont(family="Franklin Gothic Demi", size=20),
            text_color=colors().text_color_light
        )
        self.label_soal_ke.pack(pady=(20, 10), anchor="center")

        self.label_pertanyaan = CTkLabel(
            master=self.main_content,
            text=self.pertanyaan_list[self.index_pertanyaan]["question"],
            font=CTkFont(family="Franklin Gothic Demi", size=42),
            wraplength=700,
            justify="center",
            text_color=colors().text_color_light
        )
        self.label_pertanyaan.pack(pady=(50, 20), anchor="center")

        self.no_button = CTkButton(master=self.layout_grid,fg_color=colors().danger_button,
                            hover_color=colors().hover_danger_button,
                            width=426, height=102,
                            font=CTkFont(family="Franklin Gothic Demi", size=40),
                            text="Tidak",
                            command=lambda: self.jawab(0)
                            )
        self.no_button.grid(
            row=1, column=1, columnspan=5,  
            padx=0, pady=0,
            sticky = "n",
        )
        self.yes_button = CTkButton(master=self.layout_grid,fg_color=colors().success_button,
                            hover_color=colors().hover_success_button,
                            width=426, height=102,
                            font=CTkFont(family="Franklin Gothic Demi", size=40),
                            text="Ya",
                            text_color=colors().text_button_dark,
                            command=lambda: self.jawab(1),
                            )
        self.yes_button.grid(
            row=1, column=6, columnspan=5,  
            padx=0, pady=-0,
            sticky = "n",
        )

    def jawab(self, nilai):
        if self.index_pertanyaan < len(self.pertanyaan_list):
            current_question = self.pertanyaan_list[self.index_pertanyaan]
            kategori = current_question["category"]

            self.skor[kategori] += nilai

            self.index_pertanyaan += 1

            if self.index_pertanyaan < len(self.pertanyaan_list):
                self.label_soal_ke.configure(text=f"Soal ke - {self.index_pertanyaan + 1}")
                self.label_pertanyaan.configure(
                    text=self.pertanyaan_list[self.index_pertanyaan]["question"]
                )
            else:
                if all(score == 0 for score in self.skor.values()):
                    self.tampilkan_error("Hasil tidak dapat ditampilkan karena Anda menjawab semua pertanyaan dengan 'Tidak'. ")
                elif all(score == 7 for score in self.skor.values()):
                    self.tampilkan_error("Hasil tidak dapat ditampilkan karena Anda menjawab semua pertanyaan dengan 'Ya'.")
                else:
                    self.tampilkan_hasil()


    def tampilkan_error(self, message):
        error_window = CTkFrame(self.window)
        error_window.pack(fill="both", expand=True)

        error_label = CTkLabel(
            master=error_window,
            text=message,
            font=CTkFont(family="Franklin Gothic Demi", size=20),
            text_color= 'black'
        )
        error_label.pack(pady=20)

        close_button = CTkButton(
            master=error_window,
            text="Tutup",
            command=lambda: self.close_error(error_window),
            fg_color=colors().danger_button,
            hover_color=colors().hover_danger_button
        )
        close_button.pack(pady=10)

    def close_error(self, error_window):
        error_window.destroy()
        for widget in self.window.winfo_children():
            widget.destroy()
        tampilan_awal(self.window)

    def tampilkan_hasil(self):
        print("Hasil Skor RIASEC:")
        for kategori, nilai in self.skor.items():
            print(f"{kategori}: {nilai}")

        sorted_skor = sorted(self.skor.items(), key=lambda item: item[1], reverse=True)
        interest_code = "".join([item[0] for item in sorted_skor[:3]])
        print(f"Interest Code: {interest_code}")

        jurusan, karier = get_rekomendasi(interest_code)

        hasil = {
            "scores": self.skor,
            "interest_code": interest_code,
            "rekomendasi": {
                "jurusan": jurusan,
                "karier": karier
            },
            "timestamp": datetime.datetime.now().isoformat()
        }

        if os.path.exists("hasil_riasec.json"):
            os.remove("hasil_riasec.json")

        with open("hasil_riasec.json", "w", encoding="utf-8") as f:
            json.dump(hasil, f, indent=4, ensure_ascii=False)

        if self.selesai_callback:
            for widget in self.window.winfo_children():
                widget.destroy()
            self.selesai_callback()


class tampilan_selesai:
    def __init__(self, master):
        self.window = master    

        Geometri(self.window)
        
    
        self.main_frame = CTkFrame(
            master=self.window,
            bg_color=colors().background_dark,
            fg_color=colors().background_dark,
        )
        self.main_frame.pack(fill="both", expand=True)

        self.navbar_frame = CTkFrame(
            master=self.main_frame,
            height=78,
            fg_color=colors().surface_dark
        )
        self.navbar_frame.pack(fill="x", side="top", anchor="n", pady=0)

        self.text_RIASEC = CTkLabel(
            master=self.navbar_frame,
            text="RIASEC",
            text_color=colors().text_color_dark,
            font=CTkFont(family="Eras Bold ITC", size=41, weight="normal"),
            width=10, height=50
        )
        self.text_RIASEC.place(relx=.1, rely=.175)

       
        self.layout_grid = CTkFrame(
            master=self.main_frame,
            fg_color=colors().background_dark
        )
        self.layout_grid.pack(fill="both", expand=True, padx=120, pady=0)

        for col in range(12):
            self.layout_grid.grid_columnconfigure(col, weight=1, uniform="col", pad=20, minsize=40)
            self.layout_grid.grid_rowconfigure(0, weight=1)
            self.layout_grid.grid_rowconfigure(1, weight=1)

        self.main_content = CTkFrame(
            master=self.layout_grid,
            fg_color=colors().background_light,
            width= 919,
            height=261,
            corner_radius=30,
        )
        self.main_content.grid(
            row=0, column=1, columnspan=10,  
            padx=0, pady=53,
            sticky = "nsew",
        )

        for col in range(10):
            self.main_content.grid_columnconfigure(col, weight=1, uniform="col", pad=20, minsize=40)
            self.main_content.grid_rowconfigure(0, weight=1)

        self.label_selesai = CTkLabel(
            master=self.main_content,
            text="Selesai! Terima kasih sudah mengisi tes.",
            font=CTkFont(family="Franklin Gothic Demi", size=42),
            wraplength=700,
            justify="center",
            text_color=colors().text_color_light
        )
        self.label_selesai.pack(pady=(50, 20), anchor="center", expand="y")

        self.done_button = CTkButton(master=self.layout_grid,fg_color=colors().main_color,
                            hover_color=colors().hover_main_color,
                            width=426, height=82,
                            font=CTkFont(family="Franklin Gothic Demi", size=40),
                            text="Lihat Hasil",
                            text_color=colors().text_button_dark,
                            command=self.go_to_hasil
                            )
        self.done_button.grid(
            row=1, column=1, columnspan=10,  
            padx=0, pady=0,
            sticky = "new",
            
        )
    
    def go_to_hasil(self):
        for w in self.window.winfo_children():
            w.destroy()
        tampilan_hasil(self.window)

class tampilan_hasil: 
    def __init__(self, master):
        self.window = master
        Geometri(self.window)
        with open("hasil_riasec.json", "r", encoding="utf-8") as f:
            hasil = json.load(f)

        self.scores = hasil["scores"]
        self.kode = hasil["interest_code"]
        jurusan = hasil["rekomendasi"]["jurusan"]
        karier = hasil["rekomendasi"]["karier"]

        self.main_container = CTkFrame(master=self.window, fg_color="#1e1e1e")
        self.main_container.pack(fill="both", expand=True)
        
        self.scrollable_frame = CTkScrollableFrame(master=self.main_container, fg_color="#1e1e1e")
        self.scrollable_frame.pack(fill="both", expand=True, padx=30, pady=30)

        self.frame_atas = CTkFrame(master=self.scrollable_frame, fg_color="#1e1e1e")
        self.frame_atas.pack(pady=(0, 20))

        self.judul = CTkLabel(
            self.frame_atas,
            text=f"Selamat Kamu adalah: {self.kode}",
            font=CTkFont("Franklin Gothic Demi", 30, weight="bold"),
            text_color="white"
        )
        self.judul.grid(row=0, column=0, columnspan=6, pady=(10, 20))

        kategori_info = [
            ("Realistic", "R", "#4A90E2"),
            ("Investigative", "I", "#50E3C2"),
            ("Artistic", "A", "#F5A623"),
            ("Social", "S", "#7ED321"),
            ("Enterprising", "E", "#D0021B"),
            ("Conventional", "C", "#9B9B9B"),
        ]

        self.frames = {}
        frame_width = 1100
        frame_per_kolom = int(frame_width / 6)

        for idx, (nama, kode, warna) in enumerate(kategori_info):
            frame = CTkFrame(master=self.frame_atas, width=frame_per_kolom, height=150, fg_color=warna)
            frame.grid(row=1, column=idx, padx=5, pady=10, sticky="nsew")
            frame.grid_propagate(False)
            frame.grid_columnconfigure(0, weight=1)

            skor = self.scores.get(kode, 0)

            CTkLabel(
                master=frame,
                font=CTkFont(family="Franklin Gothic Demi", size=20),
                text_color=colors().background_dark,
                text=nama
            ).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

            CTkLabel(
                master=frame,
                font=CTkFont(family="Franklin Gothic Demi", size=30),
                text_color=colors().background_dark,
                text=kode
            ).grid(row=1, column=0, padx=5, pady=2, sticky="nsew")

            CTkLabel(
                master=frame,
                font=CTkFont(family="Franklin Gothic Demi", size=35),
                text_color=colors().background_dark,
                text=str(skor)
            ).grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

            self.frames[kode] = frame

        self.frame_bawah = CTkFrame(master=self.scrollable_frame, fg_color="#1e1e1e")
        self.frame_bawah.pack(fill="both", expand=True, padx=50, pady=(0, 20))

        frame_jurusan = CTkFrame(self.frame_bawah, fg_color="#2e2e2e")
        frame_jurusan.pack(side="left", fill="both", expand=True, padx=10)

        label_jurusan = CTkLabel(frame_jurusan, text="Rekomendasi Jurusan", font=CTkFont("Franklin Gothic Demi", 20), text_color="white")
        label_jurusan.pack(pady=10)

        jurusan_scroll = CTkScrollableFrame(frame_jurusan, fg_color="#2e2e2e")
        jurusan_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        for j in jurusan:
            CTkLabel(jurusan_scroll, text="• " + j, anchor="w", justify="left", font=CTkFont("Franklin Gothic Demi", 16), text_color="white", wraplength=500).pack(anchor="w", pady=5)

        frame_karier = CTkFrame(self.frame_bawah, fg_color="#2e2e2e")
        frame_karier.pack(side="right", fill="both", expand=True, padx=10)

        label_karier = CTkLabel(frame_karier, text="Rekomendasi Pekerjaan", font=CTkFont("Franklin Gothic Demi", 20), text_color="white")
        label_karier.pack(pady=10)

        karier_scroll = CTkScrollableFrame(frame_karier, fg_color="#2e2e2e")
        karier_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        for k in karier:
            CTkLabel(karier_scroll, text="• " + k, anchor="w", justify="left", font=CTkFont("Franklin Gothic Demi", 16), text_color="white", wraplength=500).pack(anchor="w", pady=5)

        self.frame_tombol = CTkFrame(master=self.scrollable_frame, fg_color="#1e1e1e")
        self.frame_tombol.pack(fill="both", expand=True, padx=50, pady=(0, 20))

        self.button_kembali = CTkButton(
            master=self.frame_tombol,
            text="Kembali ke Beranda",
            command=self.kembali_ke_beranda,
            fg_color=colors().main_color,
            hover_color=colors().hover_main_color,
            font=CTkFont("Franklin Gothic Demi", 24),
            text_color=colors().text_button_dark,
            height=55,
            width=400,
            corner_radius=16
        )
        self.button_kembali.pack(pady=10)

    def kembali_ke_beranda(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        tampilan_awal(self.window)


if __name__ == "__main__":
    window = CTk()
    window.resizable(True, True)
    gui = tampilan_awal(window)
    window.mainloop()
