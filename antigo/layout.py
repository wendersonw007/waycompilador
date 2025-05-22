# # import customtkinter as ctk
# # from dotenv import load_dotenv
# # import os

# # load_dotenv()

# # # Carregar configurações do .env
# # BANCO_CONFIG = {
# #     'nome': os.getenv('BANCO_PADRAO', 'Meu Banco'),
# #     'ip': os.getenv('BANCO_IP', '127.0.0.1'),
# #     'porta': os.getenv('BANCO_PORTA', '3306'),
# #     'usuario': os.getenv('BANCO_USUARIO', 'root'),
# #     'senha': os.getenv('BANCO_SENHA', 'root')
# # }

# # class BancoConfigFrame(ctk.CTkFrame):
# #     def __init__(self, master):
# #         super().__init__(master)
# #         self.pack(padx=20, pady=10, fill='x')

# #         ctk.CTkLabel(self, text="⚙ Configuração Banco (via .env)", font=("Arial", 16)).pack(pady=10)

# #         self.nome_entry = ctk.CTkEntry(self)
# #         self.nome_entry.insert(0, BANCO_CONFIG['nome'])
# #         self.nome_entry.pack(pady=5, fill='x')

# #         self.ip_entry = ctk.CTkEntry(self)
# #         self.ip_entry.insert(0, BANCO_CONFIG['ip'])
# #         self.ip_entry.pack(pady=5, fill='x')

# #         self.porta_entry = ctk.CTkEntry(self)
# #         self.porta_entry.insert(0, BANCO_CONFIG['porta'])
# #         self.porta_entry.pack(pady=5, fill='x')

# #         self.usuario_entry = ctk.CTkEntry(self)
# #         self.usuario_entry.insert(0, BANCO_CONFIG['usuario'])
# #         self.usuario_entry.pack(pady=5, fill='x')

# #         self.senha_entry = ctk.CTkEntry(self, show='*')
# #         self.senha_entry.insert(0, BANCO_CONFIG['senha'])
# #         self.senha_entry.pack(pady=5, fill='x')

# #         ctk.CTkButton(self, text="Salvar Configuração", command=self.salvar_env).pack(pady=10)

# #     def salvar_env(self):
# #         with open('.env', 'w') as env_file:
# #             env_file.write(f'BANCO_PADRAO={self.nome_entry.get()}\n')
# #             env_file.write(f'BANCO_IP={self.ip_entry.get()}\n')
# #             env_file.write(f'BANCO_PORTA={self.porta_entry.get()}\n')
# #             env_file.write(f'BANCO_USUARIO={self.usuario_entry.get()}\n')
# #             env_file.write(f'BANCO_SENHA={self.senha_entry.get()}\n')

# #         ctk.CTkMessagebox(title="Salvo", message="Configuração atualizada com sucesso!", icon="check")

# # # Configuração da Janela Principal
# # ctk.set_appearance_mode("dark")
# # app = ctk.CTk()
# # app.title("Aplicação com Configuração via .env")
# # app.geometry("600x400")

# # BancoConfigFrame(app)

# # app.mainloop()



# import customtkinter as ctk
# from dotenv import load_dotenv
# import os
# from tkinter import messagebox

# load_dotenv()

# # Carregar configurações do .env
# BANCO_CONFIG = {
#     'nome': os.getenv('BANCO_PADRAO', 'Meu Banco'),
#     'ip': os.getenv('BANCO_IP', '127.0.0.1'),
#     'porta': os.getenv('BANCO_PORTA', '3306'),
#     'usuario': os.getenv('BANCO_USUARIO', 'root'),
#     'senha': os.getenv('BANCO_SENHA', 'root')
# }

# class BancoConfigFrame(ctk.CTkFrame):
#     def __init__(self, master):
#         super().__init__(master)
#         self.pack(padx=20, pady=10, fill='x')

#         ctk.CTkLabel(self, text="⚙ Configuração Banco (via .env)", font=("Arial", 16)).pack(pady=10)

#         self.nome_entry = ctk.CTkEntry(self)
#         self.nome_entry.insert(0, BANCO_CONFIG['nome'])
#         self.nome_entry.pack(pady=5, fill='x')

#         self.ip_entry = ctk.CTkEntry(self)
#         self.ip_entry.insert(0, BANCO_CONFIG['ip'])
#         self.ip_entry.pack(pady=5, fill='x')

#         self.porta_entry = ctk.CTkEntry(self)
#         self.porta_entry.insert(0, BANCO_CONFIG['porta'])
#         self.porta_entry.pack(pady=5, fill='x')

#         self.usuario_entry = ctk.CTkEntry(self)
#         self.usuario_entry.insert(0, BANCO_CONFIG['usuario'])
#         self.usuario_entry.pack(pady=5, fill='x')

#         self.senha_entry = ctk.CTkEntry(self, show='*')
#         self.senha_entry.insert(0, BANCO_CONFIG['senha'])
#         self.senha_entry.pack(pady=5, fill='x')

#         self.crud_frame = ctk.CTkFrame(self)
#         self.crud_frame.pack(fill='x', pady=10)

#         ctk.CTkButton(self.crud_frame, text="Adicionar Configuração", command=self.adicionar_config).pack(side='left', padx=5)
#         ctk.CTkButton(self.crud_frame, text="Salvar Configuração", command=self.salvar_env).pack(side='left', padx=5)
#         ctk.CTkButton(self.crud_frame, text="Excluir Configuração", command=self.excluir_config).pack(side='left', padx=5)

#     def salvar_env(self):
#         with open('.env', 'w') as env_file:
#             env_file.write(f'BANCO_PADRAO={self.nome_entry.get()}\n')
#             env_file.write(f'BANCO_IP={self.ip_entry.get()}\n')
#             env_file.write(f'BANCO_PORTA={self.porta_entry.get()}\n')
#             env_file.write(f'BANCO_USUARIO={self.usuario_entry.get()}\n')
#             env_file.write(f'BANCO_SENHA={self.senha_entry.get()}\n')

#         messagebox.showinfo("Salvo", "Configuração atualizada com sucesso!")

#     def adicionar_config(self):
#         nova_config = ctk.CTkToplevel(self)
#         nova_config.title("Adicionar Nova Configuração")
#         nova_config.geometry("400x300")

#         ctk.CTkLabel(nova_config, text="Nome da Configuração:").pack(pady=10)
#         nome_entry = ctk.CTkEntry(nova_config)
#         nome_entry.pack(pady=5, fill='x')

#         ctk.CTkLabel(nova_config, text="IP:").pack(pady=5)
#         ip_entry = ctk.CTkEntry(nova_config)
#         ip_entry.pack(pady=5, fill='x')

#         ctk.CTkLabel(nova_config, text="Porta:").pack(pady=5)
#         porta_entry = ctk.CTkEntry(nova_config)
#         porta_entry.pack(pady=5, fill='x')

#         ctk.CTkLabel(nova_config, text="Usuário:").pack(pady=5)
#         usuario_entry = ctk.CTkEntry(nova_config)
#         usuario_entry.pack(pady=5, fill='x')

#         ctk.CTkLabel(nova_config, text="Senha:").pack(pady=5)
#         senha_entry = ctk.CTkEntry(nova_config, show='*')
#         senha_entry.pack(pady=5, fill='x')

#         def salvar_nova_config():
#             config_name = nome_entry.get().upper()
#             if not config_name or config_name in os.environ:
#                 messagebox.showerror("Erro", "Nome da configuração já existe ou está vazio!")
#                 return
#             with open('.env', 'a') as env_file:
#                 env_file.write(f'BANCO_{config_name}_IP={ip_entry.get()}\n')
#                 env_file.write(f'BANCO_{config_name}_PORTA={porta_entry.get()}\n')
#                 env_file.write(f'BANCO_{config_name}_USUARIO={usuario_entry.get()}\n')
#                 env_file.write(f'BANCO_{config_name}_SENHA={senha_entry.get()}\n')
#             nova_config.destroy()
#             messagebox.showinfo("Salvo", "Nova configuração adicionada com sucesso!")

#         ctk.CTkButton(nova_config, text="Salvar", command=salvar_nova_config).pack(pady=20)

#     def excluir_config(self):
#         confirm = messagebox.askyesno("Excluir Configuração", "Tem certeza que deseja excluir essa configuração?")
#         if confirm:
#             with open('.env', 'w') as env_file:
#                 env_file.write('')
#             messagebox.showinfo("Excluído", "Configuração excluída com sucesso!")

# # Configuração da Janela Principal
# ctk.set_appearance_mode("dark")
# app = ctk.CTk()
# app.title("Aplicação com Configuração via .env")
# app.geometry("600x500")

# BancoConfigFrame(app)

# app.mainloop()