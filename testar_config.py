import os
import subprocess
import sys

def main():
    """
    Script para testar a configuração simplificada.
    Permite escolher entre executar o configurador ou a aplicação principal.
    """
    print("=== TESTE DE CONFIGURAÇÃO SIMPLIFICADA ===")
    print("1. Executar configurador (config_simplificado.py)")
    print("2. Executar aplicação principal (app_simplificado.py)")
    print("3. Sair")
    
    escolha = input("Escolha uma opção (1-3): ")
    
    if escolha == "1":
        print("\nExecutando configurador simplificado...")
        subprocess.run([sys.executable, "config_simplificado.py"])
    elif escolha == "2":
        print("\nExecutando aplicação principal com configuração simplificada...")
        subprocess.run([sys.executable, "app_simplificado.py"])
    elif escolha == "3":
        print("\nSaindo...")
        return
    else:
        print("\nOpção inválida!")
    
    # Após a execução, pergunta se deseja continuar
    continuar = input("\nDeseja continuar testando? (s/n): ")
    if continuar.lower() == "s":
        main()

if __name__ == "__main__":
    main()