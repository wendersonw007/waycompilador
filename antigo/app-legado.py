# import os
# import subprocess
# import platform
# import tkinter as tk
# from tkinter import filedialog, messagebox

# # Configuração do Maven e Java
# os.environ['JAVA_HOME'] = "C:\Program Files (x86)\Java\jdk-1.8"
# os.environ['PATH'] = f"{os.environ['JAVA_HOME']}\bin;{os.environ['PATH']}"
# os.environ['M2'] = "C:\apache-maven-3.8.5"
# os.environ['PATH'] = f"{os.environ['M2']}\bin;{os.environ['PATH']}"
# os.environ['MAVEN_OPTS'] = "-Xmx1024m"

# # Função para executar comandos no terminal com exibição de logs em tempo real

# def executar_comando(comando):
#     try:
#         processo = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         while True:
#             saida = processo.stdout.readline()
#             if saida == '' and processo.poll() is not None:
#                 break
#             if saida:
#                 print(saida.strip())
#         processo.wait()
#         if processo.returncode != 0:
#             erros = processo.stderr.read().strip()
#             print(f"ERRO: {erros}")
#             return False
#         return True
#     except Exception as e:
#         print(f"Erro ao executar comando: {e}")
#         return False

# # Função para seleção de diretório do projeto

# def selecionar_diretorio_projeto():
#     root = tk.Tk()
#     root.withdraw()
#     diretorio = filedialog.askdirectory(title="Selecione a pasta do projeto")
#     if not diretorio:
#         print("Nenhuma pasta selecionada. Abortando.")
#         exit(1)
#     os.chdir(diretorio)
#     print(f"Diretório do projeto: {diretorio}")
#     return diretorio

# # Selecionar o diretório do projeto
# DIRETORIO_PROJETO = selecionar_diretorio_projeto()

# # Passo 1: Seleção de Branch
# branch = input("Informe a branch: ").strip()
# print(f"Realizando checkout em {branch}")

# if not executar_comando(f"git checkout {branch}"):
#     exit(1)

# if not executar_comando("git pull"):
#     exit(1)

# # Informações do Sistema
# print("***")
# print(f"Computador: {platform.node()}        Usuario: {os.getlogin()}")

# # Passo 2: Menu de Compilação
# print("            MENU Compilacao")
# print("  ==================================")
# print("* 1. Compile ALL                   *")
# print("* 2. Compile ERP                   *")
# print("* 3. Compile API                   *")
# print("* 4. Compile WAYCHEF               *")
# print("  ==================================")
# opcao = input("Escolha uma opcao: ").strip()
# print("-----------------------------------")

# # Passo 3: Branch de Origem
# print("****")
# print("    QUAL FOI A BRANCH DE ORIGEM")
# print("  ==================================")
# print("* 1. working                       *")
# print("* 2. rc                            *")
# print("* 3. master                        *")
# print("* 9. NAO LEVAR ORIGEM              *")
# print("  ==================================")
# branch_origem = input("Escolha uma opcao: ").strip()
# print("-----------------------------------")

# branch_origem_map = {
#     "1": "working",
#     "2": "rc",
#     "3": "master",
#     "9": None
# }

# branch_origem = branch_origem_map.get(branch_origem)

# if branch_origem:
#     print(f"*Trazendo branch de ORIGEM* {branch_origem}")
#     if not executar_comando(f"git merge origin/{branch_origem}"):
#         exit(1)
#     if not executar_comando(f"git push origin {branch}"):
#         exit(1)

# # Passo 4: Configuração do Banco
# print("****")
# print("               BANCO")
# print("  =================================")
# print("* 1. Waybe-working               *")
# print("* 2. Waybe-RC                    *")
# print("* 3. Waybe-master                *")
# print("* 4. Micro-Waychef               *")
# print("* 5. sessao                      *")
# print("  =================================")
# banco_opcao = input("Escolha uma opcao: ").strip()

# banco_map = {
#     "1": "waybe",
#     "2": "waybe",
#     "3": "waybe",
#     "4": "micro-waychef",
#     "5": "waybe"
# }

# banco = banco_map.get(banco_opcao, "waybe")

# print("****")
# print("*         ORIGEM DO BANCO          ")
# print("  ==================================")
# print("* 1. Meu Banco                     *")
# print("* 2. MeuAmbienteLinux              *")
# print("* 3. ANOTAAI                       *")
# print("* 4. Docker                        *")
# print("* 5. RASP                          *")
# print("  ==================================")
# origem_opcao = input("Escolha uma opcao: ").strip()

# origem_map = {
#     "1": ("127.0.0.1", "3306", "root", "root"),
#     "2": ("192.168.5.174", "3306", "root", "root"),
#     "3": ("192.168.5.217", "3306", "root", "root"),
#     "4": ("127.0.0.1", "3309", "root", "root"),
#     "5": ("rasp.local", "3306", "root", "root")
# }

# ip_banco, porta_banco, usuario_banco, senha_banco = origem_map.get(origem_opcao, ("127.0.0.1", "3306", "root", "root"))

# # Passo 5: Compilação com Maven
# mvn_comando = f"mvn -T 10 clean install -am -Dgenerator-phase=generate-sources -Duser={usuario_banco} -Dpass={senha_banco} -Durl=jdbc:mysql://{ip_banco}:{porta_banco}/{banco}?useSSL=false -DskipTests=true"
# print(f"Executando: {mvn_comando}")
# executar_comando(mvn_comando)

# print("Compilação finalizada.")
# exit(0)
