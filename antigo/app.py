# import os
# import subprocess
# import platform
# import customtkinter as ctk
# from tkinter import filedialog
# from uuid import uuid4
# import yaml
# import threading
# import time
# import queue
# import paramiko
# from scp import SCPClient
# from pathlib import Path
# from dotenv import load_dotenv

# # Configuration and Constants
# ctk.set_appearance_mode("dark")
# ctk.set_default_color_theme("blue")

# CREATION_FLAGS = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
# ENV_FILE = os.path.join(os.getcwd(), ".env")
# EXPORT_DIR = os.path.join(os.getcwd(), "exported_images")

# # Database and Compilation Mappings (from app.py)
# ORIGEM_MAP = {
#     "1": ("127.0.0.1", "3306", "root", "root"),
#     "2": ("192.168.5.174", "3306", "root", "root"),
#     "3": ("192.168.5.217", "3306", "root", "root"),
#     "4": ("127.0.0.1", "3309", "root", "root"),
#     "5": ("rasp.local", "3306", "root", "root")
# }

# BANCO_MAP = {
#     "1": "waybe",
#     "2": "waybe",
#     "3": "waybe",
#     "4": "micro-waychef",
#     "5": "waybe"
# }

# COMPILACAO_MAP = {
#     "1": "ALL",
#     "2": "ERP",
#     "3": "API",
#     "4": "WAYCHEF"
# }

# BRANCH_ORIGEM_MAP = {
#     "1": "working",
#     "2": "rc",
#     "3": "master",
#     "9": None
# }

# # Utility Functions
# def ler_variaveis_env(arquivo_env):
#     """Read environment variables from a .env file."""
#     variaveis = {}
#     try:
#         if os.path.exists(arquivo_env):
#             with open(arquivo_env, "r", encoding="utf-8") as env:
#                 for linha in env:
#                     linha = linha.strip()
#                     if linha and not linha.startswith("#") and "=" in linha:
#                         chave, valor = linha.split("=", 1)
#                         variaveis[chave.strip()] = valor.strip()
#         return variaveis
#     except Exception as e:
#         raise Exception(f"Erro ao ler .env: {e}")

# def atualizar_env(arquivo_env, env_dict):
#     """Update the .env file with new variables."""
#     try:
#         with open(arquivo_env, "w", encoding="utf-8") as f:
#             for chave, valor in env_dict.items():
#                 f.write(f"{chave}={valor}\n")
#     except Exception as e:
#         raise Exception(f"Erro ao atualizar .env: {e}")

# def executar_comando(comando, mensagem_erro, timeout=30, shell=False, log_func=None):
#     """Execute a shell or subprocess command with error handling."""
#     try:
#         result = subprocess.run(
#             comando,
#             shell=shell,
#             capture_output=True,
#             text=True,
#             creationflags=CREATION_FLAGS,
#             timeout=timeout
#         )
#         if result.returncode != 0:
#             error_msg = f"{mensagem_erro}\n{result.stderr}"
#             if log_func:
#                 log_func(error_msg)
#             return False, error_msg
#         if log_func and result.stdout:
#             log_func(result.stdout)
#         return True, result.stdout
#     except subprocess.TimeoutExpired:
#         error_msg = f"{mensagem_erro}\nTimeout durante a execução."
#         if log_func:
#             log_func(error_msg)
#         return False, error_msg
#     except Exception as e:
#         error_msg = f"{mensagem_erro}\nErro inesperado: {e}"
#         if log_func:
#             log_func(error_msg)
#         return False, error_msg

# # Git Operations
# def atualizar_branches(diretorio, branch_combo, log_func):
#     """Update the branch dropdown with available Git branches."""
#     try:
#         os.chdir(diretorio)
#         result = subprocess.run(
#             ["git", "branch", "-r"],
#             capture_output=True,
#             text=True,
#             timeout=10
#         )
#         branches = [
#             line.split('/')[-1].strip()
#             for line in result.stdout.splitlines()
#             if "->" not in line
#         ]
#         branch_combo.configure(values=branches)
#         if branches:
#             branch_combo.set(branches[0])
#         log_func("[INFO] Branches atualizadas com sucesso.")
#     except Exception as e:
#         log_func(f"[ERRO] Erro ao atualizar branches: {e}")

# def atualizar_core_repo(core_dir, git_repo_base, log_func):
#     """Update or clone the core repository."""
#     if not os.path.exists(core_dir):
#         comando = f"git clone {git_repo_base}core.git {core_dir}"
#         return executar_comando(comando, "Erro ao clonar repositório core.", shell=True, log_func=log_func)
#     if not os.path.exists(os.path.join(core_dir, ".git")):
#         subprocess.run(f"rm -rf {core_dir}", shell=True, creationflags=CREATION_FLAGS)
#         comando = f"git clone {git_repo_base}core.git {core_dir}"
#         return executar_comando(comando, "Erro ao clonar repositório core.", shell=True, log_func=log_func)
#     current_dir = os.getcwd()
#     os.chdir(core_dir)
#     try:
#         success, output = executar_comando("git checkout dev", "Erro no checkout da branch dev do core.", shell=True, log_func=log_func)
#         if not success:
#             return success, output
#         return executar_comando("git pull", "Erro ao atualizar o core.", shell=True, log_func=log_func)
#     finally:
#         os.chdir(current_dir)

# def atualizar_projeto(projeto, branch, GIT_REPO_BASE, base_dir, log_func):
#     """Update or clone a project repository."""
#     projeto_dir = os.path.join(base_dir, projeto)
#     if not os.path.exists(projeto_dir):
#         comando = f"git clone {GIT_REPO_BASE}{projeto}.git {projeto_dir}"
#         success, output = executar_comando(comando, "Erro ao clonar o repositório do projeto.", shell=True, log_func=log_func)
#         return success, output, projeto_dir
#     if not os.path.exists(os.path.join(projeto_dir, ".git")):
#         subprocess.run(f"rm -rf {projeto_dir}", shell=True, creationflags=CREATION_FLAGS)
#         comando = f"git clone {GIT_REPO_BASE}{projeto}.git {projeto_dir}"
#         success, output = executar_comando(comando, "Erro ao clonar o repositório do projeto.", shell=True, log_func=log_func)
#         return success, output, projeto_dir
#     current_dir = os.getcwd()
#     os.chdir(projeto_dir)
#     try:
#         success, output = executar_comando(f"git checkout {branch}", f"Erro ao fazer checkout da branch {branch}.", shell=True, log_func=log_func)
#         if not success:
#             return success, output, projeto_dir
#         success, output = executar_comando("git pull", "Erro ao atualizar o projeto.", shell=True, log_func=log_func)
#         return success, output, projeto_dir
#     finally:
#         os.chdir(current_dir)

# # Docker Operations
# def verificar_docker(log_func):
#     """Verify Docker availability and daemon status."""
#     try:
#         result = subprocess.run(
#             ['docker', '--version'],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             creationflags=CREATION_FLAGS,
#             timeout=20
#         )
#         if result.returncode != 0:
#             raise Exception(f"Docker não encontrado no PATH: {result.stderr}")
#         result = subprocess.run(
#             ['docker', 'info'],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             creationflags=CREATION_FLAGS,
#             timeout=20
#         )
#         if result.returncode != 0:
#             raise Exception(f"Docker daemon não está em execução: {result.stderr}")
#         log_func("[INFO] Docker verificado com sucesso.")
#     except subprocess.TimeoutExpired:
#         raise Exception("Timeout ao verificar Docker. Verifique se o Docker Desktop está rodando.")
#     except FileNotFoundError:
#         raise Exception("Comando 'docker' não encontrado. Verifique a instalação do Docker.")

# def verificar_porta_3306(log_func):
#     """Check and free port 3306 if in use."""
#     try:
#         result = subprocess.run(
#             "docker ps --format '{{.Ports}}' | grep 3306",
#             shell=True,
#             capture_output=True,
#             text=True,
#             creationflags=CREATION_FLAGS,
#             timeout=10
#         )
#         if result.stdout.strip():
#             log_func("[AVISO] Porta 3306 já em uso. Tentando liberar...")
#             subprocess.run(
#                 "docker stop $(docker ps -q --filter expose=3306)",
#                 shell=True,
#                 capture_output=True,
#                 text=True,
#                 creationflags=CREATION_FLAGS
#             )
#             subprocess.run(
#                 "docker rm $(docker ps -a -q --filter expose=3306)",
#                 shell=True,
#                 capture_output=True,
#                 text=True,
#                 creationflags=CREATION_FLAGS
#             )
#             return False
#         return True
#     except subprocess.TimeoutExpired:
#         log_func("[ERRO] Timeout ao verificar porta 3306.")
#         return False

# def docker_login(log_func):
#     """Perform Docker Hub login."""
#     env_vars = ler_variaveis_env(ENV_FILE)
#     docker_username = env_vars.get("DOCKER_USERNAME")
#     docker_password = env_vars.get("DOCKER_PASSWORD")
#     if not docker_username or not docker_password:
#         return False, "Credenciais do Docker Hub não encontradas no .env."
#     docker_password = docker_password.strip() + "\n"
#     comando = ["docker", "login", "-u", docker_username, "--password-stdin"]
#     try:
#         proc = subprocess.Popen(
#             comando,
#             stdin=subprocess.PIPE,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             creationflags=CREATION_FLAGS
#         )
#         stdout, stderr = proc.communicate(input=docker_password, timeout=30)
#         if proc.returncode != 0:
#             return False, stderr
#         return True, stdout
#     except subprocess.TimeoutExpired:
#         return False, "Timeout ao realizar docker login."

# def ler_jar_name(projeto, compose_path):
#     """Read JAR_NAME from docker-compose.yaml."""
#     try:
#         with open(compose_path, "r", encoding="utf-8") as file:
#             compose = yaml.safe_load(file)
#             if projeto in compose["services"]:
#                 jar_name = compose["services"][projeto]["environment"].get("JAR_NAME")
#                 if jar_name:
#                     return jar_name
#                 raise Exception("JAR_NAME não definido no docker-compose.yaml.")
#             raise Exception(f"Projeto {projeto} não encontrado no docker-compose.yaml.")
#     except Exception as e:
#         raise Exception(f"Erro ao ler docker-compose.yaml: {e}")

# def gerar_dockerfile(base_dir, projeto, jar_name, log_func):
#     """Generate a Dockerfile for the project."""
#     dockerfile_path = os.path.join(base_dir, "Dockerfile")
#     dockerfile_content = f"""FROM sifatsistemas/alpine-openjdk17 AS stage-build
# WORKDIR /build
# COPY core/ ./core/
# RUN cd core && mvn clean install

# WORKDIR /build
# COPY {projeto}/ ./{projeto}/
# RUN cd {projeto} && mvn clean && mvn clean package -DskipTests=true

# FROM bellsoft/liberica-openjdk-alpine:17.0.6 AS deploy
# WORKDIR /microsservico
# ARG JAR_NAME={jar_name}
# ARG PROFILE
# ARG ADDITIONAL_OPTS
# COPY --from=stage-build /build/{projeto}/target/{jar_name} /microsservico/{jar_name}
# CMD exec java ${{ADDITIONAL_OPTS}} -jar {jar_name} --spring.profiles.active=${{PROFILE}}
# """
#     try:
#         with open(dockerfile_path, "w", encoding="utf-8") as dockerfile:
#             dockerfile.write(dockerfile_content)
#         log_func(f"[INFO] Dockerfile gerado em: {dockerfile_path}")
#     except Exception as e:
#         log_func(f"[ERRO] Erro ao gerar Dockerfile: {e}")
#         raise

# def exportar_imagem_docker(docker_image, output_path, log_func):
#     """Export a Docker image to a tar file."""
#     try:
#         os.makedirs(output_path, exist_ok=True)
#         tar_path = os.path.join(output_path, f"{docker_image.replace('/', '_').replace(':', '_')}.tar")
#         log_func(f"[INFO] Exportando imagem {docker_image} para {tar_path}...")
#         result = subprocess.run(
#             ["docker", "save", "-o", tar_path, docker_image],
#             text=True,
#             capture_output=True,
#             creationflags=CREATION_FLAGS,
#             timeout=60
#         )
#         if result.returncode != 0:
#             raise Exception(f"Erro ao exportar a imagem {docker_image}: {result.stderr}")
#         log_func(f"[SUCESSO] Imagem {docker_image} exportada com sucesso para {tar_path}.")
#         return tar_path
#     except Exception as e:
#         log_func(f"[ERRO] Erro ao exportar imagem Docker: {e}")
#         raise

# def deploy_remoto(tar_files, compose_path, projeto, branch, log_func):
#     """Deploy Docker images to a remote server via SSH."""
#     env_vars = ler_variaveis_env(ENV_FILE)
#     REMOTE_HOST = env_vars.get("REMOTE_HOST")
#     REMOTE_USER = env_vars.get("REMOTE_USER")
#     REMOTE_PASSWORD = env_vars.get("REMOTE_PASSWORD")
#     REMOTE_SSH_KEY = env_vars.get("REMOTE_SSH_KEY")
#     REMOTE_COMPOSE_DIR = env_vars.get("REMOTE_COMPOSE_DIR")

#     if not REMOTE_HOST or not REMOTE_USER or not REMOTE_COMPOSE_DIR:
#         raise Exception("Variáveis REMOTE_HOST, REMOTE_USER e REMOTE_COMPOSE_DIR devem estar definidas no .env.")

#     ssh_client = paramiko.SSHClient()
#     ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     try:
#         if REMOTE_SSH_KEY:
#             private_key = paramiko.RSAKey.from_private_key_file(REMOTE_SSH_KEY)
#             ssh_client.connect(REMOTE_HOST, username=REMOTE_USER, pkey=private_key, timeout=10)
#         else:
#             ssh_client.connect(REMOTE_HOST, username=REMOTE_USER, password=REMOTE_PASSWORD, timeout=10)
#         log_func("[SUCESSO] Conexão SSH estabelecida com sucesso.")

#         REMOTE_BUILD_DIR = os.path.join(REMOTE_COMPOSE_DIR, "build")
#         ssh_client.exec_command(f"mkdir -p {REMOTE_BUILD_DIR}")
#         log_func(f"[INFO] Diretório remoto {REMOTE_BUILD_DIR} criado ou validado.")

#         env_content = f"""# Variáveis locais
# BRANCH={branch}
# HOST_BD={env_vars.get('HOST_BD','localhost')}
# PORTA_BD={env_vars.get('PORTA_BD','3306')}
# NOME_BD={env_vars.get('NOME_BD','default_db')}
# USUARIO_BD={env_vars.get('USUARIO_BD','root')}
# SENHA_BD={env_vars.get('SENHA_BD','')}
# """
#         remote_env_path = os.path.join(REMOTE_COMPOSE_DIR, ".env").replace("\\", "/")
#         ssh_client.exec_command(f"echo '{env_content}' > {remote_env_path}")
#         log_func(f"[SUCESSO] Arquivo .env remoto atualizado em {remote_env_path}.")

#         with SCPClient(ssh_client.get_transport()) as scp:
#             for tar_file in tar_files:
#                 scp.put(tar_file, remote_path=REMOTE_BUILD_DIR)
#                 log_func(f"[INFO] Arquivo {tar_file} transferido para {REMOTE_BUILD_DIR}.")
#             scp.put(compose_path, remote_path=REMOTE_COMPOSE_DIR)
#             log_func(f"[INFO] Arquivo {compose_path} transferido para {REMOTE_COMPOSE_DIR}.")

#         cmd_verificar_container = f"docker ps -q --filter name={projeto}"
#         stdin, stdout, stderr = ssh_client.exec_command(cmd_verificar_container)
#         container_id = stdout.read().decode().strip()
#         if container_id:
#             ssh_client.exec_command(f"docker stop {projeto}")
#             log_func(f"[INFO] Container {projeto} parado.")
#             time.sleep(2)

#         ssh_client.exec_command(f"docker rm {projeto} || true")
#         log_func(f"[INFO] Container {projeto} removido, se existia.")

#         imagem = projeto.replace("-", "")
#         docker_image = f"{env_vars.get('DOCKER_USERNAME')}/ms-{imagem}:{branch}"
#         ssh_client.exec_command(f"docker rmi {docker_image} || true")
#         log_func(f"[INFO] Imagem {docker_image} removida, se existia.")

#         for tar_file in tar_files:
#             tar_name = os.path.basename(tar_file)
#             remote_tar_path = os.path.join(REMOTE_BUILD_DIR, tar_name).replace("\\", "/")
#             cmd_load = f"docker load -i {remote_tar_path}"
#             stdin, stdout, stderr = ssh_client.exec_command(cmd_load)
#             exit_status = stdout.channel.recv_exit_status()
#             if exit_status != 0:
#                 raise Exception(f"Erro ao carregar imagem: {stderr.read().decode().strip()}")
#         remote_compose_path = os.path.join(REMOTE_COMPOSE_DIR, "docker-compose.yaml").replace("\\", "/")
#         cmd_up = f"cd {REMOTE_COMPOSE_DIR} && docker compose -f {remote_compose_path} up -d --no-deps --force-recreate {projeto}"
#         stdin, stdout, stderr = ssh_client.exec_command(cmd_up)
#         exit_status = stdout.channel.recv_exit_status()
#         if exit_status != 0:
#             raise Exception(f"Erro ao recriar container: {stderr.read().decode().strip()}")
#         log_func(f"[INFO] Container para {projeto} recriado no remoto.")
#     except Exception as e:
#         log_func(f"[ERRO] Erro no deploy remoto: {e}")
#         raise
#     finally:
#         ssh_client.close()

# # Main Workflow Functions
# def executar_compilacao(diretorio, branch, banco_opcao, origem_opcao, compilacao_opcao, branch_origem_opcao, log_func, update_queue):
#     """Execute the project compilation workflow."""
#     update_queue.put(('start', 'Compilação em andamento...', 0))
#     total_steps = 4
#     step_increment = 100 / total_steps
#     current_progress = 0

#     try:
#         if not os.path.isdir(diretorio):
#             log_func("[ERRO] Diretório do projeto inválido.")
#             update_queue.put(('finish', 'Compilação concluída com erros', 100))
#             return

#         os.chdir(diretorio)
#         log_func(f"[INFO] Computador: {platform.node()} | Usuário: {os.getlogin()}")
#         log_func(f"[INFO] Diretório do projeto: {diretorio}")

#         # Step 1: Checkout and pull
#         log_func(f"[INFO] Realizando checkout em {branch}")
#         success, output = executar_comando(f"git checkout {branch}", "Erro no checkout da branch.", shell=True, log_func=log_func)
#         if not success:
#             raise Exception(output)
#         success, output = executar_comando("git pull", "Erro ao atualizar a branch.", shell=True, log_func=log_func)
#         if not success:
#             raise Exception(output)
#         current_progress += step_increment
#         update_queue.put(('progress', current_progress))

#         # Step 2: Merge origin branch
#         branch_origem = BRANCH_ORIGEM_MAP.get(branch_origem_opcao)
#         if branch_origem:
#             log_func(f"[INFO] Trazendo branch de origem: {branch_origem}")
#             success, output = executar_comando(f"git merge origin/{branch_origem}", "Erro ao mesclar branch de origem.", shell=True, log_func=log_func)
#             if not success:
#                 raise Exception(output)
#             success, output = executar_comando(f"git push origin {branch}", "Erro ao enviar alterações.", shell=True, log_func=log_func)
#             if not success:
#                 raise Exception(output)
#         current_progress += step_increment
#         update_queue.put(('progress', current_progress))

#         # Step 3: Configure database
#         banco = BANCO_MAP.get(banco_opcao.split('.')[0])
#         ip_banco, porta_banco, usuario_banco, senha_banco = ORIGEM_MAP.get(origem_opcao.split('.')[0], ("127.0.0.1", "3306", "root", "root"))
#         current_progress += step_increment
#         update_queue.put(('progress', current_progress))

#         # Step 4: Maven compilation
#         mvn_comando = (
#             f"mvn -T 10 clean install -am -Dgenerator-phase=generate-sources "
#             f"-Duser={usuario_banco} -Dpass={senha_banco} "
#             f"-Durl=jdbc:mysql://{ip_banco}:{porta_banco}/{banco}?useSSL=false -DskipTests=true"
#         )
#         log_func(f"[INFO] Executando: {mvn_comando}")
#         success, output = executar_comando(mvn_comando, "Erro na compilação Maven.", shell=True, log_func=log_func, timeout=600)
#         if not success:
#             raise Exception(output)
#         log_func("[INFO] Compilação finalizada com sucesso.")
#         current_progress += step_increment
#         update_queue.put(('finish', 'Compilação concluída', 100))

#     except Exception as e:
#         log_func(f"[ERRO] {e}")
#         update_queue.put(('finish', 'Compilação concluída com erros', 100))

# def executar_deploy(project_names, branch, compose_path, scenario, update_queue, log_func):
#     """Execute the deployment workflow for individual APIs."""
#     update_queue.put(('start', 'Deploy em andamento...', 0))
#     projects = [p.strip() for p in project_names.split(",") if p.strip()]
#     total_steps_per_project = 8
#     errors = []
#     successes = []

#     try:
#         for project_index, project_name in enumerate(projects):
#             log_func(f"\n[INFO] Iniciando deploy da API: {project_name} (Projeto {project_index + 1}/{len(projects)})")
#             update_queue.put(('start', f"Processando: {project_name}", 0))
#             step_increment = 100 / total_steps_per_project
#             current_progress = 0

#             try:
#                 # Step 1: Update .env
#                 env_vars = ler_variaveis_env(ENV_FILE)
#                 env_vars["BRANCH"] = branch
#                 atualizar_env(ENV_FILE, env_vars)
#                 log_func("[INFO] .env atualizado com sucesso.")
#                 current_progress += step_increment
#                 update_queue.put(('progress', current_progress))

#                 # Step 2: Verify Docker
#                 verificar_docker(log_func)
#                 current_progress += step_increment
#                 update_queue.put(('progress', current_progress))

#                 # Step 3: Docker login
#                 if scenario == "Push para Docker Hub":
#                     success, output = docker_login(log_func)
#                     if not success:
#                         raise Exception("Erro no docker login. Verifique as credenciais no .env.")
#                 current_progress += step_increment
#                 update_queue.put(('progress', current_progress))

#                 # Step 4: Update core repository
#                 GIT_REPO_BASE = "git@github.com:sifatsistemas-desenvolvimento/"
#                 core_dir = os.path.join(os.getcwd(), "core")
#                 success, output = atualizar_core_repo(core_dir, GIT_REPO_BASE, log_func)
#                 if not success:
#                     raise Exception("Erro ao atualizar/clonar o repositório core.")
#                 current_progress += step_increment
#                 update_queue.put(('progress', current_progress))

#                 # Step 5: Update project repository
#                 success, output, projeto_dir = atualizar_projeto(project_name, branch, GIT_REPO_BASE, os.getcwd(), log_func)
#                 if not success:
#                     raise Exception("Erro ao atualizar/clonar o repositório do projeto.")
#                 current_progress += step_increment
#                 update_queue.put(('progress', current_progress))

#                 # Step 6: Checkout and pull branch
#                 os.chdir(projeto_dir)
#                 success, output = executar_comando(f"git checkout {branch}", f"Erro ao fazer checkout da branch {branch}.", shell=True, log_func=log_func)
#                 if not success:
#                     raise Exception("Erro no checkout da branch.")
#                 success, output = executar_comando("git pull", "Erro ao atualizar o projeto.", shell=True, log_func=log_func)
#                 if not success:
#                     raise Exception("Erro ao atualizar o projeto.")
#                 os.chdir(os.getcwd())
#                 current_progress += step_increment
#                 update_queue.put(('progress', current_progress))

#                 # Step 7: Generate Dockerfile
#                 jar_name = ler_jar_name(project_name, compose_path)
#                 gerar_dockerfile(os.getcwd(), project_name, jar_name, log_func)
#                 current_progress += step_increment
#                 update_queue.put(('progress', current_progress))

#                 # Step 8: Build and execute scenario
#                 env_vars = ler_variaveis_env(ENV_FILE)
#                 docker_username = env_vars.get("DOCKER_USERNAME", "usuario")
#                 imagem = project_name.replace("-", "")
#                 docker_image = f"{docker_username}/ms-{imagem}:{branch}"
#                 build_command = f"docker image build -t {docker_image} -f {os.path.join(os.getcwd(), 'Dockerfile')} {os.getcwd()}"
#                 success, output = executar_comando(build_command, "Erro ao construir a imagem Docker.", shell=True, log_func=log_func, timeout=300)
#                 if not success:
#                     raise Exception("Erro ao construir a imagem Docker.")

#                 if scenario == "Atualizar Dockerfile localmente":
#                     if not verificar_porta_3306(log_func):
#                         log_func("[INFO] Porta 3306 foi liberada. Continuando deploy...")
#                     cmd = f"docker compose up -d --no-deps --force-recreate --build {project_name}"
#                     success, output = executar_comando(cmd, "Erro ao recriar o container.", shell=True, log_func=log_func, timeout=120)
#                     if not success:
#                         rm_success, rm_output = executar_comando(
#                             f"docker rm -f {project_name}",
#                             f"Erro ao remover o container {project_name}.",
#                             shell=True,
#                             log_func=log_func,
#                             timeout=30
#                         )
#                         if not rm_success:
#                             raise Exception("Erro ao remover o container.")
#                         success, output = executar_comando(
#                             f"docker compose up -d --build {project_name}",
#                             "Erro ao recriar o container após remoção.",
#                             shell=True,
#                             log_func=log_func,
#                             timeout=120
#                         )
#                         if not success:
#                             raise Exception("Erro ao recriar o container após remoção.")
#                 elif scenario == "Push para Docker Hub":
#                     success, output = executar_comando(
#                         f"docker push {docker_image}",
#                         "Erro ao realizar push da imagem.",
#                         shell=True,
#                         log_func=log_func,
#                         timeout=300
#                     )
#                     if not success:
#                         raise Exception("Erro ao realizar push da imagem para o Docker Hub.")
#                 elif scenario == "Deploy Remoto via SSH":
#                     tar_file = exportar_imagem_docker(docker_image, EXPORT_DIR, log_func)
#                     deploy_remoto([tar_file], compose_path, project_name, branch, log_func)

#                 current_progress = 100
#                 update_queue.put(('progress', current_progress))
#                 successes.append(project_name)
#                 log_func(f"[SUCESSO] Deploy da API {project_name} concluído com sucesso!")

#             except Exception as e:
#                 errors.append((project_name, str(e)))
#                 log_func(f"[ERRO] Falha no deploy da API {project_name}: {e}")
#                 update_queue.put(('progress', 100))

#         log_func("\n[RESUMO DO DEPLOY]")
#         if successes:
#             log_func(f"[SUCESSO] APIs implantadas com sucesso: {', '.join(successes)}")
#         if errors:
#             log_func("[ERROS ENCONTRADOS]")
#             for project_name, error in errors:
#                 log_func(f"- API {project_name}: {error}")
#         else:
#             log_func("[INFO] Nenhum erro encontrado durante o deploy.")
#         update_queue.put(('finish', 'Deploy concluído', 100))

#     except Exception as e:
#         log_func(f"[ERRO] Erro inesperado no deploy: {e}")
#         update_queue.put(('finish', 'Deploy concluído com erros', 100))

# def executar_limpeza_geral(local, update_queue, log_func):
#     """Execute the general cleanup workflow (local or remote)."""
#     update_queue.put(('start', 'Limpeza em andamento...', 0))
#     total_steps = 7
#     step_increment = 100 / total_steps
#     current_progress = 0

#     try:
#         # Step 1: Verify Docker
#         verificar_docker(log_func)
#         current_progress += step_increment
#         update_queue.put(('progress', current_progress))

#         # Step 2: Stop all containers
#         log_func("[INFO] Parando todos os containers...")
#         result = subprocess.run(
#             "docker ps -q",
#             shell=True,
#             capture_output=True,
#             text=True,
#             creationflags=CREATION_FLAGS,
#             timeout=10
#         )
#         if result.stdout.strip():
#             cmd_stop = f"docker stop {result.stdout.strip()}"
#             success, output = executar_comando(cmd_stop, "Erro ao parar containers.", shell=True, log_func=log_func, timeout=30)
#             if not success:
#                 raise Exception("Falha ao parar containers.")
#             time.sleep(5)
#         log_func("[INFO] Containers parados com sucesso.")
#         current_progress += step_increment
#         update_queue.put(('progress', current_progress))

#         # Step 3: Run docker compose down
#         compose_path = os.path.join(os.getcwd(), "docker-compose.yaml")
#         if os.path.exists(compose_path):
#             log_func("[INFO] Executando 'docker compose down'...")
#             cmd_down = f"docker compose -f {compose_path} down"
#             success, output = executar_comando(cmd_down, "Erro ao executar 'docker compose down'.", shell=True, log_func=log_func, timeout=60)
#             log_func(output or "[INFO] 'docker compose down' executado com sucesso.")
#             time.sleep(5)
#         else:
#             log_func("[AVISO] Arquivo docker-compose.yaml não encontrado.")
#         current_progress += step_increment
#         update_queue.put(('progress', current_progress))

#         # Step 4: Remove all containers
#         log_func("[INFO] Removendo todos os containers...")
#         max_attempts = 3
#         for attempt in range(1, max_attempts + 1):
#             result = subprocess.run(
#                 "docker ps -a -q",
#                 shell=True,
#                 capture_output=True,
#                 text=True,
#                 creationflags=CREATION_FLAGS,
#                 timeout=10
#             )
#             container_ids = result.stdout.strip().splitlines()
#             log_func(f"[DEBUG] Containers encontrados (Tentativa {attempt}): {result.stdout.strip()}")
#             if container_ids:
#                 for container_id in container_ids:
#                     container_id = container_id.strip()
#                     if container_id and container_id != "31b69c305130":  # Ignore service-registry
#                         cmd_rm = f"docker rm -f {container_id}"
#                         success, output = executar_comando(
#                             cmd_rm,
#                             f"Erro ao remover container {container_id} na tentativa {attempt}.",
#                             shell=True,
#                             log_func=log_func,
#                             timeout=10
#                         )
#                         if not success:
#                             log_func(f"[AVISO] Falha ao remover container {container_id}: {output}")
#                         time.sleep(1)
#                 time.sleep(5)
#             else:
#                 log_func(f"[INFO] Nenhum container para remover na tentativa {attempt}.")
#                 break
#         else:
#             result = subprocess.run(
#                 "docker ps -a -q",
#                 shell=True,
#                 capture_output=True,
#                 text=True,
#                 creationflags=CREATION_FLAGS,
#                 timeout=10
#             )
#             if result.stdout.strip():
#                 raise Exception(f"Falha ao remover todos os containers após {max_attempts} tentativas.")
#         current_progress += step_increment
#         update_queue.put(('progress', current_progress))

#         # Step 5: Remove service-registry
#         log_func("[INFO] Verificando container service-registry...")
#         result = subprocess.run(
#             "docker ps -a -q --filter name=service-registry",
#             shell=True,
#             capture_output=True,
#             text=True,
#             creationflags=CREATION_FLAGS,
#             timeout=10
#         )
#         if result.stdout.strip():
#             cmd_rm = f"docker rm -f {result.stdout.strip()}"
#             success, output = executar_comando(
#                 cmd_rm,
#                 "Erro ao remover container service-registry.",
#                 shell=True,
#                 log_func=log_func,
#                 timeout=10
#             )
#             if not success:
#                 log_func(f"[AVISO] Falha ao remover container service-registry: {output}")
#         current_progress += step_increment
#         update_queue.put(('progress', current_progress))

#         # Step 6: Remove images (local only)
#         if local:
#             log_func("[INFO] Removendo todas as imagens...")
#             max_attempts = 3
#             for attempt in range(1, max_attempts + 1):
#                 result = subprocess.run(
#                     "docker images -q -a",
#                     shell=True,
#                     capture_output=True,
#                     text=True,
#                     creationflags=CREATION_FLAGS,
#                     timeout=10
#                 )
#                 image_ids = list(set(result.stdout.strip().splitlines()))
#                 log_func(f"[DEBUG] Imagens encontradas (Tentativa {attempt}): {result.stdout.strip()}")
#                 if image_ids:
#                     for image_id in image_ids:
#                         image_id = image_id.strip()
#                         if image_id:
#                             cmd_rmi = f"docker rmi -f {image_id}"
#                             success, output = executar_comando(
#                                 cmd_rmi,
#                                 f"Erro ao remover imagem {image_id} na tentativa {attempt}.",
#                                 shell=True,
#                                 log_func=log_func,
#                                 timeout=10
#                             )
#                             if not success:
#                                 log_func(f"[AVISO] Falha ao remover imagem {image_id}: {output}")
#                             time.sleep(1)
#                     time.sleep(5)
#                 else:
#                     log_func(f"[INFO] Nenhuma imagem para remover na tentativa {attempt}.")
#                     break
#             else:
#                 result = subprocess.run(
#                     "docker images -q -a",
#                     shell=True,
#                     capture_output=True,
#                     text=True,
#                     creationflags=CREATION_FLAGS,
#                     timeout=10
#                 )
#                 if result.stdout.strip():
#                     raise Exception(f"Falha ao remover todas as imagens após {max_attempts} tentativas.")
#             current_progress += step_increment
#             update_queue.put(('progress', current_progress))

#             # Validate cleanup
#             containers = subprocess.run(
#                 "docker ps -a -q",
#                 shell=True,
#                 capture_output=True,
#                 text=True,
#                 creationflags=CREATION_FLAGS,
#                 timeout=10
#             ).stdout.strip()
#             images = subprocess.run(
#                 "docker images -q -a",
#                 shell=True,
#                 capture_output=True,
#                 text=True,
#                 creationflags=CREATION_FLAGS,
#                 timeout=10
#             ).stdout.strip()
#             if containers or images:
#                 raise Exception(f"Limpeza incompleta: containers ou imagens ainda presentes. Containers: {containers}, Imagens: {images}")
#             log_func("[INFO] Limpeza validada com sucesso.")
#         else:
#             # Step 6: Remote cleanup
#             env_vars = ler_variaveis_env(ENV_FILE)
#             REMOTE_HOST = env_vars.get("REMOTE_HOST")
#             REMOTE_USER = env_vars.get("REMOTE_USER")
#             REMOTE_PASSWORD = env_vars.get("REMOTE_PASSWORD")
#             REMOTE_SSH_KEY = env_vars.get("REMOTE_SSH_KEY")

#             if not REMOTE_HOST or not REMOTE_USER:
#                 log_func("[ERRO] Variáveis REMOTE_HOST e REMOTE_USER devem estar definidas no .env.")
#                 update_queue.put(('finish', 'Limpeza concluída com erros', 100))
#                 return

#             ssh_client = paramiko.SSHClient()
#             ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#             try:
#                 if REMOTE_SSH_KEY:
#                     private_key = paramiko.RSAKey.from_private_key_file(REMOTE_SSH_KEY)
#                     ssh_client.connect(REMOTE_HOST, username=REMOTE_USER, pkey=private_key, timeout=10)
#                 else:
#                     ssh_client.connect(REMOTE_HOST, username=REMOTE_USER, password=REMOTE_PASSWORD, timeout=10)
#                 log_func("[SUCESSO] Conexão SSH estabelecida com sucesso.")

#                 log_func("[INFO] Parando todos os containers no remoto...")
#                 stdin, stdout, stderr = ssh_client.exec_command("docker ps -q", timeout=10)
#                 container_ids = stdout.read().decode().strip()
#                 if container_ids:
#                     ssh_client.exec_command(f"docker stop {container_ids}", timeout=30)
#                     log_func("[INFO] Containers parados no remoto.")
#                 else:
#                     log_func("[INFO] Nenhum container em execução no remoto.")

#                 log_func("[INFO] Removendo todos os containers no remoto...")
#                 max_attempts = 3
#                 for attempt in range(1, max_attempts + 1):
#                     stdin, stdout, stderr = ssh_client.exec_command("docker ps -a -q", timeout=10)
#                     container_ids = stdout.read().decode().strip()
#                     log_func(f"[DEBUG] Containers remotos encontrados (Tentativa {attempt}): {container_ids}")
#                     if container_ids:
#                         ssh_client.exec_command(f"docker rm -f {container_ids}", timeout=30)
#                         log_func(f"[INFO] Containers removidos no remoto na tentativa {attempt}.")
#                         time.sleep(5)
#                     else:
#                         log_func(f"[INFO] Nenhum container para remover na tentativa {attempt}.")
#                         break
#                 else:
#                     stdin, stdout, stderr = ssh_client.exec_command("docker ps -a -q", timeout=10)
#                     if stdout.read().decode().strip():
#                         raise Exception("Containers ainda presentes no remoto após remoção.")

#                 log_func("[INFO] Removendo todas as imagens no remoto...")
#                 stdin, stdout, stderr = ssh_client.exec_command("docker images -q -a | sort -u", timeout=10)
#                 image_ids = stdout.read().decode().strip()
#                 if image_ids:
#                     stdin, stdout, stderr = ssh_client.exec_command(f"docker rmi -f {image_ids}", timeout=60)
#                     exit_status = stdout.channel.recv_exit_status()
#                     if exit_status != 0:
#                         log_func(f"[ERRO] Falha ao remover imagens no remoto: {stderr.read().decode().strip()}")
#                         raise Exception("Falha ao remover imagens no remoto.")
#                     log_func("[INFO] Imagens removidas no remoto.")
#                     stdin, stdout, stderr = ssh_client.exec_command("docker images -q -a", timeout=10)
#                     if stdout.read().decode().strip():
#                         raise Exception("Imagens ainda presentes no remoto após remoção.")
#                 else:
#                     log_func("[INFO] Nenhuma imagem para remover no remoto.")

#                 log_func("[INFO] Validando limpeza remota...")
#                 stdin, stdout, stderr = ssh_client.exec_command("docker ps -a -q", timeout=10)
#                 containers = stdout.read().decode().strip()
#                 stdin, stdout, stderr = ssh_client.exec_command("docker images -q -a", timeout=10)
#                 images = stdout.read().decode().strip()
#                 if containers or images:
#                     raise Exception("Limpeza remota incompleta: containers ou imagens ainda presentes.")
#                 log_func("[INFO] Limpeza remota validada com sucesso.")
#             finally:
#                 ssh_client.close()
#             current_progress += step_increment
#             update_queue.put(('progress', current_progress))

#         log_func("[INFO] Limpeza geral concluída com sucesso!")
#         update_queue.put(('finish', 'Limpeza concluída', 100))

#     except Exception as e:
#         log_func(f"[ERRO] {e}")
#         update_queue.put(('finish', 'Limpeza concluída com erros', 100))

# def executar_deploy_todos(local, branch, compose_path, update_queue, log_func):
#     """Execute the full deployment workflow (local or remote)."""
#     update_queue.put(('start', 'Deploy em andamento...', 0))
#     total_steps = 6 if not local else 4
#     step_increment = 100 / total_steps
#     current_progress = 0

#     try:
#         # Step 1: Verify prerequisites
#         if not os.path.exists(compose_path):
#             log_func(f"[ERRO] Arquivo {compose_path} não encontrado.")
#             update_queue.put(('finish', 'Deploy concluído com erros', 100))
#             return
#         try:
#             with open(compose_path, 'r', encoding="utf-8") as f:
#                 yaml.safe_load(f)
#         except Exception as e:
#             log_func(f"[ERRO] Arquivo {compose_path} inválido: {e}")
#             update_queue.put(('finish', 'Deploy concluído com erros', 100))
#             return
#         verificar_docker(log_func)
#         current_progress += step_increment
#         update_queue.put(('progress', current_progress))

#         if local:
#             # Local deployment
#             log_func("[INFO] Atualizando .env com a branch selecionada...")
#             env_vars = ler_variaveis_env(ENV_FILE)
#             env_vars["BRANCH"] = branch
#             atualizar_env(ENV_FILE, env_vars)
#             log_func("[INFO] .env atualizado com sucesso.")
#             current_progress += step_increment
#             update_queue.put(('progress', current_progress))

#             log_func("[INFO] Verificando porta 3306...")
#             if not verificar_porta_3306(log_func):
#                 log_func("[INFO] Porta 3306 foi liberada. Continuando deploy...")
#             log_func("[INFO] Parando containers existentes...")
#             cmd_down = f"docker compose -f {compose_path} down"
#             success, output = executar_comando(cmd_down, "Erro ao parar containers existentes.", shell=True, log_func=log_func, timeout=60)
#             log_func(output or "[INFO] Containers existentes parados com sucesso.")
#             current_progress += step_increment
#             update_queue.put(('progress', current_progress))

#             log_func("[INFO] Subindo todos os containers localmente...")
#             cmd = f"docker compose -f {compose_path} up -d"
#             success, output = executar_comando(cmd, "Erro ao subir os containers.", shell=True, log_func=log_func, timeout=120)
#             if not success:
#                 if "port is already allocated" in output.lower() or "bind: address already in use" in output.lower():
#                     log_func("[ERRO] Porta 3306 ainda em uso. Tente parar outros serviços MySQL ou containers manualmente.")
#                 raise Exception("Erro ao subir os containers.")
#             log_func(f"[INFO] Todos os containers foram iniciados com sucesso localmente na branch {branch}.")
#             current_progress += step_increment
#             update_queue.put(('finish', 'Deploy concluído', 100))
#         else:
#             # Remote deployment
#             env_vars = ler_variaveis_env(ENV_FILE)
#             REMOTE_HOST = env_vars.get("REMOTE_HOST")
#             REMOTE_USER = env_vars.get("REMOTE_USER")
#             REMOTE_PASSWORD = env_vars.get("REMOTE_PASSWORD")
#             REMOTE_SSH_KEY = env_vars.get("REMOTE_SSH_KEY")
#             REMOTE_COMPOSE_DIR = env_vars.get("REMOTE_COMPOSE_DIR")

#             if not REMOTE_HOST or not REMOTE_USER or not REMOTE_COMPOSE_DIR:
#                 log_func("[ERRO] Variáveis REMOTE_HOST, REMOTE_USER e REMOTE_COMPOSE_DIR devem estar definidas no .env.")
#                 update_queue.put(('finish', 'Deploy concluído com erros', 100))
#                 return

#             ssh_client = paramiko.SSHClient()
#             ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#             try:
#                 if REMOTE_SSH_KEY:
#                     private_key = paramiko.RSAKey.from_private_key_file(REMOTE_SSH_KEY)
#                     ssh_client.connect(REMOTE_HOST, username=REMOTE_USER, pkey=private_key, timeout=10)
#                 else:
#                     ssh_client.connect(REMOTE_HOST, username=REMOTE_USER, password=REMOTE_PASSWORD, timeout=10)
#                 log_func("[SUCESSO] Conexão SSH estabelecida com sucesso.")
#                 current_progress += step_increment
#                 update_queue.put(('progress', current_progress))

#                 REMOTE_BUILD_DIR = os.path.join(REMOTE_COMPOSE_DIR, "build")
#                 ssh_client.exec_command(f"mkdir -p {REMOTE_BUILD_DIR}", timeout=10)
#                 log_func(f"[INFO] Diretório remoto {REMOTE_BUILD_DIR} criado ou validado.")

#                 env_content = f"""# Variáveis locais
# BRANCH={branch}
# HOST_BD={env_vars.get('HOST_BD','localhost')}
# PORTA_BD={env_vars.get('PORTA_BD','3306')}
# NOME_BD={env_vars.get('NOME_BD','default_db')}
# USUARIO_BD={env_vars.get('USUARIO_BD','root')}
# SENHA_BD={env_vars.get('SENHA_BD','')}
# """
#                 remote_env_path = os.path.join(REMOTE_COMPOSE_DIR, ".env").replace("\\", "/")
#                 ssh_client.exec_command(f"echo '{env_content}' > {remote_env_path}", timeout=10)
#                 log_func(f"[SUCESSO] Arquivo .env remoto atualizado em {remote_env_path}.")
#                 current_progress += step_increment
#                 update_queue.put(('progress', current_progress))

#                 with SCPClient(ssh_client.get_transport()) as scp:
#                     scp.put(compose_path, remote_path=REMOTE_COMPOSE_DIR)
#                     log_func(f"[INFO] Arquivo {compose_path} transferido para {REMOTE_COMPOSE_DIR}.")
#                 current_progress += step_increment
#                 update_queue.put(('progress', current_progress))

#                 log_func("[INFO] Parando containers existentes no remoto...")
#                 remote_compose_path = os.path.join(REMOTE_COMPOSE_DIR, "docker-compose.yaml").replace("\\", "/")
#                 cmd_down = f"cd {REMOTE_COMPOSE_DIR} && docker compose -f {remote_compose_path} down"
#                 stdin, stdout, stderr = ssh_client.exec_command(cmd_down, timeout=60)
#                 exit_status = stdout.channel.recv_exit_status()
#                 if exit_status != 0:
#                     log_func(f"[AVISO] Erro ao parar containers existentes: {stderr.read().decode().strip()}")
#                 else:
#                     log_func("[INFO] Containers existentes parados com sucesso.")
#                 current_progress += step_increment
#                 update_queue.put(('progress', current_progress))

#                 log_func("[INFO] Verificando porta 3306 no remoto...")
#                 stdin, stdout, stderr = ssh_client.exec_command("docker ps --format '{{.Ports}}' | grep 3306", timeout=10)
#                 if stdout.read().decode().strip():
#                     log_func("[INFO] Porta 3306 em uso no remoto. Liberando...")
#                     ssh_client.exec_command("docker stop $(docker ps -q --filter expose=3306)", timeout=30)
#                     ssh_client.exec_command("docker rm $(docker ps -a -q --filter expose=3306)", timeout=30)
#                 cmd_up = f"cd {REMOTE_COMPOSE_DIR} && docker compose -f {remote_compose_path} up -d"
#                 stdin, stdout, stderr = ssh_client.exec_command(cmd_up, timeout=120)
#                 exit_status = stdout.channel.recv_exit_status()
#                 if exit_status != 0:
#                     error_msg = stderr.read().decode().strip()
#                     if "port is already allocated" in error_msg.lower() or "bind: address already in use" in error_msg.lower():
#                         log_func("[ERRO] Porta 3306 ainda em uso no remoto. Tente parar outros serviços MySQL ou containers manualmente.")
#                     log_func(f"[ERRO] Erro ao subir containers: {error_msg}")
#                     update_queue.put(('finish', 'Deploy concluído com erros', 100))
#                     return
#                 log_func(f"[INFO] Todos os containers foram iniciados com sucesso no remoto na branch {branch}.")
#                 current_progress += step_increment
#                 update_queue.put(('finish', 'Deploy concluído', 100))
#             finally:
#                 ssh_client.close()

#     except Exception as e:
#         log_func(f"[ERRO] {e}")
#         update_queue.put(('finish', 'Deploy concluído com erros', 100))

# # UI Functions
# def add_log(msg, log_widget, window):
#     """Add a log message to the UI text box."""
#     try:
#         log_widget.configure(state="normal")
#         log_widget.insert(ctk.END, msg + "\n")
#         log_widget.see(ctk.END)
#         log_widget.configure(state="disabled")
#         window.update_idletasks()
#     except Exception as e:
#         print(f"[ERRO] Falha ao adicionar log na interface: {e}")

# def processar_fila(window, update_queue, log_widget, progress_bar, progress_label, buttons, entries, notebook):
#     """Process UI updates from the queue."""
#     try:
#         while not update_queue.empty():
#             item = update_queue.get_nowait()
#             action, *args = item
#             if action == 'log':
#                 add_log(args[0], log_widget, window)
#             elif action == 'start':
#                 progress_label.configure(text=args[0])
#                 progress_bar.configure(value=args[1])
#                 for btn in buttons:
#                     btn.configure(state="disabled")
#                 for entry in entries:
#                     entry.configure(state="disabled")
#                 notebook.configure(state="disabled")
#                 window.configure(cursor="wait")
#             elif action == 'progress':
#                 progress_bar.configure(value=args[0])
#             elif action == 'finish':
#                 progress_label.configure(text=args[0])
#                 progress_bar.configure(value=args[1])
#                 for btn in buttons:
#                     btn.configure(state="normal")
#                 for entry in entries:
#                     entry.configure(state="normal")
#                 notebook.configure(state="normal")
#                 window.configure(cursor="")
#             window.update_idletasks()
#     except queue.Empty:
#         pass
#     window.after(50, processar_fila, window, update_queue, log_widget, progress_bar, progress_label, buttons, entries, notebook)

# def escolher_compose_path(entry):
#     """Open a file dialog to select the docker-compose.yaml file."""
#     filename = filedialog.askopenfilename(title="Selecione o docker-compose.yaml", filetypes=[("YAML Files", "*.yaml *.yml")])
#     if filename:
#         entry.delete(0, ctk.END)
#         entry.insert(0, filename)

# def open_config_window(window, log_widget):
#     """Open a window to configure .env variables."""
#     config_win = ctk.CTkToplevel(window)
#     config_win.title("Configuração de Variáveis de Ambiente")
#     config_win.geometry("400x460")
#     config_win.resizable(False, False)

#     env_vars = ler_variaveis_env(ENV_FILE)
#     entries = {}

#     row = 0
#     for key, value in env_vars.items():
#         ctk.CTkLabel(config_win, text=key).grid(row=row, column=0, padx=5, pady=5, sticky="w")
#         entry = ctk.CTkEntry(config_win, width=250)
#         entry.insert(0, value)
#         entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")
#         entries[key] = entry
#         row += 1

#     def salvar_config():
#         novos_env = {key: entry.get().strip() for key, entry in entries.items()}
#         try:
#             atualizar_env(ENV_FILE, novos_env)
#             add_log("[INFO] Variáveis de ambiente salvas com sucesso no .env!", log_widget, window)
#             ctk.CTkToplevel.messagebox(config_win, title="Sucesso", message="Configurações salvas com sucesso!")
#             config_win.destroy()
#         except Exception as e:
#             ctk.CTkToplevel.messagebox(config_win, title="Erro", message=str(e))

#     btn_salvar = ctk.CTkButton(config_win, text="Salvar", command=salvar_config)
#     btn_salvar.grid(row=row, column=0, columnspan=2, pady=10, sticky="w")

# # Main Application
# def main():
#     """Initialize and run the main application."""
#     app = ctk.CTk()
#     app.title("Sifat Gerenciador de Projetos")
#     app.geometry("900x700")
#     app.minsize(800, 600)
#     app.grid_columnconfigure(0, weight=1)
#     app.grid_rowconfigure(1, weight=1)

#     # Notebook for tabs
#     notebook = ctk.CTkTabview(app)
#     notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
#     tab_compile = notebook.add("Compilação")
#     tab_deploy = notebook.add("Deploy API")
#     tab_cleanup = notebook.add("Limpeza")
#     tab_deploy_all = notebook.add("Deploy Todos")

#     # Queues for each tab
#     compile_queue = queue.Queue()
#     deploy_queue = queue.Queue()
#     cleanup_queue = queue.Queue()
#     deploy_all_queue = queue.Queue()

#     # Compilation Tab
#     tab_compile.grid_columnconfigure(0, weight=1)
#     tab_compile.grid_rowconfigure(4, weight=1)

#     ctk.CTkLabel(tab_compile, text="Compilação de Projetos", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)

#     project_frame = ctk.CTkFrame(tab_compile)
#     project_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
#     ctk.CTkLabel(project_frame, text="📁 Diretório do Projeto:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
#     diretorio_entry = ctk.CTkEntry(project_frame, width=400)
#     diretorio_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
#     diretorio_button = ctk.CTkButton(project_frame, text="Selecionar", command=lambda: selecionar_diretorio_projeto(diretorio_entry, branch_combo, btn_executar_compile))
#     diretorio_button.grid(row=0, column=2, sticky="w", padx=5, pady=5)

#     config_frame = ctk.CTkFrame(tab_compile)
#     config_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
#     config_frame.grid_columnconfigure(1, weight=1)

#     ctk.CTkLabel(config_frame, text="Branch:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
#     branch_combo = ctk.CTkComboBox(config_frame, width=300)
#     branch_combo.grid(row=0, column=1, sticky="w", padx=5, pady=5)

#     ctk.CTkLabel(config_frame, text="Banco:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
#     banco_combo = ctk.CTkComboBox(config_frame, width=300, values=["1. Waybe-working", "2. Waybe-RC", "3. Waybe-master", "4. Micro-Waychef", "5. Sessao"])
#     banco_combo.grid(row=1, column=1, sticky="w", padx=5, pady=5)

#     ctk.CTkLabel(config_frame, text="Origem do Banco:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
#     origem_combo = ctk.CTkComboBox(config_frame, width=300, values=["1. Meu Banco", "2. MeuAmbienteLinux", "3. ANOTAAI", "4. Docker", "5. RASP"])
#     origem_combo.grid(row=2, column=1, sticky="w", padx=5, pady=5)

#     ctk.CTkLabel(config_frame, text="Compilação:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
#     compilacao_combo = ctk.CTkComboBox(config_frame, width=300, values=["1. Compile ALL", "2. Compile ERP", "3. Compile API", "4. Compile WAYCHEF"])
#     compilacao_combo.grid(row=3, column=1, sticky="w", padx=5, pady=5)

#     ctk.CTkLabel(config_frame, text="Branch de Origem:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
#     branch_origem_combo = ctk.CTkComboBox(config_frame, width=300, values=["1. working", "2. rc", "3. master", "9. NÃO LEVAR ORIGEM"])
#     branch_origem_combo.grid(row=4, column=1, sticky="w", padx=5, pady=5)

#     progress_frame = ctk.CTkFrame(tab_compile)
#     progress_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
#     progress_frame.grid_columnconfigure(0, weight=1)
#     compile_progress_label = ctk.CTkLabel(progress_frame, text="Aguardando início")
#     compile_progress_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
#     compile_progress_bar = ctk.CTkProgressBar(progress_frame, width=400)
#     compile_progress_bar.grid(row=1, column=0, sticky="ew", padx=5, pady=2)

#     log_frame = ctk.CTkFrame(tab_compile)
#     log_frame.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)
#     log_frame.grid_columnconfigure(0, weight=1)
#     log_frame.grid_rowconfigure(0, weight=1)
#     log_text_compile = ctk.CTkTextbox(log_frame, height=200, state="disabled")
#     log_text_compile.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

#     footer_frame = ctk.CTkFrame(tab_compile)
#     footer_frame.grid(row=5, column=0, sticky="w", padx=10, pady=10)
#     btn_executar_compile = ctk.CTkButton(footer_frame, text="Compilar", state="disabled")
#     btn_executar_compile.grid(row=0, column=0, sticky="w", padx=5)
#     btn_clear_compile = ctk.CTkButton(footer_frame, text="Limpar Log", command=lambda: log_text_compile.configure(state="normal") or log_text_compile.delete(1.0, ctk.END) or log_text_compile.configure(state="disabled"))
#     btn_clear_compile.grid(row=0, column=1, sticky="w", padx=5)

#     # Deploy API Tab
#     tab_deploy.grid_columnconfigure(0, weight=1)
#     tab_deploy.grid_rowconfigure(3, weight=1)

#     ctk.CTkLabel(tab_deploy, text="Deploy de APIs", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)

#     input_frame = ctk.CTkFrame(tab_deploy)
#     input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
#     input_frame.grid_columnconfigure(1, weight=1)

#     ctk.CTkLabel(input_frame, text="Projetos (separe por vírgula):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
#     entry_project = ctk.CTkEntry(input_frame, width=400)
#     entry_project.grid(row=0, column=1, sticky="w", padx=5, pady=5)

#     ctk.CTkLabel(input_frame, text="Branch:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
#     entry_branch = ctk.CTkEntry(input_frame, width=400)
#     entry_branch.grid(row=1, column=1, sticky="w", padx=5, pady=5)

#     ctk.CTkLabel(input_frame, text="Docker Compose:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
#     entry_compose = ctk.CTkEntry(input_frame, width=300)
#     entry_compose.insert(0, os.path.join(os.getcwd(), "docker-compose.yaml"))
#     entry_compose.grid(row=2, column=1, sticky="w", padx=5, pady=5)
#     btn_browse = ctk.CTkButton(input_frame, text="Procurar", command=lambda: escolher_compose_path(entry_compose))
#     btn_browse.grid(row=2, column=2, sticky="w", padx=5, pady=5)

#     ctk.CTkLabel(input_frame, text="Cenário:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
#     scenario_var = ctk.StringVar(value="Atualizar Dockerfile localmente")
#     scenario_frame = ctk.CTkFrame(input_frame)
#     scenario_frame.grid(row=3, column=1, sticky="w", padx=5, pady=5)
#     cenarios = ["Atualizar Dockerfile localmente", "Push para Docker Hub", "Deploy Remoto via SSH"]
#     radio_buttons = []
#     for i, c in enumerate(cenarios):
#         rb = ctk.CTkRadioButton(scenario_frame, text=c, variable=scenario_var, value=c)
#         rb.grid(row=i, column=0, sticky="w", padx=5, pady=2)
#         radio_buttons.append(rb)

#     progress_frame = ctk.CTkFrame(tab_deploy)
#     progress_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
#     progress_frame.grid_columnconfigure(0, weight=1)
#     deploy_progress_label = ctk.CTkLabel(progress_frame, text="Aguardando início")
#     deploy_progress_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
#     deploy_progress_bar = ctk.CTkProgressBar(progress_frame, width=400)
#     deploy_progress_bar.grid(row=1, column=0, sticky="ew", padx=5, pady=2)

#     log_frame = ctk.CTkFrame(tab_deploy)
#     log_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
#     log_frame.grid_columnconfigure(0, weight=1)
#     log_frame.grid_rowconfigure(0, weight=1)
#     log_text_deploy = ctk.CTkTextbox(log_frame, height=200, state="disabled")
#     log_text_deploy.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

#     footer_frame = ctk.CTkFrame(tab_deploy)
#     footer_frame.grid(row=4, column=0, sticky="w", padx=10, pady=10)
#     btn_executar_deploy = ctk.CTkButton(footer_frame, text="Executar Deploy")
#     btn_executar_deploy.grid(row=0, column=0, sticky="w", padx=5)
#     btn_config = ctk.CTkButton(footer_frame, text="Configurar .env", command=lambda: open_config_window(app, log_text_deploy))
#     btn_config.grid(row=0, column=1, sticky="w", padx=5)
#     btn_clear_deploy = ctk.CTkButton(footer_frame, text="Limpar Log", command=lambda: log_text_deploy.configure(state="normal") or log_text_deploy.delete(1.0, ctk.END) or log_text_deploy.configure(state="disabled"))
#     btn_clear_deploy.grid(row=0, column=2, sticky="w", padx=5)

#     # Cleanup Tab
#     tab_cleanup.grid_columnconfigure(0, weight=1)
#     tab_cleanup.grid_rowconfigure(1, weight=1)

#     ctk.CTkLabel(tab_cleanup, text="Limpeza Geral", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)

#     log_frame = ctk.CTkFrame(tab_cleanup)
#     log_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
#     log_frame.grid_columnconfigure(0, weight=1)
#     log_frame.grid_rowconfigure(0, weight=1)
#     log_text_cleanup = ctk.CTkTextbox(log_frame, height=300, state="disabled")
#     log_text_cleanup.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

#     footer_frame = ctk.CTkFrame(tab_cleanup)
#     footer_frame.grid(row=2, column=0, sticky="w", padx=10, pady=10)
#     btn_limpeza_local = ctk.CTkButton(footer_frame, text="Limpeza Local")
#     btn_limpeza_local.grid(row=0, column=0, sticky="w", padx=5)
#     btn_limpeza_remota = ctk.CTkButton(footer_frame, text="Limpeza Remota")
#     btn_limpeza_remota.grid(row=0, column=1, sticky="w", padx=5)
#     btn_clear_cleanup = ctk.CTkButton(footer_frame, text="Limpar Log", command=lambda: log_text_cleanup.configure(state="normal") or log_text_cleanup.delete(1.0, ctk.END) or log_text_cleanup.configure(state="disabled"))
#     btn_clear_cleanup.grid(row=0, column=2, sticky="w", padx=5)

#     # Deploy All Tab
#     tab_deploy_all.grid_columnconfigure(0, weight=1)
#     tab_deploy_all.grid_rowconfigure(3, weight=1)

#     ctk.CTkLabel(tab_deploy_all, text="Deploy de Todos os Containers", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)

#     input_frame = ctk.CTkFrame(tab_deploy_all)
#     input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
#     input_frame.grid_columnconfigure(1, weight=1)

#     ctk.CTkLabel(input_frame, text="Branch:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
#     branch_var = ctk.StringVar(value="homolog")
#     # branch_combo_all = ctk.CTkComboBox(input_frame, textvariable=branch_var, values=["homolog", "master"], width=300)
#     branch_combo_all = ctk.CTkComboBox(input_frame, variable=branch_var, values=["homolog", "master"], width=300)
#     branch_combo_all.grid(row=0, column=1, sticky="w", padx=5, pady=5)

#     ctk.CTkLabel(input_frame, text="Docker Compose:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
#     entry_compose_all = ctk.CTkEntry(input_frame, width=300)
#     entry_compose_all.insert(0, os.path.join(os.getcwd(), "docker-compose.yaml"))
#     entry_compose_all.grid(row=1, column=1, sticky="w", padx=5, pady=5)
#     btn_browse_all = ctk.CTkButton(input_frame, text="Procurar", command=lambda: escolher_compose_path(entry_compose_all))
#     btn_browse_all.grid(row=1, column=2, sticky="w", padx=5, pady=5)

#     progress_frame = ctk.CTkFrame(tab_deploy_all)
#     progress_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
#     progress_frame.grid_columnconfigure(0, weight=1)
#     deploy_all_progress_label = ctk.CTkLabel(progress_frame, text="Aguardando início")
#     deploy_all_progress_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
#     deploy_all_progress_bar = ctk.CTkProgressBar(progress_frame, width=400)
#     deploy_all_progress_bar.grid(row=1, column=0, sticky="ew", padx=5, pady=2)

#     log_frame = ctk.CTkFrame(tab_deploy_all)
#     log_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
#     log_frame.grid_columnconfigure(0, weight=1)
#     log_frame.grid_rowconfigure(0, weight=1)
#     log_text_deploy_all = ctk.CTkTextbox(log_frame, height=200, state="disabled")
#     log_text_deploy_all.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

#     footer_frame = ctk.CTkFrame(tab_deploy_all)
#     footer_frame.grid(row=4, column=0, sticky="w", padx=10, pady=10)
#     btn_executar_local = ctk.CTkButton(footer_frame, text="Deploy Local")
#     btn_executar_local.grid(row=0, column=0, sticky="w", padx=5)
#     btn_executar_remote = ctk.CTkButton(footer_frame, text="Deploy Remoto")
#     btn_executar_remote.grid(row=0, column=1, sticky="w", padx=5)
#     btn_config_all = ctk.CTkButton(footer_frame, text="Configurar .env", command=lambda: open_config_window(app, log_text_deploy_all))
#     btn_config_all.grid(row=0, column=2, sticky="w", padx=5)
#     btn_clear_deploy_all = ctk.CTkButton(footer_frame, text="Limpar Log", command=lambda: log_text_deploy_all.configure(state="normal") or log_text_deploy_all.delete(1.0, ctk.END) or log_text_deploy_all.configure(state="disabled"))
#     btn_clear_deploy_all.grid(row=0, column=3, sticky="w", padx=5)

#     # Button and Entry Management
#     all_buttons = [
#         btn_executar_compile, btn_clear_compile, btn_executar_deploy, btn_config, btn_clear_deploy,
#         btn_limpeza_local, btn_limpeza_remota, btn_clear_cleanup, btn_executar_local, btn_executar_remote,
#         btn_config_all, btn_clear_deploy_all, btn_browse, btn_browse_all, diretorio_button
#     ]
#     compile_entries = [diretorio_entry, branch_combo, banco_combo, origem_combo, compilacao_combo, branch_origem_combo]
#     deploy_entries = [entry_project, entry_branch, entry_compose] + radio_buttons
#     deploy_all_entries = [branch_combo_all, entry_compose_all]

#     # Button Commands
#     def with_timeout(func, args, queue, log_widget):
#         completion_event = threading.Event()
#         def wrapper():
#             try:
#                 func(*args)
#             except Exception as e:
#                 add_log(f"[ERRO] Erro inesperado: {e}", log_widget, app)
#                 queue.put(('finish', 'Processo concluído com erros', 100))
#             finally:
#                 completion_event.set()
#         thread = threading.Thread(target=wrapper, daemon=True)
#         thread.start()
#         if not completion_event.wait(timeout=600):
#             add_log("[ERRO] Tempo limite excedido. Processo interrompido.", log_widget, app)
#             queue.put(('finish', 'Processo concluído com erros', 100))

#     btn_executar_compile.configure(command=lambda: with_timeout(
#         executar_compilacao,
#         (
#             diretorio_entry.get().strip(),
#             branch_combo.get().strip(),
#             banco_combo.get().strip(),
#             origem_combo.get().strip(),
#             compilacao_combo.get().strip(),
#             branch_origem_combo.get().strip(),
#             lambda msg: add_log(msg, log_text_compile, app),
#             compile_queue
#         ),
#         compile_queue,
#         log_text_compile
#     ))

#     btn_executar_deploy.configure(command=lambda: with_timeout(
#         executar_deploy,
#         (
#             entry_project.get().strip(),
#             entry_branch.get().strip(),
#             entry_compose.get().strip(),
#             scenario_var.get(),
#             deploy_queue,
#             lambda msg: add_log(msg, log_text_deploy, app)
#         ),
#         deploy_queue,
#         log_text_deploy
#     ))

#     btn_limpeza_local.configure(command=lambda: with_timeout(
#         executar_limpeza_geral,
#         (
#             True,
#             cleanup_queue,
#             lambda msg: add_log(msg, log_text_cleanup, app)
#         ),
#         cleanup_queue,
#         log_text_cleanup
#     ))

#     btn_limpeza_remota.configure(command=lambda: with_timeout(
#         executar_limpeza_geral,
#         (
#             False,
#             cleanup_queue,
#             lambda msg: add_log(msg, log_text_cleanup, app)
#         ),
#         cleanup_queue,
#         log_text_cleanup
#     ))

#     btn_executar_local.configure(command=lambda: with_timeout(
#         executar_deploy_todos,
#         (
#             True,
#             branch_var.get().strip(),
#             entry_compose_all.get().strip(),
#             deploy_all_queue,
#             lambda msg: add_log(msg, log_text_deploy_all, app)
#         ),
#         deploy_all_queue,
#         log_text_deploy_all
#     ))

#     btn_executar_remote.configure(command=lambda: with_timeout(
#         executar_deploy_todos,
#         (
#             False,
#             branch_var.get().strip(),
#             entry_compose_all.get().strip(),
#             deploy_all_queue,
#             lambda msg: add_log(msg, log_text_deploy_all, app)
#         ),
#         deploy_all_queue,
#         log_text_deploy_all
#     ))

#     # Helper function to select project directory and update branches
#     def selecionar_diretorio_projeto(entry, branch_combo, executar_btn):
#         """Select project directory and update branch dropdown."""
#         diretorio = filedialog.askdirectory(title="Selecione o diretório do projeto")
#         if diretorio:
#             entry.delete(0, ctk.END)
#             entry.insert(0, diretorio)
#             executar_btn.configure(state="normal")
#             try:
#                 atualizar_branches(diretorio, branch_combo, lambda msg: add_log(msg, log_text_compile, app))
#             except Exception as e:
#                 add_log(f"[ERRO] Falha ao atualizar branches: {e}", log_text_compile, app)

#     # Start queue processing for each tab
#     processar_fila(app, compile_queue, log_text_compile, compile_progress_bar, compile_progress_label, all_buttons, compile_entries + deploy_entries + deploy_all_entries, notebook)
#     processar_fila(app, deploy_queue, log_text_deploy, deploy_progress_bar, deploy_progress_label, all_buttons, compile_entries + deploy_entries + deploy_all_entries, notebook)
#     processar_fila(app, cleanup_queue, log_text_cleanup, None, None, all_buttons, compile_entries + deploy_entries + deploy_all_entries, notebook)
#     processar_fila(app, deploy_all_queue, log_text_deploy_all, deploy_all_progress_bar, deploy_all_progress_label, all_buttons, compile_entries + deploy_entries + deploy_all_entries, notebook)

#     # Load environment variables
#     load_dotenv(ENV_FILE)

#     # Run the application
#     app.mainloop()

# if __name__ == "__main__":
#     main()