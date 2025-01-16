from sqlalchemy import NVARCHAR, create_engine
import pandas as pd
import os, glob, pickle

class Conversor:
    def __init__(self):
        self.serverList = []
        self.zerosToAdd = 0

    def add_server(self, server):
        self.serverList.append(server)
        self.save_login_server_information()
        return "Servidor Adicionado!"

    def load_datas(self):
        try:
            server, username = self.load_login_server_information()
            return server, username
        except Exception:
            return [], ""

    def set_first_server(self, server):
        index = self.serverList.index(server)
        self.serverList[0], self.serverList[index] = self.serverList[index], self.serverList[0]
    
    def get_directory_files(self, directory_path):
        directory_file_pattern = os.path.join(directory_path, "*.xls*")
        return glob.glob(directory_file_pattern)

    def converter(self, server, database, username, password, issue_Key, is_Local_Database, enable_Leading_Zero_Padding, padding_Columns, padding_Zero_Count):
        try:
            files = self.get_directory_files(self.get_default_directory())
            if len(files) == 0:
                return "No diretório escolhido não existe arquivos .xls ou .xlsx."
            
            self.set_first_server(server)

            if is_Local_Database:
                if database != "" and server != "":
                    connection_string = f"mssql+pyodbc://{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
                else:
                    return "Preencha os campos Servidor e Banco!"
            else:
                if server != "" and database != "" and username != "" and password != "":
                    connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
                else:
                    return "Preencha todos os campos!"
            
            self.save_login_server_information(username)
            conn = create_engine(connection_string)

            for arquivo in files:
                xls = pd.ExcelFile(arquivo)
                for sheet_name in xls.sheet_names:
                    df = xls.parse(sheet_name, dtype=str)
                    if enable_Leading_Zero_Padding:
                        for column in padding_Columns:
                            if column in df.columns:
                                df[column] = df[column].apply(self.fill_zeros, quantidadeZeros=padding_Zero_Count)
                            else:
                                print(f"A coluna {padding_Columns} não foi encontrada no DataFrame.")
                    nomeTabela = issue_Key + "_" + sheet_name.replace(' ', '_')
                    df.to_sql(nomeTabela, conn, schema='tmp', if_exists='replace', index=False, dtype={col: NVARCHAR for col in df.columns})

            return "Conversão realizada com sucesso"
        except Exception as e:
            print("Ocorreu um erro durante a execução do aplicativo!")
            print(str(e))
            raise ValueError("Ocorreu um erro durante a execução do código \n"
                    "Verifique:\n\n"
                    "  - O nome do Servidor\n"
                    "  - O nome do Banco de dados\n"
                    "  - O nome de Usuario\n"
                    "  - A senha\n"
                    "  - Se o nome do SP está preenchido\n\n"
                    "Obs: Caso esteja utilizado um Banco de dados local, os campos Usuario e senha não precisam estar preenchidos\n\n"
                    f"  - Exceção encontrada: {str(e)}")

    def save_login_server_information(self, username=""):
        if not os.path.exists(".login"):
            os.mkdir('.login')
        with open(".login/login_data.pkl", "wb") as f:
            login_data = {"server": self.serverList, "username": username}
            pickle.dump(login_data, f)

    def load_login_server_information(self):
        try:
            with open(".login/login_data.pkl", "rb") as f:
                login_data = pickle.load(f)
                self.serverList = login_data["server"]
                return login_data["server"], login_data["username"]
        except FileNotFoundError:
            return [], ""
        
    def get_quantidade_zeros(self):
        return self.zerosToAdd
    
    def fill_zeros(self, value, quantidadeZeros):
        if isinstance(value, int) or isinstance(value, float):
            return str(int(value)).zfill(quantidadeZeros)
        return value

    def get_default_directory(self):
        diretorio_base = os.path.expanduser("~")
        diretorio = os.path.join(diretorio_base, "Downloads/_imports")
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
        return diretorio