import os
import subprocess
import platform
import customtkinter as ctk
from tkinter import filedialog, messagebox
from uuid import uuid4
from PIL import Image
from pathlib import Path
import threading

# === INTEGRAÇÃO COM CONFIG.PY ===
from config import load_env_config, get_db_origins, get_db_names, get_origin_combo_values, get_db_combo_values

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
    "3": "master",
    "9": None
}

# Função para executar comandos no terminal com exibição de logs
def executar_comando(comando, log_text, status_label):
    try:
        status_label.configure(text="Executando...", text_color="yellow")
        processo = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while True:
            saida = processo.stdout.readline()
            if saida == '' and processo.poll() is not None:
                break
            if saida:
                log_text.configure(state="normal")
                log_text.insert(ctk.END, saida.strip() + "\n")
                log_text.see(ctk.END)
                log_text.configure(state="disabled")
        processo.wait()
        if processo.returncode != 0:
            erros = processo.stderr.read().strip()
            log_text.configure(state="normal")
            log_text.insert(ctk.END, f"ERRO: {erros}\n")
            log_text.see(ctk.END)
            log_text.configure(state="disabled")
            status_label.configure(text="Erro na execução", text_color="red")
            return False
        status_label.configure(text="Comando concluído", text_color="green")
        return True
    except Exception as e:
        log_text.configure(state="normal")
        log_text.insert(ctk.END, f"Erro ao executar comando: {e}\n")
        log_text.see(ctk.END)
        log_text.configure(state="disabled")
        status_label.configure(text="Erro na execução", text_color="red")
        return False

# Função para seleção de diretório do projeto
def selecionar_diretorio_projeto(diretorio_entry, branch_combo, start_button):
    diretorio = filedialog.askdirectory(title="Selecione a pasta do projeto")
    if diretorio:
        diretorio_entry.delete(0, ctk.END)
        diretorio_entry.insert(0, diretorio)
        os.chdir(diretorio)
        atualizar_branches(diretorio, branch_combo)
        start_button.configure(state="normal")

# Função para atualizar lista de branches
def atualizar_branches(diretorio, branch_combo):
    try:
        resultado = subprocess.run(["git", "branch", "-r"], capture_output=True, text=True, cwd=diretorio)
        branches = [line.split('/')[-1].strip() for line in resultado.stdout.splitlines() if "->" not in line]
        branch_combo.configure(values=branches)
        if branches:
            branch_combo.set(branches[0])
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar branches: {e}")

# Função para iniciar o processo de compilação
def iniciar_processo(diretorio_entry, branch_combo, banco_combo, origem_combo, compilacao_combo, branch_origem_combo, log_text, status_label, start_button):
    diretorio = diretorio_entry.get()
    branch = branch_combo.get()
    banco_opcao = banco_combo.get()
    origem_opcao = origem_combo.get()
    compilacao_opcao = compilacao_combo.get()
    branch_origem_opcao = branch_origem_combo.get()

    if not diretorio or not branch:
        messagebox.showwarning("Aviso", "Selecione o diretório do projeto e a branch.")
        return

    start_button.configure(state="disabled")
    log_text.configure(state="normal")
    log_text.insert(ctk.END, f"Computador: {platform.node()} | Usuário: {os.getlogin()}\n")
    log_text.insert(ctk.END, f"Diretório do projeto: {diretorio}\n")
    log_text.insert(ctk.END, f"Realizando checkout em {branch}\n")
    log_text.see(ctk.END)
    log_text.configure(state="disabled")

    # Passo 1: Checkout e pull
    if not executar_comando(f"git checkout {branch}", log_text, status_label):
        start_button.configure(state="normal")
        return

    if not executar_comando("git pull", log_text, status_label):
        start_button.configure(state="normal")
        return

    # Passo 2: Merge da branch de origem
    branch_origem = branch_origem_map.get(branch_origem_opcao)
    if branch_origem:
        log_text.configure(state="normal")
        log_text.insert(ctk.END, f"Trazendo branch de origem: {branch_origem}\n")
        log_text.see(ctk.END)
        log_text.configure(state="disabled")
        if not executar_comando(f"git merge origin/{branch_origem}", log_text, status_label):
            start_button.configure(state="normal")
            return
        if not executar_comando(f"git push origin {branch}", log_text, status_label):
            start_button.configure(state="normal")
            return

    # Passo 3: Configuração do banco
    # Recarrega as configurações do arquivo .env para garantir que temos os dados mais recentes
    load_env_config()
    origem_map_atual = get_db_origins()
    banco_map_atual = get_db_names()
    
    # Obtém as configurações selecionadas
    banco_id = banco_opcao.split('.')[0]
    origem_id = origem_opcao.split('.')[0]
    
    banco = banco_map_atual.get(banco_id, banco_map.get(banco_id, "waybe"))
    ip_banco, porta_banco, usuario_banco, senha_banco = origem_map_atual.get(origem_id, origem_map.get(origem_id, ("127.0.0.1", "3306", "root", "root")))

    # Passo 4: Compilação com Maven
    mvn_comando = f"mvn -T 10 clean install -am -Dgenerator-phase=generate-sources -Duser={usuario_banco} -Dpass={senha_banco} -Durl=jdbc:mysql://{ip_banco}:{porta_banco}/{banco}?useSSL=false -DskipTests=true"
    log_text.configure(state="normal")
    log_text.insert(ctk.END, f"Executando: {mvn_comando}\n")
    log_text.see(ctk.END)
    log_text.configure(state="disabled")

    if executar_comando(mvn_comando, log_text, status_label):
        log_text.configure(state="normal")
        log_text.insert(ctk.END, "Compilação finalizada com sucesso.\n")
        log_text.see(ctk.END)
        log_text.configure(state="disabled")
    else:
        log_text.configure(state="normal")
        log_text.insert(ctk.END, "Compilação finalizada com erros.\n")
        log_text.see(ctk.END)
        log_text.configure(state="disabled")

    start_button.configure(state="normal")

# Configuração da Janela Principal
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.title("Sifat Compilador Waybe Web Java")
app.geometry("1100x1000")
app.resizable(True, True)

# Cabeçalho
header_frame = ctk.CTkFrame(app)
header_frame.pack(fill="x", padx=20, pady=20)
title = ctk.CTkLabel(header_frame, text="Gerenciador de Branches e Projeto", font=ctk.CTkFont(size=28, weight="bold"))
title.pack()

# Projeto (Diretório)
project_frame = ctk.CTkFrame(app, width=1000)
project_frame.pack(fill="x", padx=20, pady=10)
ctk.CTkLabel(project_frame, text="📁 Pasta do Projeto", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=10, pady=5)

project_select_frame = ctk.CTkFrame(project_frame)
project_select_frame.pack(fill="x", pady=5)
diretorio_entry = ctk.CTkEntry(project_select_frame, placeholder_text="Selecione o diretório do projeto")
diretorio_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
diretorio_button = ctk.CTkButton(project_select_frame, text="Selecionar", command=lambda: selecionar_diretorio_projeto(diretorio_entry, branch_combo, start_button))
diretorio_button.pack(side="right")

# Configurações (Branch, Banco, Compilação)
config_frame = ctk.CTkFrame(app, width=1000)
config_frame.pack(fill="x", padx=20, pady=10)
ctk.CTkLabel(config_frame, text="⚙️ Configurações", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=10, pady=5)

config_grid = ctk.CTkFrame(config_frame)
config_grid.pack(fill="x", padx=10, pady=5)
config_grid.columnconfigure((0, 1), weight=1)

# Branch
ctk.CTkLabel(config_grid, text="Branch:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
branch_combo = ctk.CTkComboBox(config_grid, width=400)
branch_combo.grid(row=0, column=1, sticky="w", padx=5, pady=5)

# Banco
ctk.CTkLabel(config_grid, text="Banco:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
banco_combo = ctk.CTkComboBox(config_grid, width=400, values=get_db_combo_values())
banco_combo.grid(row=1, column=1, sticky="w", padx=5, pady=5)

# Origem do Banco
ctk.CTkLabel(config_grid, text="Origem do Banco:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
origem_combo = ctk.CTkComboBox(config_grid, width=400, values=get_origin_combo_values())
origem_combo.grid(row=2, column=1, sticky="w", padx=5, pady=5)

# Compilação
ctk.CTkLabel(config_grid, text="Compilação:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
compilacao_combo = ctk.CTkComboBox(config_grid, width=400, values=["1. Compile ALL", "2. Compile ERP", "3. Compile API", "4. Compile WAYCHEF"])
compilacao_combo.grid(row=3, column=1, sticky="w", padx=5, pady=5)

# Branch de Origem
ctk.CTkLabel(config_grid, text="Branch de Origem:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
branch_origem_combo = ctk.CTkComboBox(config_grid, width=400, values=["1. working", "2. rc", "3. master", "9. NÃO LEVAR ORIGEM"])
branch_origem_combo.grid(row=4, column=1, sticky="w", padx=5, pady=5)

# Execução e Logs
execution_frame = ctk.CTkFrame(app, width=1000)
execution_frame.pack(fill="both", expand=True, padx=20, pady=10)
ctk.CTkLabel(execution_frame, text="📜 Logs de Execução", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=10, pady=5)

status_label = ctk.CTkLabel(execution_frame, text="Aguardando início", text_color="gray")
status_label.pack(anchor="w", padx=10, pady=5)

log_box = ctk.CTkTextbox(execution_frame, height=300, state="disabled")
log_box.pack(fill="both", expand=True, padx=10, pady=10)

# Botões de Controle
btn_frame = ctk.CTkFrame(app)
btn_frame.pack(fill="x", padx=20, pady=10)

start_button = ctk.CTkButton(btn_frame, text="Iniciar Processo", state="disabled", width=200, command=lambda: threading.Thread(target=iniciar_processo, args=(diretorio_entry, branch_combo, banco_combo, origem_combo, compilacao_combo, branch_origem_combo, log_box, status_label, start_button), daemon=True).start())
start_button.pack(side="left", padx=5)

# Botão para abrir a tela de configuração
def abrir_tela_configuracao():
    import subprocess
    subprocess.Popen(["python", "config.py"])

config_button = ctk.CTkButton(btn_frame, text="Configuração", command=abrir_tela_configuracao)
config_button.pack(side="left", padx=5)

clear_button = ctk.CTkButton(btn_frame, text="Limpar Log", command=lambda: log_box.configure(state="normal") or log_box.delete(1.0, ctk.END) or log_box.configure(state="disabled"))
clear_button.pack(side="right", padx=5)

app.mainloop()
