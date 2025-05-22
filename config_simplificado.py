import os
import dotenv
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from typing import Dict, Tuple, List

# Caminho do arquivo .env
ENV_PATH = ".env"

def load_env_config():
    """Carrega todas as configurações do arquivo .env"""
    if os.path.exists(ENV_PATH):
        dotenv.load_dotenv(ENV_PATH, override=True)
    
    # Configuração automática das variáveis de ambiente JAVA/MAVEN se existirem no .env
    java_home = os.getenv('JAVA_HOME')
    maven_home = os.getenv('MAVEN_HOME')
    maven_opts = os.getenv('MAVEN_OPTS', '-Xmx1024m')
    
    if java_home:
        os.environ['JAVA_HOME'] = java_home
        os.environ['PATH'] = f"{java_home}\\bin;{os.environ['PATH']}"
    if maven_home:
        os.environ['M2'] = maven_home
        os.environ['PATH'] = f"{maven_home}\\bin;{os.environ['PATH']}"
    if maven_opts:
        os.environ['MAVEN_OPTS'] = maven_opts

def get_db_origins() -> Dict[str, Tuple[str, str, str, str]]:
    """Obtém todas as origens de banco de dados do arquivo .env"""
    origins = {}
    
    # Carrega o arquivo .env novamente para garantir que temos os dados mais recentes
    if os.path.exists(ENV_PATH):
        dotenv.load_dotenv(ENV_PATH, override=True)
    
    # Procura por padrões DB_X_IP, DB_X_PORTA, DB_X_USER, DB_X_PASS
    for key in os.environ:
        if key.startswith('DB_') and key.endswith('_IP'):
            db_id = key.split('_')[1]
            ip = os.getenv(f'DB_{db_id}_IP', '')
            porta = os.getenv(f'DB_{db_id}_PORTA', '3306')
            usuario = os.getenv(f'DB_{db_id}_USER', 'root')
            senha = os.getenv(f'DB_{db_id}_PASS', 'root')
            
            # Adiciona ao dicionário de origens
            origins[db_id] = (ip, porta, usuario, senha)
    
    # Se não encontrou nenhuma origem no .env, cria uma origem padrão
    if not origins:
        # Adiciona uma origem padrão ao arquivo .env
        with open(ENV_PATH, "a") as f:
            f.write("DB_1_IP=127.0.0.1\n")
            f.write("DB_1_PORTA=3306\n")
            f.write("DB_1_USER=root\n")
            f.write("DB_1_PASS=root\n")
            f.write("DB_1_NOME=Banco Local\n")
        
        # Recarrega o arquivo .env
        dotenv.load_dotenv(ENV_PATH, override=True)
        
        # Adiciona a origem padrão ao dicionário
        origins["1"] = ("127.0.0.1", "3306", "root", "root")
    
    return origins

def get_db_names() -> Dict[str, str]:
    """Obtém todos os nomes de bancos de dados do arquivo .env"""
    db_names = {}
    
    # Carrega o arquivo .env novamente para garantir que temos os dados mais recentes
    if os.path.exists(ENV_PATH):
        dotenv.load_dotenv(ENV_PATH, override=True)
    
    # Procura por padrões BANCO_X
    for key in os.environ:
        if key.startswith('BANCO_') and '_' not in key[6:]:
            db_id = key.split('_')[1]
            db_name = os.getenv(key, '')
            
            # Adiciona ao dicionário de bancos
            if db_name:
                db_names[db_id] = db_name
    
    # Se não encontrou nenhum banco no .env, cria um banco padrão
    if not db_names:
        # Adiciona um banco padrão ao arquivo .env
        with open(ENV_PATH, "a") as f:
            f.write("BANCO_1=waybe\n")
            f.write("BANCO_1_NOME=Waybe\n")
        
        # Recarrega o arquivo .env
        dotenv.load_dotenv(ENV_PATH, override=True)
        
        # Adiciona o banco padrão ao dicionário
        db_names["1"] = "waybe"
    
    return db_names

def get_origin_display_names() -> Dict[str, str]:
    """Obtém nomes de exibição para as origens de banco de dados"""
    origins = get_db_origins()
    display_names = {}
    
    # Carrega o arquivo .env novamente para garantir que temos os dados mais recentes
    if os.path.exists(ENV_PATH):
        dotenv.load_dotenv(ENV_PATH, override=True)
    
    for db_id, (ip, porta, _, _) in origins.items():
        # Verifica se existe um nome amigável definido no .env
        nome_amigavel = os.getenv(f'DB_{db_id}_NOME', '')
        
        if nome_amigavel:
            display_names[db_id] = nome_amigavel
        else:
            # Se não tiver nome amigável, usa o IP e porta
            display_names[db_id] = f"Banco {ip}:{porta}"
            
            # Adiciona o nome amigável ao arquivo .env
            with open(ENV_PATH, "a") as f:
                f.write(f"DB_{db_id}_NOME=Banco {ip}:{porta}\n")
            
            # Recarrega o arquivo .env
            dotenv.load_dotenv(ENV_PATH, override=True)
    
    return display_names

def get_db_display_names() -> Dict[str, str]:
    """Obtém nomes de exibição para os bancos de dados"""
    db_names = get_db_names()
    display_names = {}
    
    # Carrega o arquivo .env novamente para garantir que temos os dados mais recentes
    if os.path.exists(ENV_PATH):
        dotenv.load_dotenv(ENV_PATH, override=True)
    
    for db_id, name in db_names.items():
        # Verifica se existe um nome amigável definido no .env
        nome_amigavel = os.getenv(f'BANCO_{db_id}_NOME', '')
        
        if nome_amigavel:
            display_names[db_id] = nome_amigavel
        else:
            # Se não tiver nome amigável, usa o nome do banco com primeira letra maiúscula
            display_names[db_id] = name.capitalize()
            
            # Adiciona o nome amigável ao arquivo .env
            with open(ENV_PATH, "a") as f:
                f.write(f"BANCO_{db_id}_NOME={name.capitalize()}\n")
            
            # Recarrega o arquivo .env
            dotenv.load_dotenv(ENV_PATH, override=True)
    
    return display_names

def get_origin_combo_values() -> List[str]:
    """Retorna lista formatada de origens para o ComboBox"""
    origins = get_origin_display_names()
    return [f"{id}. {name}" for id, name in origins.items()]

def get_db_combo_values() -> List[str]:
    """Retorna lista formatada de bancos para o ComboBox"""
    db_names = get_db_display_names()
    return [f"{id}. {name}" for id, name in db_names.items()]
        
def get_next_id(prefix, env_path=".env"):
    """Obtém o próximo ID disponível para um determinado prefixo no arquivo .env"""
    if not os.path.exists(env_path):
        return "1"
        
    with open(env_path, "r") as f:
        content = f.read()
    
    # Procura por padrões como DB_1, DB_2, BANCO_1, BANCO_2, etc.
    pattern = rf"{prefix}_(\d+)"
    matches = re.findall(pattern, content)
    
    if not matches:
        return "1"
    
    # Converte para inteiros e encontra o maior
    ids = [int(id_str) for id_str in matches]
    return str(max(ids) + 1)

class ConfigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuração do Sistema")
        self.root.geometry("600x700")
        
        # Criar notebook (abas)
        self.notebook = ctk.CTkTabview(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Criar abas
        self.tab_java_maven = self.notebook.add("Java/Maven")
        self.tab_origem = self.notebook.add("Origem do Banco")
        self.tab_banco = self.notebook.add("Nome do Banco")
        
        # Configurar cada aba
        self.setup_java_maven_tab()
        self.setup_origem_tab()
        self.setup_banco_tab()
    
    def setup_java_maven_tab(self):
        # Título
        ctk.CTkLabel(self.tab_java_maven, text="Configuração JAVA E MAVEN", font=("Arial", 16, "bold"), anchor="w").pack(anchor="w", padx=10, pady=5)
        
        # Frame para JAVA_HOME
        java_frame = ctk.CTkFrame(self.tab_java_maven)
        java_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(java_frame, text="JAVA_HOME:", width=100).pack(side="left", padx=5)
        
        self.entry_java = ctk.CTkEntry(java_frame, width=300)
        self.entry_java.insert(0, os.getenv("JAVA_HOME", ""))
        self.entry_java.pack(side="left", padx=5, fill="x", expand=True)
        
        def procurar_java_home():
            diretorio = filedialog.askdirectory(title="Selecione o diretório JAVA_HOME")
            if diretorio:
                self.entry_java.delete(0, ctk.END)
                self.entry_java.insert(0, diretorio)
        
        btn_procurar_java = ctk.CTkButton(java_frame, text="Procurar", width=80, command=procurar_java_home)
        btn_procurar_java.pack(side="right", padx=5)
        
        # Frame para MAVEN_HOME
        maven_frame = ctk.CTkFrame(self.tab_java_maven)
        maven_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(maven_frame, text="MAVEN_HOME:", width=100).pack(side="left", padx=5)
        
        self.entry_maven = ctk.CTkEntry(maven_frame, width=300)
        self.entry_maven.insert(0, os.getenv("MAVEN_HOME", ""))
        self.entry_maven.pack(side="left", padx=5, fill="x", expand=True)
        
        def procurar_maven_home():
            diretorio = filedialog.askdirectory(title="Selecione o diretório MAVEN_HOME")
            if diretorio:
                self.entry_maven.delete(0, ctk.END)
                self.entry_maven.insert(0, diretorio)
        
        btn_procurar_maven = ctk.CTkButton(maven_frame, text="Procurar", width=80, command=procurar_maven_home)
        btn_procurar_maven.pack(side="right", padx=5)
        
        # Botão para salvar
        def salvar_java_maven():
            # Atualiza o arquivo .env com os novos valores
            java_home = self.entry_java.get()
            maven_home = self.entry_maven.get()
            
            # Lê o conteúdo atual do arquivo .env
            env_content = ""
            if os.path.exists(ENV_PATH):
                with open(ENV_PATH, "r") as f:
                    env_content = f.read()
            
            # Remove as linhas existentes de JAVA_HOME e MAVEN_HOME
            env_lines = env_content.splitlines()
            env_lines = [line for line in env_lines if not line.startswith("JAVA_HOME=") and not line.startswith("MAVEN_HOME=")]
            
            # Adiciona as novas linhas
            env_lines.append(f"JAVA_HOME={java_home}")
            env_lines.append(f"MAVEN_HOME={maven_home}")
            
            # Escreve de volta no arquivo .env
            with open(ENV_PATH, "w") as f:
                f.write("\n".join(env_lines))
            
            # Recarrega as variáveis de ambiente
            load_env_config()
            
            messagebox.showinfo("Salvo", "Configurações de JAVA e MAVEN salvas com sucesso.")
        
        btn_salvar = ctk.CTkButton(self.tab_java_maven, text="Salvar Configurações", command=salvar_java_maven)
        btn_salvar.pack(pady=10)
    
    def setup_origem_tab(self):
        # Título
        ctk.CTkLabel(self.tab_origem, text="Configuração de Origem do banco", font=("Arial", 16, "bold"), anchor="w").pack(anchor="w", padx=10, pady=5)
        
        # Frame para lista de origens
        self.origens_listbox_frame = ctk.CTkFrame(self.tab_origem)
        self.origens_listbox_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(self.origens_listbox_frame, text="Origens cadastradas:", anchor="w").pack(anchor="w", padx=5, pady=5)
        
        # Listbox para origens
        self.origens_listbox = tk.Listbox(self.origens_listbox_frame, bg="#2b2b2b", fg="white", font=("Arial", 12), height=10)
        self.origens_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Atualiza a lista de origens
        self.atualizar_lista_origens()
        
        # Frame para nova origem
        nova_origem_frame = ctk.CTkFrame(self.tab_origem)
        nova_origem_frame.pack(fill="x", padx=10, pady=5)
        
        # Campos para nova origem
        ctk.CTkLabel(nova_origem_frame, text="Nova Origem:", anchor="w").pack(anchor="w", padx=5, pady=5)
        
        # IP
        ip_frame = ctk.CTkFrame(nova_origem_frame)
        ip_frame.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(ip_frame, text="IP:", width=80).pack(side="left", padx=5)
        self.entry_ip = ctk.CTkEntry(ip_frame)
        self.entry_ip.pack(side="left", fill="x", expand=True, padx=5)
        
        # Porta
        porta_frame = ctk.CTkFrame(nova_origem_frame)
        porta_frame.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(porta_frame, text="Porta:", width=80).pack(side="left", padx=5)
        self.entry_porta = ctk.CTkEntry(porta_frame)
        self.entry_porta.insert(0, "3306")
        self.entry_porta.pack(side="left", fill="x", expand=True, padx=5)
        
        # Usuário
        usuario_frame = ctk.CTkFrame(nova_origem_frame)
        usuario_frame.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(usuario_frame, text="Usuário:", width=80).pack(side="left", padx=5)
        self.entry_usuario = ctk.CTkEntry(usuario_frame)
        self.entry_usuario.insert(0, "root")
        self.entry_usuario.pack(side="left", fill="x", expand=True, padx=5)
        
        # Senha
        senha_frame = ctk.CTkFrame(nova_origem_frame)
        senha_frame.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(senha_frame, text="Senha:", width=80).pack(side="left", padx=5)
        self.entry_senha = ctk.CTkEntry(senha_frame, show="*")
        self.entry_senha.insert(0, "root")
        self.entry_senha.pack(side="left", fill="x", expand=True, padx=5)
        
        # Nome amigável
        nome_frame = ctk.CTkFrame(nova_origem_frame)
        nome_frame.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(nome_frame, text="Nome:", width=80).pack(side="left", padx=5)
        self.entry_nome_origem = ctk.CTkEntry(nome_frame)
        self.entry_nome_origem.pack(side="left", fill="x", expand=True, padx=5)
        
        # Botão para adicionar
        def adicionar_origem():
            # Gera ID automaticamente
            next_id = get_next_id("DB")
            prefix = f"DB_{next_id}"
            
            # Verifica se os campos obrigatórios estão preenchidos
            if not self.entry_ip.get():
                messagebox.showerror("Erro", "O campo IP é obrigatório.")
                return
            
            # Obtém os valores dos campos
            ip = self.entry_ip.get()
            porta = self.entry_porta.get() or '3306'
            usuario = self.entry_usuario.get() or 'root'
            senha = self.entry_senha.get() or 'root'
            
            # Cria um nome amigável para a origem
            nome_amigavel = self.entry_nome_origem.get() or f"Banco {ip}:{porta}"
            
            # Adiciona ao arquivo .env
            with open(ENV_PATH, "a") as f:
                f.write(f"{prefix}_IP={ip}\n")
                f.write(f"{prefix}_PORTA={porta}\n")
                f.write(f"{prefix}_USER={usuario}\n")
                f.write(f"{prefix}_PASS={senha}\n")
                f.write(f"{prefix}_NOME={nome_amigavel}\n")
            
            # Recarrega as variáveis de ambiente
            load_env_config()
            
            messagebox.showinfo("Salvo", f"Origem {nome_amigavel} cadastrada com sucesso.")
            
            # Limpa os campos após o cadastro
            self.entry_ip.delete(0, ctk.END)
            self.entry_porta.delete(0, ctk.END)
            self.entry_porta.insert(0, "3306")
            self.entry_usuario.delete(0, ctk.END)
            self.entry_usuario.insert(0, "root")
            self.entry_senha.delete(0, ctk.END)
            self.entry_senha.insert(0, "root")
            self.entry_nome_origem.delete(0, ctk.END)
            
            # Atualiza a lista de origens
            self.atualizar_lista_origens()
        
        btn_adicionar = ctk.CTkButton(nova_origem_frame, text="Adicionar Origem", command=adicionar_origem)
        btn_adicionar.pack(pady=10)
    
    def atualizar_lista_origens(self):
        # Limpa a lista atual
        self.origens_listbox.delete(0, tk.END)
        
        # Obtém as origens e nomes de exibição
        origens = get_db_origins()
        display_names = get_origin_display_names()
        
        # Adiciona cada origem à lista
        for db_id, (ip, porta, usuario, _) in origens.items():
            nome = display_names.get(db_id, f"Banco {ip}:{porta}")
            self.origens_listbox.insert(tk.END, f"{nome} ({ip}:{porta})")
    
    def setup_banco_tab(self):
        # Título
        ctk.CTkLabel(self.tab_banco, text="Cadastro de Nome de Banco", font=("Arial", 16, "bold"), anchor="w").pack(anchor="w", padx=10, pady=5)
        
        # Frame para lista de bancos
        self.bancos_listbox_frame = ctk.CTkFrame(self.tab_banco)
        self.bancos_listbox_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(self.bancos_listbox_frame, text="Bancos cadastrados:", anchor="w").pack(anchor="w", padx=5, pady=5)
        
        # Listbox para bancos
        self.bancos_listbox = tk.Listbox(self.bancos_listbox_frame, bg="#2b2b2b", fg="white", font=("Arial", 12), height=10)
        self.bancos_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Atualiza a lista de bancos
        self.atualizar_lista_bancos()
        
        # Frame para novo banco
        novo_banco_frame = ctk.CTkFrame(self.tab_banco)
        novo_banco_frame.pack(fill="x", padx=10, pady=5)
        
        # Campos para novo banco
        ctk.CTkLabel(novo_banco_frame, text="Novo Banco:", anchor="w").pack(anchor="w", padx=5, pady=5)
        
        # Nome do banco
        nome_banco_frame = ctk.CTkFrame(novo_banco_frame)
        nome_banco_frame.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(nome_banco_frame, text="Nome:", width=80).pack(side="left", padx=5)
        self.entry_nome_banco = ctk.CTkEntry(nome_banco_frame)
        self.entry_nome_banco.pack(side="left", fill="x", expand=True, padx=5)
        
        # Nome amigável
        nome_amigavel_frame = ctk.CTkFrame(novo_banco_frame)
        nome_amigavel_frame.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(nome_amigavel_frame, text="Exibição:", width=80).pack(side="left", padx=5)
        self.entry_nome_amigavel = ctk.CTkEntry(nome_amigavel_frame)
        self.entry_nome_amigavel.pack(side="left", fill="x", expand=True, padx=5)
        
        # Botão para adicionar
        def adicionar_banco():
            # Gera ID automaticamente
            next_id = get_next_id("BANCO")
            
            # Verifica se o campo está preenchido
            if not self.entry_nome_banco.get():
                messagebox.showerror("Erro", "O nome do banco é obrigatório.")
                return
            
            # Obtém o nome do banco
            nome_banco = self.entry_nome_banco.get()
            
            # Cria um nome amigável para o banco
            nome_amigavel = self.entry_nome_amigavel.get() or nome_banco.capitalize()
            
            # Adiciona ao arquivo .env
            with open(ENV_PATH, "a") as f:
                f.write(f"BANCO_{next_id}={nome_banco}\n")
                f.write(f"BANCO_{next_id}_NOME={nome_amigavel}\n")
            
            # Recarrega as variáveis de ambiente
            load_env_config()
            
            messagebox.showinfo("Salvo", f"Banco {nome_amigavel} cadastrado com sucesso.")
            
            # Limpa os campos após o cadastro
            self.entry_nome_banco.delete(0, ctk.END)
            self.entry_nome_amigavel.delete(0, ctk.END)
            
            # Atualiza a lista de bancos
            self.atualizar_lista_bancos()
        
        btn_adicionar = ctk.CTkButton(novo_banco_frame, text="Adicionar Banco", command=adicionar_banco)
        btn_adicionar.pack(pady=10)
    
    def atualizar_lista_bancos(self):
        # Limpa a lista atual
        self.bancos_listbox.delete(0, tk.END)
        
        # Obtém os bancos e nomes de exibição
        bancos = get_db_names()
        display_names = get_db_display_names()
        
        # Adiciona cada banco à lista
        for db_id, nome in bancos.items():
            display_name = display_names.get(db_id, nome.capitalize())
            self.bancos_listbox.insert(tk.END, f"{display_name} ({nome})")

if __name__ == "__main__":
    # Carrega as configurações do arquivo .env
    load_env_config()
    
    # UI Principal
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = ctk.CTk()
    
    # Inicializa a aplicação
    config_app = ConfigApp(app)
    
    # Inicia o loop principal
    app.mainloop()