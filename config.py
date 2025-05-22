import os
import dotenv

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

# A interface gráfica de configuração só deve rodar se este arquivo for executado diretamente
if __name__ == "__main__":
    import customtkinter as ctk
    from tkinter import messagebox

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
    ctk.CTkLabel(frame_java, text="Configuração Java e Maven", font=("Arial", 18, "bold")).pack(anchor="w", padx=10, pady=5)

    entry_java = ctk.CTkEntry(frame_java, placeholder_text="JAVA_HOME", width=600)
    entry_java.insert(0, os.getenv("JAVA_HOME", ""))
    entry_java.pack(padx=10, pady=5)

    entry_maven = ctk.CTkEntry(frame_java, placeholder_text="MAVEN_HOME", width=600)
    entry_maven.insert(0, os.getenv("MAVEN_HOME", ""))
    entry_maven.pack(padx=10, pady=5)

    # === Frame para adicionar nova origem de banco ===
    frame_origem = ctk.CTkFrame(app)
    frame_origem.pack(pady=10, fill="x", padx=20)
    ctk.CTkLabel(frame_origem, text="Cadastro de Origem do Banco", font=("Arial", 18, "bold")).pack(anchor="w", padx=10, pady=5)

    entry_origem_id = ctk.CTkEntry(frame_origem, placeholder_text="ID")
    entry_ip = ctk.CTkEntry(frame_origem, placeholder_text="IP")
    entry_porta = ctk.CTkEntry(frame_origem, placeholder_text="Porta")
    entry_usuario = ctk.CTkEntry(frame_origem, placeholder_text="Usuário")
    entry_senha = ctk.CTkEntry(frame_origem, placeholder_text="Senha")

    for entry in [entry_origem_id, entry_ip, entry_porta, entry_usuario, entry_senha]:
        entry.pack(padx=10, pady=2)

    def adicionar_origem():
        prefix = f"DB_{entry_origem_id.get()}"
        with open(ENV_PATH, "a") as f:
            f.write(f"{prefix}_IP={entry_ip.get()}\n")
            f.write(f"{prefix}_PORTA={entry_porta.get()}\n")
            f.write(f"{prefix}_USER={entry_usuario.get()}\n")
            f.write(f"{prefix}_PASS={entry_senha.get()}\n")
        messagebox.showinfo("Salvo", f"Origem {entry_origem_id.get()} cadastrada.")

    btn_add_origem = ctk.CTkButton(frame_origem, text="Cadastrar Origem", command=adicionar_origem)
    btn_add_origem.pack(padx=10, pady=5)

    # === Frame para adicionar nome de banco ===
    frame_banco = ctk.CTkFrame(app)
    frame_banco.pack(pady=10, fill="x", padx=20)
    ctk.CTkLabel(frame_banco, text="Cadastro de Nome de Banco", font=("Arial", 18, "bold")).pack(anchor="w", padx=10, pady=5)

    entry_banco_id = ctk.CTkEntry(frame_banco, placeholder_text="ID do Banco")
    entry_banco_nome = ctk.CTkEntry(frame_banco, placeholder_text="Nome do Banco")
    entry_banco_id.pack(padx=10, pady=2)
    entry_banco_nome.pack(padx=10, pady=2)

    def adicionar_banco():
        with open(ENV_PATH, "a") as f:
            f.write(f"BANCO_{entry_banco_id.get()}={entry_banco_nome.get()}\n")
        messagebox.showinfo("Salvo", f"Banco {entry_banco_id.get()} cadastrado.")

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
