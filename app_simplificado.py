import os
import subprocess
import platform
import customtkinter as ctk
from tkinter import filedialog, messagebox
from uuid import uuid4
from PIL import Image
from pathlib import Path
import threading

# === INTEGRAÇÃO COM CONFIG_SIMPLIFICADO.PY ===
# Importa as funções do config_simplificado.py em vez de config.py
from config_simplificado import load_env_config, get_db_origins, get_db_names, get_origin_combo_values, get_db_combo_values

# Carrega as configurações do arquivo .env
load_env_config()

# Obtém as configurações de banco de dados do arquivo .env
origem_map = get_db_origins()
banco_map = get_db_names()

compilacao_map = {
    "1": "ALL",
    "2": "ERP",
    "3": "API",
    "4": "WAYCHEF"
}

branch_origem_map = {
    "1": "working",
    "2": "rc",
    "3": "master"
}

branch_destino_map = {
    "1": "working",
    "2": "rc",
    "3": "master"
}

# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuração da janela principal
        self.title("Way Compilador")
        self.geometry("800x600")
        
        # Variáveis de controle
        self.origem_var = ctk.StringVar(value="")
        self.banco_var = ctk.StringVar(value="")
        self.compilacao_var = ctk.StringVar(value="")
        self.branch_origem_var = ctk.StringVar(value="")
        self.branch_destino_var = ctk.StringVar(value="")
        self.pasta_var = ctk.StringVar(value="")
        
        # Cria o layout
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="Way Compilador", font=("Arial", 24, "bold"))
        title_label.pack(pady=10)
        
        # Frame para os campos
        fields_frame = ctk.CTkFrame(main_frame)
        fields_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # === Origem do Banco ===
        origem_frame = ctk.CTkFrame(fields_frame)
        origem_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(origem_frame, text="Origem do Banco:", width=120).pack(side="left", padx=5)
        
        # Recarrega as configurações antes de criar o ComboBox
        global origem_map
        origem_map = get_db_origins()
        origem_values = get_origin_combo_values()
        
        self.origem_combo = ctk.CTkComboBox(origem_frame, values=origem_values, width=300, variable=self.origem_var)
        self.origem_combo.pack(side="left", padx=5, fill="x", expand=True)
        
        # Botão para configurar origens
        def abrir_config_origem():
            # Executa o arquivo config_simplificado.py
            subprocess.Popen(["python", "config_simplificado.py"])
        
        btn_config_origem = ctk.CTkButton(origem_frame, text="Configurar", width=100, command=abrir_config_origem)
        btn_config_origem.pack(side="right", padx=5)
        
        # === Nome do Banco ===
        banco_frame = ctk.CTkFrame(fields_frame)
        banco_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(banco_frame, text="Nome do Banco:", width=120).pack(side="left", padx=5)
        
        # Recarrega as configurações antes de criar o ComboBox
        global banco_map
        banco_map = get_db_names()
        banco_values = get_db_combo_values()
        
        self.banco_combo = ctk.CTkComboBox(banco_frame, values=banco_values, width=300, variable=self.banco_var)
        self.banco_combo.pack(side="left", padx=5, fill="x", expand=True)
        
        # Botão para configurar bancos
        def abrir_config_banco():
            # Executa o arquivo config_simplificado.py
            subprocess.Popen(["python", "config_simplificado.py"])
        
        btn_config_banco = ctk.CTkButton(banco_frame, text="Configurar", width=100, command=abrir_config_banco)
        btn_config_banco.pack(side="right", padx=5)
        
        # === Tipo de Compilação ===
        compilacao_frame = ctk.CTkFrame(fields_frame)
        compilacao_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(compilacao_frame, text="Compilação:", width=120).pack(side="left", padx=5)
        
        compilacao_values = [f"{id}. {name}" for id, name in compilacao_map.items()]
        self.compilacao_combo = ctk.CTkComboBox(compilacao_frame, values=compilacao_values, width=300, variable=self.compilacao_var)
        self.compilacao_combo.pack(side="left", padx=5, fill="x", expand=True)
        
        # === Branch Origem ===
        branch_origem_frame = ctk.CTkFrame(fields_frame)
        branch_origem_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(branch_origem_frame, text="Branch Origem:", width=120).pack(side="left", padx=5)
        
        branch_origem_values = [f"{id}. {name}" for id, name in branch_origem_map.items()]
        self.branch_origem_combo = ctk.CTkComboBox(branch_origem_frame, values=branch_origem_values, width=300, variable=self.branch_origem_var)
        self.branch_origem_combo.pack(side="left", padx=5, fill="x", expand=True)
        
        # === Branch Destino ===
        branch_destino_frame = ctk.CTkFrame(fields_frame)
        branch_destino_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(branch_destino_frame, text="Branch Destino:", width=120).pack(side="left", padx=5)
        
        branch_destino_values = [f"{id}. {name}" for id, name in branch_destino_map.items()]
        self.branch_destino_combo = ctk.CTkComboBox(branch_destino_frame, values=branch_destino_values, width=300, variable=self.branch_destino_var)
        self.branch_destino_combo.pack(side="left", padx=5, fill="x", expand=True)
        
        # === Pasta de Destino ===
        pasta_frame = ctk.CTkFrame(fields_frame)
        pasta_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(pasta_frame, text="Pasta Destino:", width=120).pack(side="left", padx=5)
        
        self.pasta_entry = ctk.CTkEntry(pasta_frame, width=300, textvariable=self.pasta_var)
        self.pasta_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        def selecionar_pasta():
            pasta = filedialog.askdirectory(title="Selecione a pasta de destino")
            if pasta:
                self.pasta_var.set(pasta)
        
        btn_pasta = ctk.CTkButton(pasta_frame, text="Procurar", width=100, command=selecionar_pasta)
        btn_pasta.pack(side="right", padx=5)
        
        # === Botão de Compilação ===
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        def compilar():
            # Verifica se todos os campos estão preenchidos
            if not self.origem_var.get() or not self.banco_var.get() or not self.compilacao_var.get() or \
               not self.branch_origem_var.get() or not self.branch_destino_var.get() or not self.pasta_var.get():
                messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
                return
            
            # Obtém os IDs dos valores selecionados
            origem_id = self.origem_var.get().split(".")[0]
            banco_id = self.banco_var.get().split(".")[0]
            compilacao_id = self.compilacao_var.get().split(".")[0]
            branch_origem_id = self.branch_origem_var.get().split(".")[0]
            branch_destino_id = self.branch_destino_var.get().split(".")[0]
            
            # Recarrega as configurações para garantir que temos os dados mais recentes
            load_env_config()
            origem_map = get_db_origins()
            banco_map = get_db_names()
            
            # Obtém os valores correspondentes aos IDs
            origem = origem_map.get(origem_id)
            banco = banco_map.get(banco_id)
            compilacao = compilacao_map.get(compilacao_id)
            branch_origem = branch_origem_map.get(branch_origem_id)
            branch_destino = branch_destino_map.get(branch_destino_id)
            pasta_destino = self.pasta_var.get()
            
            if not origem or not banco or not compilacao or not branch_origem or not branch_destino:
                messagebox.showerror("Erro", "Configuração inválida.")
                return
            
            # Exibe as informações de compilação
            ip, porta, usuario, senha = origem
            mensagem = f"Compilação iniciada:\n\n"
            mensagem += f"Origem: {ip}:{porta} (usuário: {usuario})\n"
            mensagem += f"Banco: {banco}\n"
            mensagem += f"Tipo: {compilacao}\n"
            mensagem += f"Branch Origem: {branch_origem}\n"
            mensagem += f"Branch Destino: {branch_destino}\n"
            mensagem += f"Pasta: {pasta_destino}\n"
            
            messagebox.showinfo("Compilação", mensagem)
            
            # Aqui você pode adicionar o código para executar a compilação
            # Por exemplo, chamar um script Maven ou outro processo
        
        btn_compilar = ctk.CTkButton(btn_frame, text="Compilar", font=("Arial", 16, "bold"), 
                                     height=40, command=compilar)
        btn_compilar.pack(pady=10)
        
        # === Status ===
        self.status_label = ctk.CTkLabel(main_frame, text="Pronto para compilar", font=("Arial", 12))
        self.status_label.pack(pady=5)

if __name__ == "__main__":
    app = App()
    app.mainloop()