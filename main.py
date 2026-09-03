import os
import threading
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Import the new engine
from engine import INPEDownloader

# Configuração de estilo macOS
ctk.set_appearance_mode("System")

class DownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Embracedata Downloader")
        self.geometry("1100x750")
        self.minsize(950, 600)
        self.resizable(True, True)

        sf_font = "SF Pro Display"
        sf_text = "SF Pro Text"

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.save_dir = os.path.expanduser("~/Dados/Embracedata")
        self.engine = None

        # ==================== SIDEBAR ====================
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=("gray92", "gray12"))
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="Embracedata", font=ctk.CTkFont(family=sf_font, size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(35, 20), sticky="w")

        self.btn_nav_down = ctk.CTkButton(self.sidebar, text="📥  Nova Transferência", fg_color=("gray82", "gray22"), text_color=("black", "white"), anchor="w", font=ctk.CTkFont(family=sf_text, size=14, weight="bold"))
        self.btn_nav_down.grid(row=1, column=0, padx=15, pady=2, sticky="ew")

        # ==================== MAIN CONTENT (Scrollable) ====================
        self.main_content = ctk.CTkScrollableFrame(self, fg_color=("gray98", "gray7"), corner_radius=0)
        self.main_content.grid(row=0, column=1, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkLabel(self.main_content, text="Baixar Dados do INPE", font=ctk.CTkFont(family=sf_font, size=32, weight="bold"))
        self.header.grid(row=0, column=0, padx=35, pady=(25, 0), sticky="w")
        
        self.subtitle = ctk.CTkLabel(self.main_content, text="Siga os 3 passos abaixo para configurar e extrair os arquivos científicos.", text_color="gray", font=ctk.CTkFont(family=sf_text, size=14))
        self.subtitle.grid(row=1, column=0, padx=35, pady=(0, 20), sticky="w")

        # ====== PASSO 1: PERÍODO ======
        self.card_periodo = ctk.CTkFrame(self.main_content, fg_color=("white", "gray15"), corner_radius=12)
        self.card_periodo.grid(row=2, column=0, padx=30, pady=10, sticky="ew")

        ctk.CTkLabel(self.card_periodo, text="1. Qual o período de dados?", font=ctk.CTkFont(family=sf_text, size=18, weight="bold")).grid(row=0, column=0, columnspan=4, padx=25, pady=(20, 5), sticky="w")
        
        dias = [str(i).zfill(2) for i in range(1, 32)]
        meses = [str(i).zfill(2) for i in range(1, 13)]
        anos = [str(i) for i in range(2010, 2027)]

        ctk.CTkLabel(self.card_periodo, text="De (Data Inicial):", text_color="gray").grid(row=1, column=0, padx=25, pady=(5,20), sticky="w")
        frame_ini = ctk.CTkFrame(self.card_periodo, fg_color="transparent")
        frame_ini.grid(row=1, column=1, padx=(0, 20), pady=(5,20), sticky="w")
        self.dia_ini = ctk.CTkOptionMenu(frame_ini, values=dias, width=65, fg_color=("gray90", "gray22"), text_color=("black", "white"), button_color=("gray80", "gray30"), command=self.on_start_date_change)
        self.dia_ini.pack(side="left", padx=(0, 5))
        self.mes_ini = ctk.CTkOptionMenu(frame_ini, values=meses, width=65, fg_color=("gray90", "gray22"), text_color=("black", "white"), button_color=("gray80", "gray30"), command=self.on_start_date_change)
        self.mes_ini.pack(side="left", padx=(0, 5))
        self.ano_ini = ctk.CTkOptionMenu(frame_ini, values=anos, width=80, fg_color=("gray90", "gray22"), text_color=("black", "white"), button_color=("gray80", "gray30"), command=self.on_start_date_change)
        self.ano_ini.pack(side="left")

        ctk.CTkLabel(self.card_periodo, text="Até (Data Final):", text_color="gray").grid(row=1, column=2, padx=40, pady=(5,20), sticky="w")
        frame_fim = ctk.CTkFrame(self.card_periodo, fg_color="transparent")
        frame_fim.grid(row=1, column=3, padx=(0, 20), pady=(5,20), sticky="w")
        self.dia_fim = ctk.CTkOptionMenu(frame_fim, values=dias, width=65, fg_color=("gray90", "gray22"), text_color=("black", "white"), button_color=("gray80", "gray30"))
        self.dia_fim.pack(side="left", padx=(0, 5))
        self.mes_fim = ctk.CTkOptionMenu(frame_fim, values=meses, width=65, fg_color=("gray90", "gray22"), text_color=("black", "white"), button_color=("gray80", "gray30"))
        self.mes_fim.pack(side="left", padx=(0, 5))
        self.ano_fim = ctk.CTkOptionMenu(frame_fim, values=anos, width=80, fg_color=("gray90", "gray22"), text_color=("black", "white"), button_color=("gray80", "gray30"))
        self.ano_fim.pack(side="left")

        # ====== PASSO 2: TIPOS DE ARQUIVO ======
        self.card_tipos = ctk.CTkFrame(self.main_content, fg_color=("white", "gray15"), corner_radius=12)
        self.card_tipos.grid(row=3, column=0, padx=30, pady=10, sticky="ew")
        self.card_tipos.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.card_tipos, text="2. Quais tipos de arquivo?", font=ctk.CTkFont(family=sf_text, size=18, weight="bold")).grid(row=0, column=0, padx=25, pady=(20, 5), sticky="w")
        
        self.frame_switches = ctk.CTkFrame(self.card_tipos, fg_color="transparent")
        self.frame_switches.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.frame_switches.grid_columnconfigure((0, 1, 2), weight=1)
        
        tipos = [('SAO', 'Ionogramas'), ('RSF', 'Resumos'), ('DFT', 'Drift Data'), ('SKY', 'Sky Maps'), ('DVL', 'Doppler Velocity')]
        self.type_vars = {}
        for i, (sigla, desc) in enumerate(tipos):
            sw = ctk.CTkSwitch(self.frame_switches, text=f"{sigla} ({desc})", font=ctk.CTkFont(family=sf_text, size=14), progress_color=("#34C759", "#30D158"))
            sw.grid(row=i // 3, column=i % 3, padx=10, pady=12, sticky="ew")
            self.type_vars[sigla] = sw

        # ====== PASSO 3: ESTAÇÕES ======
        self.card_cities = ctk.CTkFrame(self.main_content, fg_color=("white", "gray15"), corner_radius=12)
        self.card_cities.grid(row=4, column=0, padx=30, pady=10, sticky="ew")
        self.card_cities.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.card_cities, text="3. Em quais estações (Cidades)?", font=ctk.CTkFont(family=sf_text, size=18, weight="bold")).grid(row=0, column=0, padx=25, pady=(20, 5), sticky="w")
        
        self.frame_cities = ctk.CTkFrame(self.card_cities, fg_color="transparent")
        self.frame_cities.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.frame_cities.grid_columnconfigure((0, 1), weight=1)
        
        self.city_mapping = {
            'Belém, PA': 'BLJ03', 'Boa Vista, RR': 'BVJ03', 'Cachoeira Paulista, SP': 'CAJ2M', 'Campo Grande, MS': 'CGK21', 
            'Fortaleza, CE': 'FZA0M', 'São José dos Campos, SP': 'SAA0K', 'Santarém, PA': 'SAJ03', 'Santa Maria, RS': 'SMK29'
        }
        self.city_vars = {}
        for i, cidade in enumerate(self.city_mapping.keys()):
            chk = ctk.CTkCheckBox(self.frame_cities, text=cidade, font=ctk.CTkFont(family=sf_text, size=14), fg_color=("#007AFF", "#0A84FF"))
            chk.grid(row=i // 2, column=i % 2, padx=10, pady=12, sticky="ew")
            self.city_vars[cidade] = chk

        # ====== ACTION BAR ======
        self.action_bar = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.action_bar.grid(row=5, column=0, padx=30, pady=20, sticky="ew")
        self.action_bar.grid_columnconfigure(1, weight=1)

        self.dir_frame = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        self.dir_frame.grid(row=0, column=0, sticky="w")
        self.lbl_dir = ctk.CTkLabel(self.dir_frame, text=f"📁 Destino: {self.save_dir}", text_color="gray", font=ctk.CTkFont(family=sf_text, size=13))
        self.lbl_dir.grid(row=0, column=0, padx=(0, 10))
        self.btn_dir = ctk.CTkButton(self.dir_frame, text="Mudar...", width=70, fg_color=("gray85", "gray25"), text_color=("black", "white"), command=self.change_dir)
        self.btn_dir.grid(row=0, column=1)

        self.btn_cancel = ctk.CTkButton(self.action_bar, text="Parar Download", state="disabled", fg_color="transparent", text_color=("#FF3B30", "#FF453A"), width=120, command=self.cancel_download)
        self.btn_cancel.grid(row=0, column=1, sticky="e", padx=10)

        self.btn_start = ctk.CTkButton(self.action_bar, text="Iniciar Transferência", fg_color=("#007AFF", "#0A84FF"), font=ctk.CTkFont(family=sf_text, size=15, weight="bold"), width=180, height=36, command=self.start_download_process)
        self.btn_start.grid(row=0, column=2, sticky="e")

        # ====== PROGRESS BAR & LOGS ======
        self.progress_bar = ctk.CTkProgressBar(self.main_content, height=6, progress_color=("#007AFF", "#0A84FF"), fg_color=("gray85", "gray25"))
        self.progress_bar.grid(row=6, column=0, padx=30, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0.0)
        
        self.log_box = ctk.CTkTextbox(self.main_content, height=120, font=("Menlo", 12), fg_color=("gray95", "gray10"))
        self.log_box.grid(row=7, column=0, padx=30, pady=(0, 20), sticky="ew")
        self.log_box.insert("0.0", "Logs do Sistema...\n")
        self.log_box.configure(state="disabled")

    def on_start_date_change(self, _):
        """Auto-ajusta a Data Final se a Data Inicial for superior"""
        try:
            start_d = datetime(int(self.ano_ini.get()), int(self.mes_ini.get()), int(self.dia_ini.get()))
            end_d = datetime(int(self.ano_fim.get()), int(self.mes_fim.get()), int(self.dia_fim.get()))
            
            if start_d > end_d:
                self.dia_fim.set(self.dia_ini.get())
                self.mes_fim.set(self.mes_ini.get())
                self.ano_fim.set(self.ano_ini.get())
        except ValueError:
            pass # Ignora se a data temporariamente formada for inválida (ex: 31 de fev)

    def change_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.save_dir = dir_path
            self.lbl_dir.configure(text=f"📁 Destino: {self.save_dir}")

    def append_log(self, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def update_progress(self, current, total):
        if total > 0:
            self.progress_bar.set(current / total)
        self.update_idletasks()

    def cancel_download(self):
        if self.engine:
            self.engine.cancel()
            self.append_log("[!] Solicitando cancelamento ao motor...")
            self.btn_cancel.configure(state="disabled")

    def start_download_process(self):
        try:
            start_d = datetime(int(self.ano_ini.get()), int(self.mes_ini.get()), int(self.dia_ini.get()))
            end_d = datetime(int(self.ano_fim.get()), int(self.mes_fim.get()), int(self.dia_fim.get()))
            if start_d > end_d:
                messagebox.showerror("Erro de Data", "A Data Inicial não pode ser maior que a Data Final.")
                return
        except ValueError:
            messagebox.showerror("Erro de Data", "Data selecionada é inválida (ex: 31 de Fevereiro).")
            return

        selected_types = [sigla for sigla, sw in self.type_vars.items() if sw.get() == 1]
        selected_cities = [self.city_mapping[cidade] for cidade, chk in self.city_vars.items() if chk.get() == 1]

        if not selected_types:
            messagebox.showwarning("Aviso", "Selecione ao menos um Tipo de Arquivo.")
            return
        if not selected_cities:
            messagebox.showwarning("Aviso", "Selecione ao menos uma Estação.")
            return

        # Prepare UI
        self.progress_bar.set(0.0)
        self.btn_start.configure(state="disabled", text="Baixando...")
        self.btn_cancel.configure(state="normal")
        self.log_box.configure(state="normal")
        self.log_box.delete("0.0", "end")
        self.log_box.configure(state="disabled")
        
        self.engine = INPEDownloader(
            output_dir=self.save_dir,
            logger_callback=self.append_log,
            progress_callback=self.update_progress
        )

        threading.Thread(target=self.run_engine_thread, args=(start_d, end_d, selected_cities, selected_types), daemon=True).start()

    def run_engine_thread(self, start_d, end_d, selected_cities, selected_types):
        # This blocks only the background thread
        self.engine.start_download(start_d, end_d, selected_cities, selected_types)
        
        # Re-enable UI safely
        self.after(0, self._finish_download_ui)

    def _finish_download_ui(self):
        self.btn_start.configure(state="normal", text="Iniciar Transferência")
        self.btn_cancel.configure(state="disabled")
        self.progress_bar.set(1.0)
        messagebox.showinfo("Concluído", "Processo finalizado. Verifique os logs para detalhes.")

if __name__ == "__main__":
    app = DownloaderApp()
    app.mainloop()
