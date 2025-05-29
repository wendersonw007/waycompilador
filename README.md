# Way Compilador

Aplicação para compilação e configuração de projetos Java com Maven.

## Funcionalidades

- Configuração de JAVA_HOME e MAVEN_HOME
- Cadastro de origens de banco de dados
- Cadastro de nomes de banco de dados
- Compilação de projetos com diferentes configurações

## Arquivos Principais

### 1. Configuração

- **config.py**: Configurador original com todas as funcionalidades
- **config_simplificado.py**: Nova interface simplificada com abas para melhor organização
- **config_melhorado.py**: Versão intermediária com melhorias na interface

### 2. Aplicação

- **app_funcionando.py**: Aplicação principal original

### 3. Teste

- **testar_config.py**: Script para testar a configuração e a aplicação

## Como Usar

### Configuração Completa

Para usar a interface completa:

```bash
python config.py
```

A interface possui três abas:
1. **Java/Maven**: Configuração dos diretórios JAVA_HOME e MAVEN_HOME
2. **Origem do Banco**: Cadastro de origens de banco de dados
3. **Nome do Banco**: Cadastro de nomes de banco de dados

### Configuração Simplificada

Para usar a nova interface simplificada:

```bash
python config_simplificado.py
```

A interface possui as mesmas três abas, porém com visual mais simples.

### Aplicação Completa

Para usar a aplicação principal:

```bash
python app_funcionando.py
```

### Teste

Para testar a configuração e a aplicação:

```bash
python testar_config.py
```

## Melhorias Implementadas

1. **Carregamento Dinâmico de Configurações**
   - Carregamento automático das configurações do arquivo .env
   - Recarregamento antes de usar os valores selecionados

2. **Geração Automática de IDs**
   - IDs gerados automaticamente para origens e bancos
   - Não é mais necessário informar o ID manualmente

3. **Interface Simplificada**
   - Organização em abas para melhor separação das configurações
   - Listagem simples dos bancos e origens cadastrados
   - Atualização imediata após cadastro de novos itens

4. **Integração com Aplicação Principal**
   - Botões para abrir a configuração diretamente da aplicação principal
   - Recarregamento automático das configurações

## Configurações

As configurações são salvas no arquivo `.env` no seguinte formato:

```
JAVA_HOME=/caminho/para/java
MAVEN_HOME=/caminho/para/maven

DB_1_IP=127.0.0.1
DB_1_PORTA=3306
DB_1_USER=root
DB_1_PASS=root
DB_1_NOME=Banco Local

BANCO_1=waybe
BANCO_1_NOME=Waybe
```

## Requisitos

- Python 3.6+
- customtkinter
- PIL (Pillow)
- python-dotenv