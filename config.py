import os
import dotenv
import re

def load_env_config():
    ENV_PATH = ".env"
    if os.path.exists(ENV_PATH):
        dotenv.load_dotenv(ENV_PATH)
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

    # Caminho do arquivo .env
    ENV_PATH = ".env"

    # Carrega variáveis do .env
    if os.path.exists(ENV_PATH):
        dotenv.load_dotenv(ENV_PATH)

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

    entry_ip = ctk.CTkEntry(frame_origem, placeholder_text="IP")
    entry_porta = ctk.CTkEntry(frame_origem, placeholder_text="Porta")
    entry_usuario = ctk.CTkEntry(frame_origem, placeholder_text="Usuário")
    entry_senha = ctk.CTkEntry(frame_origem, placeholder_text="Senha")

    for entry in [entry_ip, entry_porta, entry_usuario, entry_senha]:
        entry.pack(padx=10, pady=2)

    def adicionar_origem():
        # Gera ID automaticamente
        next_id = get_next_id("DB")
        prefix = f"DB_{next_id}"
        
        with open(ENV_PATH, "a") as f:
            f.write(f"{prefix}_IP={entry_ip.get()}\n")
            f.write(f"{prefix}_PORTA={entry_porta.get()}\n")
            f.write(f"{prefix}_USER={entry_usuario.get()}\n")
            f.write(f"{prefix}_PASS={entry_senha.get()}\n")
        
        messagebox.showinfo("Salvo", f"Origem {next_id} cadastrada com sucesso.")
        
        # Limpa os campos após o cadastro
        for entry in [entry_ip, entry_porta, entry_usuario, entry_senha]:
            entry.delete(0, ctk.END)

    btn_add_origem = ctk.CTkButton(frame_origem, text="Cadastrar Origem", command=adicionar_origem)
    btn_add_origem.pack(padx=10, pady=5)

    # === Frame para adicionar nome de banco ===
    frame_banco = ctk.CTkFrame(app)
    frame_banco.pack(pady=10, fill="x", padx=20)
    ctk.CTkLabel(frame_banco, text="Cadastro de Nome de Banco", font=("Arial", 18, "bold"), anchor="w").pack(anchor="w", padx=10, pady=5)

    entry_banco_nome = ctk.CTkEntry(frame_banco, placeholder_text="Nome do Banco")
    entry_banco_nome.pack(padx=10, pady=2)

    def adicionar_banco():
        # Gera ID automaticamente
        next_id = get_next_id("BANCO")
        
        with open(ENV_PATH, "a") as f:
            f.write(f"BANCO_{next_id}={entry_banco_nome.get()}\n")
        
        messagebox.showinfo("Salvo", f"Banco {next_id} cadastrado com sucesso.")
        
        # Limpa o campo após o cadastro
        entry_banco_nome.delete(0, ctk.END)

    btn_add_banco = ctk.CTkButton(frame_banco, text="Cadastrar Banco", command=adicionar_banco)
    btn_add_banco.pack(padx=10, pady=5)

    # === Botão para salvar JAVA/MAVEN ===
    def salvar_java_maven():
        with open(ENV_PATH, "a") as f:
            f.write(f"JAVA_HOME={entry_java.get()}\n")
            f.write(f"MAVEN_HOME={entry_maven.get()}\n")
        messagebox.showinfo("Salvo", "Caminhos JAVA_HOME e MAVEN_HOME salvos no .env")

    btn_salvar_geral = ctk.CTkButton(app, text="Salvar JAVA/MAVEN", command=salvar_java_maven)
    btn_salvar_geral.pack(pady=10)

    app.mainloop()
