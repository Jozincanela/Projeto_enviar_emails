import sqlite3 as sq
from random import randint

class CRUD:
    # Método construtor/inicializador
    def __init__(self, endereco_banco: str):

        self.endereço_banco = endereco_banco
        
    def selecionar_colunas(self, nome_tabela:str, nome_colunas :str):
        """
        seleciona todos os dados de uma coluna específica

        Variaveis:
            nome_tabela (str) :"nome_da_tabela"
            nome_colunas (str): "'coluna', 'coluna'..."
        Returns:
            lista: [(dado,), (dado,), (dado,), (dado,), (dado,)]
        """
        
        banco =  sq.connect(self.endereço_banco)
        cursor = banco.cursor()
        
        
        dados_coluna = cursor.execute(f"SELECT {nome_colunas} FROM {nome_tabela}").fetchall()

        banco.commit()
        banco.close()
        return dados_coluna
    
    def nova_tabela(self,nome_tabela: str, nome_coluna_e_tipo:str , tipo_de_tabela:int):
        """
        Cria uma tabela no banco de dados que não existe  \n
        
        Variaveis:
            nome_tabela (str): "nome_da_tabela"
            nome_coluna_e_tipo (str): "coluna1 TIPO, coluna2 TIPO, coluna3 TIPO, ..."\n
            
        Tipos:
            INTEGER, REAL, TEXT
        """
        
        banco =  sq.connect(self.endereço_banco)
        cursor = banco.cursor()
        if tipo_de_tabela == 0:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {nome_tabela}(CHAVE TEXT,{nome_coluna_e_tipo})")
        elif  tipo_de_tabela == 1:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {nome_tabela}({nome_coluna_e_tipo})")
        banco.commit()
        banco.close()
           
           
    def Tabelas(self):
        """mostra os nomes das tabelas presentes no banco de dados
        """
        banco =  sq.connect(self.endereço_banco)
        cursor = banco.cursor()
        tabelas = cursor.execute("SELECT name FROM sqlite_master  WHERE type='table'").fetchall()
        return tabelas
        
    def selecionar_linhas(self, nome_tabela:str, id: int):
        """
        seleciona todas as linhas (id = 0) ou seleciona a linha desejada atravez do id

        Variaveis:
            nome_tabela (str) :"nome_da_tabela"
            id (int): id da linha

        Returns:
            se id = 0 :  todas as linhas retornará uma lista com todas as linhas
            senão id != 0 : a linha descrita no id
        """
        banco =  sq.connect(self.endereço_banco)
        cursor = banco.cursor()
        linhas = []
        for linha in cursor.execute(f"SELECT * FROM {nome_tabela} ").fetchall():
            linhas.append(linha)
        if id != 0:
                return linhas[id-1]
        else :            
            return linhas
        
    def nome_colunas(self, nome_tabela:str):
        """
        possibilita a visualização das colunas da tabela

        Variaveis:
            nome_tabela (str) :"nome_da_tabela"
        Returns:
            _type_: Lista
            
        """
        banco =  sq.connect(self.endereço_banco)
        cursor = banco.cursor()
        cursor.execute(f"PRAGMA table_info({nome_tabela})")
        colunas = cursor.fetchall()
        nomes_das_colunas = [coluna[1] for coluna in colunas]
        return nomes_das_colunas
    



    def inserir_dados(self, nome_tabela: str, nome_coluna:str ,valores: str, tipo_da_tabela:int):
        """ 
        Adiciona valores para a tabela 
        
        Variaveis:
            nome_tabela (str): "nome_da_tabela"
            nome_coluna (str): nome_coluna = "'coluna1, coluna2, coluna3 ...'"
            valores (str): "'valor_respeitando_tipo_estipulado1', 'valor_respeitando_tipo_estipulado2', 'valor_respeitando_tipo_estipulado3'..."
        """

        chave =  ""
        banco =  sq.connect(self.endereço_banco)
        cursor = banco.cursor()
        for i in range(0, 9):
            chave+= str(randint(0,9))

        if tipo_da_tabela == 0:
            cursor.execute(f"INSERT INTO {nome_tabela}(CHAVE ,{nome_coluna}) VALUES ({chave},{valores})")
        elif tipo_da_tabela == 1:
                cursor.execute(f"INSERT INTO {nome_tabela}({nome_coluna}) VALUES ({valores})")
        banco.commit()
        banco.close()
        
    def ler_dados_tabela(self, nome_tabela:str):
        """        
        Le todos os dados da tabela seguindo a seguinte formatação
        Variaveis:
            nome_tabela (str): "nome_da_tabela"
        """
        
        banco =  sq.connect(self.endereço_banco)
        cursor = banco.cursor()
        print(cursor.execute(f"SELECT * FROM {nome_tabela} ").fetchall())
        banco.commit()
        banco.close()

    def ler_dado_id(self,nome_tabela:str, id: int):
        """        
        Ler uma linha de uma tabela especifica atravez do id ultilizando a seguinte formatação \n
        Variaveis:
            nome_tabela (str): "nome_da_tabela"
            id (int): numero da linha
        """
        banco =  sq.connect(self.endereço_banco)
        cursor = banco.cursor()
        nometabela = nome_tabela
        coluna = CRUD.nome_colunas(self,nometabela)[0]
        valor = CRUD.selecionar_linhas(self,nometabela, id)[0]
        
        informacoes = cursor.execute(f"SELECT * FROM {nome_tabela} WHERE {coluna}='{valor}'").fetchall()


        banco.commit()
        banco.close()
        return informacoes
        

    def atualizar_dados(self, nome_tabela:str, id:int, Coluna_com_Novo_valor: str):
        """        
        Atualiza dados de uma linha da tabela ultilizando a seguinte formatação\n


        Variaveis:
            nome_tabela (str): "nome_da_tabela"
            id (int): numero da linha
            Coluna_com_Novo_valor (str): "coluna1= 'novo valor'"
        """ 

        banco =  sq.connect(self.endereço_banco)
        cursor = banco.cursor()
        
        coluna = CRUD.nome_colunas(nome_tabela)[0]
        valor = CRUD.selecionar_linhas(nome_tabela, id)[0]
        
        cursor.execute(f"UPDATE {nome_tabela} SET {Coluna_com_Novo_valor} WHERE {coluna}='{valor}'")
        banco.commit()
        banco.close()
        
    def atualizar_dados_por_chave(self, nome_tabela:str, chave:str, Coluna_com_Novo_valor: str):
        """        
        Atualiza dados de uma linha da tabela ultilizando a seguinte formatação\n


        Variaveis:
            nome_tabela (str): "nome_da_tabela"
            chave (str): chave
            Coluna_com_Novo_valor (str): "coluna1= 'novo valor'"
        """ 

        banco =  sq.connect(self.endereço_banco)
        cursor = banco.cursor()
        
        
        cursor.execute(f"UPDATE {nome_tabela} SET {Coluna_com_Novo_valor} WHERE CHAVE ='{chave}'")
        banco.commit()
        banco.close()

    def apagar_dados_linha(self, nome_tabela:str, id: int):
        """
        Apaga dados de uma linha especifica

        Args:
            nome_tabela (str): "nome_da_tabela"
            id (int): numero da linha
        """

        banco =  sq.connect(self.endereço_banco)
        cursor = banco.cursor()
        
    
        coluna = CRUD.nome_colunas(nome_tabela)[0]
        valor = CRUD.selecionar_linhas(nome_tabela, id)[0]

        cursor.execute(f"DELETE FROM {nome_tabela} WHERE {coluna} = {valor}")
        banco.commit()        
        banco.close()
        
    def apagar_dados_linha_chave(self, nome_tabela:str, chave: str):
        """
        Apaga dados de uma linha especifica

        Args:
            nome_tabela (str): "nome_da_tabela"
            id (int): numero da linha
        """

        banco =  sq.connect(self.endereço_banco)
        cursor = banco.cursor()
        
        cursor.execute(f"DELETE FROM {nome_tabela} WHERE CHAVE = {chave}")
        banco.commit()        
        banco.close()
        
    
    def reset (self, nome_da_tabela:str):
        """        
        Apagará todos os dados de uma tabela mas mantem as respectivas colunas ultilizando a seguinte formatação
        Args:
            nome_da_tabela (str): "nome_da_tabela"
        """

        banco =  sq.connect(self.endereço_banco)
        cursor = banco.cursor()
        cursor.execute(f"DELETE FROM {nome_da_tabela}")
        banco.commit()  
        banco.close() 
    
    def apagar_tabela (self, nome_da_tabela:str):
        """
        Apagará a tabela do banco de dados

        Args:
            nome_da_tabela (str): "nome_da_tabela"
        """
        
        banco =  sq.connect(self.endereço_banco)
        cursor = banco.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {nome_da_tabela}")
        banco.commit()  
        banco.close() 