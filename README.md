# ConverterUI

ConverterUI é uma aplicação desenvolvida em Python para converter arquivos Excel (.xls, .xlsx) para um banco de dados SQL Server. A aplicação utiliza bibliotecas como `flet`, `pandas`, `sqlalchemy` e `pyodbc`.

## Requisitos

Para instalar as dependências necessárias, execute:
```sh
pip install -r requirements.txt
```

## Estrutura do Projeto

- `ConverterUI/requirements.txt`: Lista de dependências do projeto.
- `ConverterUI/conversor.spec`: Arquivo de especificação para PyInstaller, para quem desejar ter um `.exe`.
- `ConverterUI/.gitignore`: Arquivo para ignorar arquivos e diretórios no Git.
- `ConverterUI/pyproject.toml`: Arquivo de configuração do projeto.
- `ConverterUI/src/converter.py`: Código principal da lógica de conversão.
- `ConverterUI/src/main.py`: Interface gráfica da aplicação utilizando Flet.

## Uso

Para iniciar a aplicação, execute:
```sh
python src/main.py
```
ou
```sh
flet run main.py
```

## Funcionalidades

- Adicionar servidores SQL Server.
- Carregar informações de login e servidores adicionados salvos.
- Converter arquivos Excel para tabelas no SQL Server.
- Suporte para adicionar zeros à esquerda em colunas específicas.