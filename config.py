import os
import dotenv
import re
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
    
    # Se não encontrou nenhuma origem no .env, usa valores padrão
    if not origins:
        origins = {
            "1": ("127.0.0.1", "3306", "root", "root"),
            "2": ("192.168.5.174", "3306", "root", "root"),
            "3": ("192.168.5.217", "3306", "root", "root"),
            "4": ("127.0.0.1", "3309", "root", "root"),
            "5": ("rasp.local", "3306", "root", "root")
        }
    
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
    
    # Se não encontrou nenhum banco no .env, usa valores padrão
    if not db_names:
        db_names = {
            "1": "waybe",
            "2": "waybe",
            "3": "waybe",
            "4": "micro-waychef",
            "5": "waybe"
        }
    
    return db_names

def get_origin_display_names() -> Dict[str, str]:
    """Obtém nomes de exibição para as origens de banco de dados"""
    origins = get_db_origins()
    display_names = {}
    
    # Nomes amigáveis para as origens padrão
    default_names = {
        "127.0.0.1:3306": "Meu Banco",
        "192.168.5.174:3306": "MeuAmbienteLinux",
        "192.168.5.217:3306": "ANOTAAI",
        "127.0.0.1:3309": "Docker",
        "rasp.local:3306": "RASP"
    }
    
    for db_id, (ip, porta, _, _) in origins.items():
        key = f"{ip}:{porta}"
        if key in default_names:
            display_names[db_id] = default_names[key]
        else:
            display_names[db_id] = f"Banco {ip}:{porta}"
    
    return display_names

def get_db_display_names() -> Dict[str, str]:
    """Obtém nomes de exibição para os bancos de dados"""
    db_names = get_db_names()
    display_names = {}
    
    # Nomes amigáveis para os bancos padrão
    default_names = {
        "waybe": "Waybe",
        "micro-waychef": "Micro-Waychef"
    }
    
    for db_id, name in db_names.items():
        if name.lower() in default_names:
            display_names[db_id] = default_names[name.lower()]
        else:
            display_names[db_id] = name
    
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

# A interface gráfica de configuração só deve rodar se este arquivo for executado diretamente
if __name__ == "__main__":
    import customtkinter as ctk
    from tkinter import messagebox, filedialog

    # Carrega variáveis do .env
    load_env_config()

    # UI Principal
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = ctk.CTk()
    app.title("Configurador Maven e Banco de Dados")
    app.geometry("800x600")

    # === Frame JAVA/MAVEN ===
    frame_java = ctk.CTkFrame(app)
    frame_java.pack(pady=10, fill="x", padx=20)
    ctk.CTkLabel(frame_java, text="Configuração JAVA E MAVEN", font=("Arial", 18, "bold"), anchor="w").pack(anchor="w", padx=10, pady=5)

    # Frame para JAVA_HOME com botão de procurar
    java_frame = ctk.CTkFrame(frame_java)
    java_frame.pack(fill="x", padx=10, pady=5)
    
    entry_java = ctk.CTkEntry(java_frame, placeholder_text="JAVA_HOME", width=500)
    entry_java.insert(0, os.getenv("JAVA_HOME", ""))
    entry_java.pack(side="left", padx=(0, 10), fill="x", expand=True)
    
    def procurar_java_home():
        diretorio = filedialog.askdirectory(title="Selecione o diretório JAVA_HOME")
        if diretorio:
            entry_java.delete(0, ctk.END)
            entry_java.insert(0, diretorio)
    
    btn_procurar_java = ctk.CTkButton(java_frame, text="Procurar", command=procurar_java_home)
    btn_procurar_java.pack(side="right")

    # Frame para MAVEN_HOME com botão de procurar
    maven_frame = ctk.CTkFrame(frame_java)
    maven_frame.pack(fill="x", padx=10, pady=5)
    
    entry_maven = ctk.CTkEntry(maven_frame, placeholder_text="MAVEN_HOME", width=500)
    entry_maven.insert(0, os.getenv("MAVEN_HOME", ""))
    entry_maven.pack(side="left", padx=(0, 10), fill="x", expand=True)
    
    def procurar_maven_home():
        diretorio = filedialog.askdirectory(title="Selecione o diretório MAVEN_HOME")
        if diretorio:
            entry_maven.delete(0, ctk.END)
            entry_maven.insert(0, diretorio)
    
    btn_procurar_maven = ctk.CTkButton(maven_frame, text="Procurar", command=procurar_maven_home)
    btn_procurar_maven.pack(side="right")

    # === Frame para adicionar nova origem de banco ===
    frame_origem = ctk.CTkFrame(app)
    frame_origem.pack(pady=10, fill="x", padx=20)
    ctk.CTkLabel(frame_origem, text="Configuração de Origem do banco", font=("Arial", 18, "bold"), anchor="w").pack(anchor="w", padx=10, pady=5)

    # Exibe as origens existentes
    origens_frame = ctk.CTkFrame(frame_origem)
    origens_frame.pack(fill="x", padx=10, pady=5)
    
    origens = get_db_origins()
    display_names = get_origin_display_names()
    
    if origens:
        ctk.CTkLabel(origens_frame, text="Origens cadastradas:").pack(anchor="w", padx=5, pady=5)
        for db_id, (ip, porta, usuario, _) in origens.items():
            nome = display_names.get(db_id, f"Banco {ip}:{porta}")
            ctk.CTkLabel(origens_frame, text=f"ID: {db_id} - {nome} ({ip}:{porta}, usuário: {usuario})").pack(anchor="w", padx=20, pady=2)
    
    # Campos para nova origem
    entry_ip = ctk.CTkEntry(frame_origem, placeholder_text="IP")
    entry_porta = ctk.CTkEntry(frame_origem, placeholder_text="Porta")
    entry_usuario = ctk.CTkEntry(frame_origem, placeholder_text="Usuário")
    entry_senha = ctk.CTkEntry(frame_origem, placeholder_text="Senha", show="*")

    for entry in [entry_ip, entry_porta, entry_usuario, entry_senha]:
        entry.pack(padx=10, pady=2)

    def adicionar_origem():
        # Gera ID automaticamente
        next_id = get_next_id("DB")
        prefix = f"DB_{next_id}"
        
        # Verifica se os campos obrigatórios estão preenchidos
        if not entry_ip.get():
            messagebox.showerror("Erro", "O campo IP é obrigatório.")
            return
        
        # Adiciona ao arquivo .env
        with open(ENV_PATH, "a") as f:
            f.write(f"{prefix}_IP={entry_ip.get()}\n")
            f.write(f"{prefix}_PORTA={entry_porta.get() or '3306'}\n")
            f.write(f"{prefix}_USER={entry_usuario.get() or 'root'}\n")
            f.write(f"{prefix}_PASS={entry_senha.get() or 'root'}\n")
        
        # Recarrega as variáveis de ambiente
        load_env_config()
        
        messagebox.showinfo("Salvo", f"Origem {next_id} cadastrada com sucesso.")
        
        # Limpa os campos após o cadastro
        for entry in [entry_ip, entry_porta, entry_usuario, entry_senha]:
            entry.delete(0, ctk.END)
            
        # Reinicia a aplicação para atualizar a lista de origens
        app.destroy()
        os.system(f"python {__file__}")

    btn_add_origem = ctk.CTkButton(frame_origem, text="Cadastrar Origem", command=adicionar_origem)
    btn_add_origem.pack(padx=10, pady=5)

    # === Frame para adicionar nome de banco ===
    frame_banco = ctk.CTkFrame(app)
    frame_banco.pack(pady=10, fill="x", padx=20)
    ctk.CTkLabel(frame_banco, text="Cadastro de Nome de Banco", font=("Arial", 18, "bold"), anchor="w").pack(anchor="w", padx=10, pady=5)

    # Exibe os bancos existentes
    bancos_frame = ctk.CTkFrame(frame_banco)
    bancos_frame.pack(fill="x", padx=10, pady=5)
    
    bancos = get_db_names()
    display_names = get_db_display_names()
    
    if bancos:
        ctk.CTkLabel(bancos_frame, text="Bancos cadastrados:").pack(anchor="w", padx=5, pady=5)
        for db_id, nome in bancos.items():
            display_name = display_names.get(db_id, nome)
            ctk.CTkLabel(bancos_frame, text=f"ID: {db_id} - {display_name}").pack(anchor="w", padx=20, pady=2)
    
    # Campo para novo banco
    entry_banco_nome = ctk.CTkEntry(frame_banco, placeholder_text="Nome do Banco")
    entry_banco_nome.pack(padx=10, pady=2)

    def adicionar_banco():
        # Gera ID automaticamente
        next_id = get_next_id("BANCO")
        
        # Verifica se o campo está preenchido
        if not entry_banco_nome.get():
            messagebox.showerror("Erro", "O nome do banco é obrigatório.")
            return
        
        # Adiciona ao arquivo .env
        with open(ENV_PATH, "a") as f:
            f.write(f"BANCO_{next_id}={entry_banco_nome.get()}\n")
        
        # Recarrega as variáveis de ambiente
        load_env_config()
        
        messagebox.showinfo("Salvo", f"Banco {next_id} cadastrado com sucesso.")
        
        # Limpa o campo após o cadastro
        entry_banco_nome.delete(0, ctk.END)
        
        # Reinicia a aplicação para atualizar a lista de bancos
        app.destroy()
        os.system(f"python {__file__}")

    btn_add_banco = ctk.CTkButton(frame_banco, text="Cadastrar Banco", command=adicionar_banco)
    btn_add_banco.pack(padx=10, pady=5)

    # === Botão para salvar JAVA/MAVEN ===
    def salvar_java_maven():
        # Atualiza o arquivo .env com os novos valores
        java_home = entry_java.get()
        maven_home = entry_maven.get()
        
        # Lê o conteúdo atual do arquivo
        env_content = ""
        if os.path.exists(ENV_PATH):
            with open(ENV_PATH, "r") as f:
                env_content = f.read()
        
        # Remove as linhas existentes de JAVA_HOME e MAVEN_HOME
        lines = env_content.splitlines()
        new_lines = [line for line in lines if not line.startswith("JAVA_HOME=") and not line.startswith("MAVEN_HOME=")]
        
        # Adiciona as novas linhas
        new_lines.append(f"JAVA_HOME={java_home}")
        new_lines.append(f"MAVEN_HOME={maven_home}")
        
        # Escreve de volta no arquivo
        with open(ENV_PATH, "w") as f:
            f.write("\n".join(new_lines) + "\n")
        
        # Recarrega as variáveis de ambiente
        load_env_config()
        
        messagebox.showinfo("Salvo", "Caminhos JAVA_HOME e MAVEN_HOME salvos no .env")

    btn_salvar_geral = ctk.CTkButton(app, text="Salvar JAVA/MAVEN", command=salvar_java_maven)
    btn_salvar_geral.pack(pady=10)

    app.mainloop()
