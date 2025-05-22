# import os
# import subprocess
# import platform
# import customtkinter as ctk
# from tkinter import filedialog, messagebox
# from PIL import Image
# from pathlib import Path

# # Configuração do Maven e Java
# os.environ['JAVA_HOME'] = r"C:\Program Files (x86)\Java\jdk-1.8"
# os.environ['PATH'] = f"{os.environ['JAVA_HOME']}\bin;{os.environ['PATH']}"
# os.environ['M2'] = r"C:\apache-maven-3.8.5"
# os.environ['PATH'] = f"{os.environ['M2']}\bin;{os.environ['PATH']}"
# os.environ['MAVEN_OPTS'] = "-Xmx1024m"

# # Configurações padrão do banco de dados
# origem_map = {
#     "1": ("127.0.0.1", "3306", "root", "root"),
#     "2": ("192.168.5.174", "3306", "root", "root"),
#     "3": ("192.168.5.217", "3306", "root", "root"),
#     "4": ("127.0.0.1", "3309", "root", "root"),
#     "5": ("rasp.local", "3306", "root", "root")
# }

# # Função para executar comandos no terminal com exibição de logs

# def executar_comando(comando, log_text):
#     try:
#         processo = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         while True:
#             saida = processo.stdout.readline()
#             if saida == '' and processo.poll() is not None:
#                 break
#             if saida:
#                 log_text.configure(state="normal")
#                 log_text.insert(ctk.END, saida.strip() + "\n")
#                 log_text.see(ctk.END)
#                 log_text.configure(state="disabled")
#         processo.wait()
#         if processo.returncode != 0:
#             erros = processo.stderr.read().strip()
#             log_text.configure(state="normal")
#             log_text.insert(ctk.END, f"ERRO: {erros}\n")
#             log_text.see(ctk.END)
#             log_text.configure(state="disabled")
#             return False
#         return True
#     except Exception as e:
#         log_text.configure(state="normal")
#         log_text.insert(ctk.END, f"Erro ao executar comando: {e}\n")
#         log_text.see(ctk.END)
#         log_text.configure(state="disabled")
#         return False

# # Função para seleção de diretório do projeto

# def selecionar_diretorio_projeto(diretorio_entry, branch_combo, start_button):
#     diretorio = filedialog.askdirectory(title="Selecione a pasta do projeto")
#     if diretorio:
#         diretorio_entry.delete(0, ctk.END)
#         diretorio_entry.insert(0, diretorio)
#         os.chdir(diretorio)
#         atualizar_branches(diretorio, branch_combo)
#         start_button.configure(state="normal")

# # Função para atualizar lista de branches

# def atualizar_branches(diretorio, branch_combo):
#     try:
#         resultado = subprocess.run(["git", "branch", "-r"], capture_output=True, text=True, cwd=diretorio)
#         branches = [line.split('/')[-1].strip() for line in resultado.stdout.splitlines() if "->" not in line]
#         branch_combo.configure(values=branches)
#         if branches:
#             branch_combo.set(branches[0])
#     except Exception as e:
#         messagebox.showerror("Erro", f"Erro ao atualizar branches: {e}")

# # Configuração da Janela Principal
# ctk.set_appearance_mode("dark")
# app = ctk.CTk()
# app.title("Compilador de Projetos")
# app.geometry("1100x1000")

# # Cabeçalho
# title = ctk.CTkLabel(app, text="Gerenciador de Branches e Projeto", font=ctk.CTkFont(size=28, weight="bold"))
# title.pack(pady=20)

# # Projeto (Diretório)
# project_frame = ctk.CTkFrame(app, width=1000)
# project_frame.pack(fill="x", padx=20, pady=10)

# ctk.CTkLabel(project_frame, text="📁 Selecione a pasta do projeto:", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=10, pady=5)

# project_select_frame = ctk.CTkFrame(project_frame)
# project_select_frame.pack(fill="x", pady=10)

# diretorio_entry = ctk.CTkEntry(project_select_frame)
# diretorio_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

# diretorio_button = ctk.CTkButton(project_select_frame, text="Selecionar", command=lambda: selecionar_diretorio_projeto(diretorio_entry, branch_combo, start_button))
# diretorio_button.pack(side="right")

# # Branch e Banco
# branch_frame = ctk.CTkFrame(app, width=1000)
# branch_frame.pack(fill="x", padx=20, pady=10)

# ctk.CTkLabel(branch_frame, text="🌿 Branch e Banco:", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=10, pady=5)

# branch_combo = ctk.CTkComboBox(branch_frame, width=500)
# branch_combo.pack(fill="x", padx=10, pady=(5, 10))

# banco_combo = ctk.CTkComboBox(branch_frame, width=500, values=["Waybe-working", "Waybe-RC", "Waybe-master", "Micro-Waychef", "Sessao"])
# banco_combo.pack(fill="x", padx=10, pady=(5, 10))

# origem_combo = ctk.CTkComboBox(branch_frame, width=500, values=["Meu Banco", "MeuAmbienteLinux", "ANOTAAI", "Docker", "RASP"])
# origem_combo.pack(fill="x", padx=10, pady=(5, 10))

# # Execução e Logs
# execution_frame = ctk.CTkFrame(app, width=1000)
# execution_frame.pack(fill="both", expand=True, padx=20, pady=10)

# ctk.CTkLabel(execution_frame, text="🔧 Execução e Logs:", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=10, pady=5)

# log_box = ctk.CTkTextbox(execution_frame, height=300, state="disabled")
# log_box.pack(fill="both", expand=True, padx=10, pady=10)

# # Botões de Controle
# btn_frame = ctk.CTkFrame(app)
# btn_frame.pack(pady=10, padx=20)

# start_button = ctk.CTkButton(btn_frame, text="Iniciar Processo", state="disabled", width=200)
# start_button.pack(side="left", padx=5)

# clear_button = ctk.CTkButton(btn_frame, text="Limpar Log", command=lambda: log_box.configure(state="normal") or log_box.delete(1.0, ctk.END) or log_box.configure(state="disabled"))
# clear_button.pack(side="right", padx=5)

# app.mainloop()
