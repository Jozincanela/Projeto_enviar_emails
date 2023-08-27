from tkinter import *
from tkinter import ttk
from bd_poo import CRUD
'''Criando Janela Tkinter'''
Janela_main = Tk()
Janela_main.title("Main")

'''Criando uma tabela no Banco de dados'''
Cadastro = CRUD("banco_projeto_email.db")
Cadastro.nova_tabela("Cadastros", "Nome TEXT, Sobrenome TEXT, Email TEXT",0)
Tabela_cadastro = "Cadastros"
colunas_cadastro = "Nome, Sobrenome, Email"




def pagina_Cadastrar():
    janela_cadastro  = Tk()
    janela_cadastro.title("Cadastro")
    
    
    def volta_main ():
        Janela_main.deiconify()
        janela_cadastro.destroy()


    def cadastrar_email() -> str:
        nome = Nome.get()
        sobrenome = Sobrenome.get()
        email = Email.get()
        valores = f"'{nome}','{sobrenome}','{email}'"
        Cadastro.inserir_dados(Tabela_cadastro, colunas_cadastro, valores, 0)

        
        Nome.delete(0, END)
        Sobrenome.delete(0, END)
        Email.delete(0, END)
        
        texto = "email cadastrado!"
        texto_confirmacao["text"] = texto
        


    texto_orientacao = Label(janela_cadastro, text= "Bem vindo ao cadastro de emails!!")
    texto_orientacao.grid(column=0, row= 0, padx=15, pady= 5, columnspan=3)




    Nome = Entry(janela_cadastro)
    Nome.grid(column= 0, row= 3, padx=15)
    texto_Nome = Label(janela_cadastro, text= "Nome")
    texto_Nome.grid(column=0, row= 2, padx=15)




    Sobrenome = Entry(janela_cadastro)
    Sobrenome.grid(column= 1, row= 3, padx=15)
    texto_Sobrenome = Label(janela_cadastro, text= "Sobrenome")
    texto_Sobrenome.grid(column=1, row= 2, padx=15, pady= 5)




    Email = Entry(janela_cadastro, text="Email", width= 40 )
    Email.grid(column=0, row=5, columnspan=3)
    texto_Email = Label(janela_cadastro, text= "Email")
    texto_Email.grid(column=0, row= 4, padx=15, pady= 5,columnspan=3)




    texto_confirmacao = Label(janela_cadastro, text = "")
    texto_confirmacao.grid(column=0,row=6 ,columnspan=3)




    botao_confirm = Button(janela_cadastro, text="confirma", command=cadastrar_email)
    botao_confirm.grid(column= 0, row=7, pady= 10,columnspan=3)
    
    botao_voltar = Button(janela_cadastro, text="Voltar", command=volta_main)
    botao_voltar.grid(column= 0, row=8, pady= 10,columnspan=3)
    
    
    Janela_main.iconify()
    janela_cadastro.mainloop()


def gerenciamento_emails():
    Janela_gerenciamento = Tk()
    Janela_gerenciamento.title("Gerenciamento emails")

    Janela_main.iconify()

    def Fechar():
        Janela_main.deiconify
        Janela_gerenciamento.destroy()
        
    def deletar_usuario():
        Janela_gerenciamento.iconify()
        Janela_delete_usu = Tk()
        
        def Fechar():
            Janela_gerenciamento.deiconify()
            Janela_delete_usu.destroy()
        
        def Entrys_del():
            try:
                chave_pessoa = list(Cadastro.ler_dado_id("Teste1", int(ID_usuario.get()))  [0])[0]
                for tabelas in str(Cadastro.Tabelas()).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("[","").replace("]", "").split(" "):
                
                    Cadastro.apagar_dados_linha_chave(tabelas, chave_pessoa)
            except:
                pass
            Confirma_salvamento = Label(Janela_delete_usu, text="Usuario Deletado!")
            Confirma_salvamento.grid(row=1, column=0, columnspan=4)
        
        ID_usuario_instrucao =  Label(Janela_delete_usu, text="ID")
        ID_usuario_instrucao.grid(row=0, column=0)
        ID_usuario = Entry(Janela_delete_usu, width=15)
        ID_usuario.grid(row=0, column=1, columnspan=1)
        confirma_id = Button(Janela_delete_usu, text="confirma", command=Entrys_del)
        confirma_id.grid(row=0, column=2)
        botao_fechar =  Button(Janela_delete_usu,text="Voltar", command=Fechar)
        botao_fechar.grid(row=2, column=0, columnspan=4)
        
        Janela_delete_usu.mainloop()
        
    def deletar_lista():
        Janela_Deletar_lista =  Tk()
        Janela_Deletar_lista.title("Deletar lista")
        Janela_gerenciamento.iconify()
        
        def Fechar_Janela_Deletar_lista():

            Janela_gerenciamento.deiconify()
            Janela_Deletar_lista.destroy()
        def apagar_lista():
            try:
                lista_apagada = lista_tabelas [int(escolha_id.get()) -  1]
                if int(escolha_id.get()) - 1  == 0:
                    texto_conclusao['text'] =  "Não é permitido excluir a tabela mãe"
                else :

                        Cadastro.apagar_tabela(lista_apagada)
                        texto_conclusao['text'] =  f"Tabela {lista_apagada} deletada do banco de dados"
            except:
                texto_conclusao['text'] =  f"Não foi possivel deletar a Tabela do banco de dados"
                pass
                    
        
        


        lista_id = []
        global Nomes_das_listas
        Nomes_das_listas = []
        lista_tabelas = Cadastro.Tabelas()
        tabela_listas = ttk.Treeview(Janela_Deletar_lista, columns=("id" ,"Nome da Lista"), show="headings")
        tabela_listas.column('id' ,minwidth=0, width=50)
        tabela_listas.column('Nome da Lista' ,minwidth=0, width=150)
        tabela_listas.heading('id', text="ID")
        tabela_listas.heading('Nome da Lista', text="NOME DA LISTA")
        tabela_listas.grid(row= 1, column=1, columnspan= 3)

        for labels in range  (0, len(lista_tabelas)):
            lista_tabelas[labels] = str(lista_tabelas[labels]).replace("'", " ").replace("(", "").replace(")", "").replace(",","").replace(" ","")

        for itens in range (1, len(lista_tabelas)+1):
            lista_id.append(itens)

        for i in range(0,len(lista_tabelas)):
            tabela_listas.insert("", "end",values=(lista_id[i], lista_tabelas[i]))
            
        instrução =  Label(Janela_Deletar_lista, text="Id da lista de emails")
        instrução.grid( row=2, column=1, columnspan=3)

        escolha_id = Entry(Janela_Deletar_lista)
        escolha_id.grid(row=3, column=1, columnspan=3)

        botao_escolher_msg = Button(Janela_Deletar_lista, text="Apagar", command= apagar_lista)
        botao_escolher_msg.grid(row=4, column=1, columnspan=3)
        
        texto_conclusao =  Label(Janela_Deletar_lista, text="")
        texto_conclusao.grid(row=6,column=1,columnspan=3 )
        
        
        botao_sair_Janela_Deletar_lista = Button(Janela_Deletar_lista, text="Voltar", command= Fechar_Janela_Deletar_lista)
        botao_sair_Janela_Deletar_lista.grid(row=5, column=1, columnspan=3)
            
        Janela_Deletar_lista.mainloop()

    def mudar_cadastros():
        Janela_gerenciamento.iconify()
        Janela_Update = Tk()
        Janela_Update.title("Update usuarios")
        

        def Fechar():
            Janela_gerenciamento.deiconify()
            Janela_Update.destroy()
        
        def Salvar():
            Novo_nome.get()
            Novo_sobrenome.get()
            Novo_Email.get()
            chave_pessoa = list(Cadastro.ler_dado_id("Teste1", int(ID_usuario.get()))  [0])[0]
            for tabela in str(Cadastro.Tabelas()).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("[","").replace("]", "").split(" "):
                atualizacao = f"Nome='{Novo_nome.get()}', Sobrenome='{Novo_sobrenome.get()}', Email='{Novo_Email.get()}'"
                try:
                    Cadastro.atualizar_dados_por_chave(tabela,chave_pessoa,atualizacao )
                except:
                    pass
                
            Confirma_salvamento = Label(Janela_Update, text="Usuario modificado!")
            Confirma_salvamento.grid(row=9, column=0, columnspan=4)
            

            
            
        def Entrys_up ():
            id_escolhido = ID_usuario.get()
            slecionado_nao_tratado = Cadastro.selecionar_linhas(Tabela_cadastro,int(id_escolhido))
            slecionado_nao_tratado = str(slecionado_nao_tratado).replace("(", "").replace(")", "").replace(" ","").replace("'", "")
            informacoes_usuario = slecionado_nao_tratado.split(",")
            
            
            
            Novo_nome.delete(0, END)
            Novo_sobrenome.delete(0,END)
            Novo_Email.delete(0, END)
            
            Novo_nome.insert(0, informacoes_usuario[1])
            Novo_sobrenome.insert(0, informacoes_usuario[2])
            Novo_Email.insert(0, informacoes_usuario[3])
            
            confirma_atualizacao =  Button(Janela_Update, text="Salvar", command=Salvar)
            confirma_atualizacao.grid(row=7, column=0, columnspan=4)
            


            

            
            
            
        ID_usuario_instrucao =  Label(Janela_Update, text="ID")
        ID_usuario_instrucao.grid(row=0, column=0)
        ID_usuario = Entry(Janela_Update, width=15)
        ID_usuario.grid(row=0, column=1, columnspan=1)
        confirma_id = Button(Janela_Update, text="confirma", command=Entrys_up)
        confirma_id.grid(row=0, column=2)
        
        Novo_nome_instrucao =  Label(Janela_Update, text="Edite o nome:")
        Novo_nome_instrucao.grid(row=1, column=0, columnspan=4)
        Novo_nome = Entry(Janela_Update, width=30)
        Novo_nome.grid(row=2, column=0, columnspan=4)
        
        Novo_sobrenome_instrucao =  Label(Janela_Update, text="Edite o Sobrenome:")
        Novo_sobrenome_instrucao.grid(row=3, column=0, columnspan=4)
        Novo_sobrenome = Entry(Janela_Update, width=30)
        Novo_sobrenome.grid(row=4, column=0, columnspan=4)
        
        Novo_Email_instrucao =  Label(Janela_Update, text="Edite o Email:")
        Novo_Email_instrucao.grid(row=5, column=0, columnspan=4)
        Novo_Email = Entry(Janela_Update, width=30)
        Novo_Email.grid(row=6, column=0, columnspan=4)

        botao_fechar =  Button(Janela_Update,text="Voltar", command=Fechar)
        botao_fechar.grid(row=8, column=0, columnspan=4)

        Janela_Update.mainloop()


        
    global Nomes_das_listas
    lista_id = lista_nome_limpa = Nomes_das_listas =[]

    dados_coluna = Cadastro.selecionar_colunas(Tabela_cadastro, "Nome, Sobrenome")
    for dados in range (0, len(dados_coluna)):
        lista_de_nome = list(dados_coluna[dados])
        for i in range (0,len(lista_de_nome)-1):
            lista_de_nome[i] += " " + lista_de_nome[i+1]
            lista_de_nome[i] = str(lista_de_nome[i]).title()
            lista_de_nome.remove(lista_de_nome[i+1])
            lista_nome_limpa.append(lista_de_nome[i])


    tabela_listas = ttk.Treeview(Janela_gerenciamento, columns=("id" ,"Nome de todos usuarios"), show="headings")
    tabela_listas.column('id' ,minwidth=0, width=50)
    tabela_listas.column('Nome de todos usuarios' ,minwidth=0, width=150)
    tabela_listas.heading('id', text="ID")
    tabela_listas.heading('Nome de todos usuarios', text="NOME USUARIOS")
    tabela_listas.grid(row= 0, column=0, columnspan= 3, rowspan= 4)

    for labels in range  (0, len(lista_nome_limpa)):
        lista_nome_limpa[labels] = str(lista_nome_limpa[labels]).replace("'", " ").replace("(", "").replace(")", "").replace(",","")

    for id in range(0,len(lista_nome_limpa)):
        tabela_listas.insert("", "end",values=(id + 1, lista_nome_limpa[id]))




    botao_update = Button(Janela_gerenciamento, text="mudar cadastros", command=mudar_cadastros)
    botao_update.grid(column=4, row= 0, padx=15, pady= 0, columnspan=2)

    botao_deletar_linha = Button(Janela_gerenciamento, text="Deletar linha", command= deletar_usuario)
    botao_deletar_linha.grid(column=4, row= 1, padx=15, pady= 0, columnspan=2)

    botao_deletar_tudo = Button(Janela_gerenciamento, text="Deletar lista", command=deletar_lista)
    botao_deletar_tudo.grid(column=4, row= 2, padx=15, pady= 0, columnspan=2)
    
    botao_voltar = Button(Janela_gerenciamento, text="voltar", command=Fechar)
    botao_voltar.grid(column=4, row= 3, padx=15, pady= 5, columnspan=3)




    Janela_gerenciamento.mainloop()

def Escolher_Lista_ou_Criar():
    Janela_seleção_lista =  Tk()
    Janela_seleção_lista.title("Seleção lista")

    lista_id = []
    global Nomes_das_listas
    Nomes_das_listas = []
    lista_tabelas = Cadastro.Tabelas()

    def fechar_Janela_seleção_lista(): 
        Janela_main.deiconify()
        Janela_seleção_lista.destroy()

    def Escolher_mensagem():
        """"Fazer pag seleção e enviar emails"""
        ...
    
    def escolha_nome_lista ():
        Janela_escolha_nome =  Tk()
        Janela_escolha_nome.title("Nome da nova lista")
        def fechar_botao_voltar_Janela_escolha_nome():
            Janela_seleção_lista.deiconify()
            Janela_escolha_nome.destroy()
                    
        def seleção_usuarios():
            Janela_confirmar_emails = Tk()
            colunas = "CHAVE INTEGER, Nome TEXT, Sobrenome TEXT,Email TEXT"
            Janela_confirmar_emails.title("seleção de usuarios")
            nome_da_lista =  escolha_nome.get()
            Nomes_das_listas.append(nome_da_lista)
            Cadastro.nova_tabela(nome_da_lista, colunas, 1)
            def fechar_Janela_confirmar_emails():
                Janela_escolha_nome.deiconify()
                Janela_confirmar_emails.destroy()
            def ids_escolhidos():
                id_lista_escolhidos = escolha_id.get()
                """Criação de nova tabela"""
                """Cadastro.nova_tabela(nome_da_lista,"Chave TEXT, Nome TEXT, Sobrenome TEXT, Email TEXT", tipo_de_tabela=1 )"""

                ids = 0
                while ids <= len(id_lista_escolhidos):
                    """banco1.selecionar_linhas(nome_tabela,str(ids))"""
                    
                    slecionado_nao_tratado = Cadastro.selecionar_linhas(nome_tabela,int(id_lista_escolhidos[ids]))
                    slecionado_nao_tratado = str(slecionado_nao_tratado).replace("(", "").replace(")", "").replace(" ","")
                    Cadastro.inserir_dados(nome_da_lista,"CHAVE, Nome, Sobrenome, Email", slecionado_nao_tratado, 1)
                    ids+=2

                    """Tratamento da linha vinda do CRUD CHAVE, Nome, Sobrenome, Email"""
                

                escolha_id.delete(0, END)
                confirma["text"] = "texto"



            global lista
            lista = []
            


            nome_tabela = "Cadastros"
            lista_nome_limpa= []
            lista_id = []

            dados_coluna = Cadastro.selecionar_colunas(nome_tabela, "Nome, Sobrenome")
            for dados in range (0, len(dados_coluna)):
                lista_de_nome = list(dados_coluna[dados])
                for i in range (0,len(lista_de_nome)-1):
                    lista_de_nome[i] += " " + lista_de_nome[i+1]
                    lista_de_nome[i] = str(lista_de_nome[i]).title()
                    lista_de_nome.remove(lista_de_nome[i+1])
                    lista_nome_limpa.append(lista_de_nome[i])

            for itens in range (1, len(lista_nome_limpa)+1):
                lista_id.append(itens)


            tabela = ttk.Treeview(Janela_confirmar_emails, columns=("id" ,"Nome"), show="headings")
            tabela.column('id' ,minwidth=0, width=50)
            tabela.column('Nome' ,minwidth=0, width=150)
            tabela.heading('id', text="ID")
            tabela.heading('Nome', text="NOME")
            tabela.grid(row= 1, column=1, columnspan= 3)

            for i in range(0,len(lista_nome_limpa)):
                tabela.insert("", "end",values=(lista_id[i], lista_nome_limpa[i]))

            instrução =  Label(Janela_confirmar_emails, text="Ids das pessoas a serem enviadas")
            instrução.grid( row=2, column=1, columnspan=3)

            instrução_1 =  Label(Janela_confirmar_emails, text="1-coloque somente '0' para todos")
            instrução_1.grid( row=3, column=1, columnspan=3)

            instrução_2 =  Label(Janela_confirmar_emails, text="2- se não for para todos siga o formato:")
            instrução_2.grid( row=4, column=1, columnspan=3)

            instrução_3 =  Label(Janela_confirmar_emails, text="id,id2,id3,id4... (1,2,3,4...)")
            instrução_3.grid( row=5, column=1, columnspan=3)

            escolha_id = Entry(Janela_confirmar_emails)
            escolha_id.grid(row=6, column=1, columnspan=3)


            botao_confirma = Button(Janela_confirmar_emails, text="Confirmar", command= ids_escolhidos)
            botao_confirma.grid(row=7, column=1, columnspan=3)
            
            botao_voltar_Janela_confirmar_emails = Button(Janela_confirmar_emails, text="Voltar", command= fechar_Janela_confirmar_emails)
            botao_voltar_Janela_confirmar_emails.grid(row=8, column=1, columnspan=3)

            confirma = Label(Janela_confirmar_emails,text="")
            confirma.grid(row=8, column=1)
            Janela_escolha_nome.iconify()
            Janela_confirmar_emails.mainloop()


        instrução =  Label(Janela_escolha_nome, text="Qual o nome da nova lista?")
        instrução.grid( row=2, column=1, columnspan=3)
        
        escolha_nome = Entry(Janela_escolha_nome)
        escolha_nome.grid(row=3, column=1, columnspan=3)
        
        confirma = Button(Janela_escolha_nome, text="Confirmar", command= seleção_usuarios)
        confirma.grid(row=4, column=1, columnspan=3)
        
        botao_voltar_Janela_escolha_nome= Button(Janela_escolha_nome, text="Voltar", command=fechar_botao_voltar_Janela_escolha_nome)
        botao_voltar_Janela_escolha_nome.grid(row=5, column=1, columnspan=3)
        
        Janela_seleção_lista.iconify()
        Janela_escolha_nome.mainloop()

    tabela_listas = ttk.Treeview(Janela_seleção_lista, columns=("id" ,"Nome da Lista"), show="headings")
    tabela_listas.column('id' ,minwidth=0, width=50)
    tabela_listas.column('Nome da Lista' ,minwidth=0, width=150)
    tabela_listas.heading('id', text="ID")
    tabela_listas.heading('Nome da Lista', text="NOME DA LISTA")
    tabela_listas.grid(row= 1, column=1, columnspan= 3)

    for labels in range  (0, len(lista_tabelas)):
        lista_tabelas[labels] = str(lista_tabelas[labels]).replace("'", " ").replace("(", "").replace(")", "").replace(",","").replace(" ","")

    for itens in range (1, len(lista_tabelas)+1):
        lista_id.append(itens)

    for i in range(0,len(lista_tabelas)):
        tabela_listas.insert("", "end",values=(lista_id[i], lista_tabelas[i]))
        
    instrução =  Label(Janela_seleção_lista, text="Id da lista de emails")
    instrução.grid( row=2, column=1, columnspan=3)

    escolha_id = Entry(Janela_seleção_lista)
    escolha_id.grid(row=3, column=1, columnspan=3)


    botao_escolher_msg = Button(Janela_seleção_lista, text="Escolher mensagem", command= Escolher_mensagem)
    botao_escolher_msg.grid(row=4, column=1, columnspan=3)


    botao_confirma = Button(Janela_seleção_lista, text="Criar nova lista", command= escolha_nome_lista)
    botao_confirma.grid(row=5, column=1, columnspan=3)
    
    botao_voltar_Janela_seleção_lista = Button(Janela_seleção_lista, text="Voltar", command= fechar_Janela_seleção_lista)
    botao_voltar_Janela_seleção_lista.grid(row=6, column=1, columnspan=3)
    
    Janela_main.iconify()
    Janela_seleção_lista.mainloop()



texto_bem_vindo = Label(Janela_main, text= "Bem vindo ao programa de envio e cadastro de emails!!")
texto_bem_vindo.grid(column=0, row= 0, padx=15, pady= 5, columnspan=3)


botao_pag_cadastro = Button(Janela_main, text= "Cadastrar novos Emails", command= pagina_Cadastrar)
botao_pag_cadastro.grid(column=0, row=1,padx=15, pady= 5, columnspan=3)

botao_pag_gerenciamento= Button(Janela_main, text= "Gerenciar emails", command= gerenciamento_emails)
botao_pag_gerenciamento.grid(column=0, row=2,padx=15, pady= 5, columnspan=3)

botao_pag_envio = Button(Janela_main, text= "Enviar Emails", command=Escolher_Lista_ou_Criar)
botao_pag_envio.grid(column=0, row=3,padx=15, pady= 5, columnspan=3)

Janela_main.mainloop()
