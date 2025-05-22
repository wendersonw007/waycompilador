# # import os
# # from pathlib import Path
# # from dotenv import load_dotenv
# # from typing import Dict, Tuple

# # class Config:
# #     def __init__(self):
# #         # Carrega as variáveis do arquivo .env
# #         load_dotenv()
        
# #         # Configurações de Java e Maven
# #         self.java_home = os.getenv('JAVA_HOME', '')
# #         self.maven_home = os.getenv('MAVEN_HOME', '')
# #         self.maven_opts = os.getenv('MAVEN_OPTS', '-Xmx1024m')
        
# #         # Configurações de banco de dados
# #         self.databases = self._load_databases()
    
# #     def _load_databases(self) -> Dict[str, Tuple[str, str, str, str, str]]:
# #         """Carrega as configurações de banco de dados do .env"""
# #         databases = {}
# #         i = 1
# #         while True:
# #             db_config = os.getenv(f'DB_{i}')
# #             if not db_config:
# #                 break
# #             ip, porta, usuario, senha, nome_banco = db_config.split(',')
# #             databases[str(i)] = (ip, porta, usuario, senha, nome_banco)
# #             i += 1
# #         return databases
    
# #     def setup_environment(self):
# #         """Configura as variáveis de ambiente necessárias"""
# #         if self.java_home:
# #             os.environ['JAVA_HOME'] = self.java_home
# #             os.environ['PATH'] = f"{self.java_home}\\bin;{os.environ['PATH']}"
        
# #         if self.maven_home:
# #             os.environ['M2'] = self.maven_home
# #             os.environ['PATH'] = f"{self.maven_home}\\bin;{os.environ['PATH']}"
        
# #         if self.maven_opts:
# #             os.environ['MAVEN_OPTS'] = self.maven_opts

# # # Instância global de configuração
# # config = Config()

# import os
# import dotenv
# import customtkinter as ctk
# from tkinter import messagebox

# # Caminho do arquivo .env
# ENV_PATH = ".env"

# # Carrega variáveis do .env
# if os.path.exists(ENV_PATH):
#     dotenv.load_dotenv(ENV_PATH)

# # UI Principal
# ctk.set_appearance_mode("dark")
# ctk.set_default_color_theme("blue")
# app = ctk.CTk()
# app.title("Configurador Maven e Banco de Dados")
# app.geometry("800x600")

# # === Frame JAVA/MAVEN ===
# frame_java = ctk.CTkFrame(app)
# frame_java.pack(pady=10, fill="x", padx=20)
# ctk.CTkLabel(frame_java, text="Configuração Java e Maven", font=("Arial", 18, "bold")).pack(anchor="w", padx=10, pady=5)

# entry_java = ctk.CTkEntry(frame_java, placeholder_text="JAVA_HOME", width=600)
# entry_java.insert(0, os.getenv("JAVA_HOME", ""))
# entry_java.pack(padx=10, pady=5)

# entry_maven = ctk.CTkEntry(frame_java, placeholder_text="MAVEN_HOME", width=600)
# entry_maven.insert(0, os.getenv("MAVEN_HOME", ""))
# entry_maven.pack(padx=10, pady=5)

# # === Frame para adicionar nova origem de banco ===
# frame_origem = ctk.CTkFrame(app)
# frame_origem.pack(pady=10, fill="x", padx=20)
# ctk.CTkLabel(frame_origem, text="Cadastro de Origem do Banco", font=("Arial", 18, "bold")).pack(anchor="w", padx=10, pady=5)

# entry_origem_id = ctk.CTkEntry(frame_origem, placeholder_text="ID")
# entry_ip = ctk.CTkEntry(frame_origem, placeholder_text="IP")
# entry_porta = ctk.CTkEntry(frame_origem, placeholder_text="Porta")
# entry_usuario = ctk.CTkEntry(frame_origem, placeholder_text="Usuário")
# entry_senha = ctk.CTkEntry(frame_origem, placeholder_text="Senha")

# for entry in [entry_origem_id, entry_ip, entry_porta, entry_usuario, entry_senha]:
#     entry.pack(padx=10, pady=2)

# def adicionar_origem():
#     prefix = f"DB_{entry_origem_id.get()}"
#     with open(ENV_PATH, "a") as f:
#         f.write(f"{prefix}_IP={entry_ip.get()}\n")
#         f.write(f"{prefix}_PORTA={entry_porta.get()}\n")
#         f.write(f"{prefix}_USER={entry_usuario.get()}\n")
#         f.write(f"{prefix}_PASS={entry_senha.get()}\n")
#     messagebox.showinfo("Salvo", f"Origem {entry_origem_id.get()} cadastrada.")

# btn_add_origem = ctk.CTkButton(frame_origem, text="Cadastrar Origem", command=adicionar_origem)
# btn_add_origem.pack(padx=10, pady=5)

# # === Frame para adicionar nome de banco ===
# frame_banco = ctk.CTkFrame(app)
# frame_banco.pack(pady=10, fill="x", padx=20)
# ctk.CTkLabel(frame_banco, text="Cadastro de Nome de Banco", font=("Arial", 18, "bold")).pack(anchor="w", padx=10, pady=5)

# entry_banco_id = ctk.CTkEntry(frame_banco, placeholder_text="ID do Banco")
# entry_banco_nome = ctk.CTkEntry(frame_banco, placeholder_text="Nome do Banco")
# entry_banco_id.pack(padx=10, pady=2)
# entry_banco_nome.pack(padx=10, pady=2)

# def adicionar_banco():
#     with open(ENV_PATH, "a") as f:
#         f.write(f"BANCO_{entry_banco_id.get()}={entry_banco_nome.get()}\n")
#     messagebox.showinfo("Salvo", f"Banco {entry_banco_id.get()} cadastrado.")

# btn_add_banco = ctk.CTkButton(frame_banco, text="Cadastrar Banco", command=adicionar_banco)
# btn_add_banco.pack(padx=10, pady=5)

# # === Botão para salvar JAVA/MAVEN ===
# def salvar_java_maven():
#     with open(ENV_PATH, "a") as f:
#         f.write(f"JAVA_HOME={entry_java.get()}\n")
#         f.write(f"MAVEN_HOME={entry_maven.get()}\n")
#     messagebox.showinfo("Salvo", "Caminhos JAVA_HOME e MAVEN_HOME salvos no .env")

# btn_salvar_geral = ctk.CTkButton(app, text="Salvar JAVA/MAVEN", command=salvar_java_maven)
# btn_salvar_geral.pack(pady=10)

# app.mainloop()
