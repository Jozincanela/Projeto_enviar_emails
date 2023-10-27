from tkinter import *
from tkinter import ttk
from bd_poo import CRUD
from tkinter import filedialog
from PIL import Image, ImageTk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, SimpleDocTemplate, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import time
import threading

Janela_main = Tk()
Janela_main.title("Main")

Cadastro = CRUD("C:\\Users\\afrod\\OneDrive\\Documentos\\Programas\\Projeto envio emails\\banco_projeto_email.db")


Tabela_cadastro = "Cadastros"
colunas_cadastro = "Nome, Sobrenome, Email"

Tabela_excluidos = "Excluidos"
coluanas_excluidos = "CHAVE,Nome,Sobrenome,Email"

tabela_mensagem =  "Mensagem"
colunas_mensagem = "mensagem chaves_usuarios"

tabela_email_salvo = "Email"
coluna_email_salvo = "Email, Senha"

Cadastro.nova_tabela("Cadastros", "Nome TEXT, Sobrenome TEXT, Email TEXT",0)
Cadastro.nova_tabela("Mensagem", "Mensagem TEXT, Titulo TEXT, Chaves_Usuarios TEXT, Imagem TEXT", 0)
Cadastro.nova_tabela("Excluidos","Nome TEXT,Sobrenome TEXT, Email TEXT", 0 )
Cadastro.nova_tabela("Email","Email TEXT,Senha TEXT", 1)


def Sair():
    Janela_main.destroy()

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
        Janela_main.deiconify()
        Janela_gerenciamento.destroy()
        
    def deletar_usuario():
        Janela_gerenciamento.iconify()
        Janela_delete_usu = Tk()
        Janela_delete_usu.title("Deletar Usuario")
        
        def Fechar():
            Janela_gerenciamento.deiconify()
            Janela_delete_usu.destroy()
        
        def Entrys_del():
        
            try:
                informaoes_usuario = str(Cadastro.ler_dado_id(Tabela_cadastro,int(ID_usuario.get()) )).replace("(", "").replace(")", "").replace("[","").replace("]", "")
                chave_pessoa = list(Cadastro.ler_dado_id(Tabela_cadastro, int(ID_usuario.get()))  [0])[0]
                for tabelas in str(Cadastro.Tabelas()).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("[","").replace("]", "").split(" "):
                    Cadastro.apagar_dados_linha_chave(tabelas, chave_pessoa)
                Cadastro.inserir_dados(Tabela_excluidos,"CHAVE,Nome,Sobrenome,Email",informaoes_usuario,1)
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

    botao_deletar_linha = Button(Janela_gerenciamento, text="Deletar Usuario", command= deletar_usuario)
    botao_deletar_linha.grid(column=4, row= 1, padx=15, pady= 0, columnspan=2)

    
    botao_voltar = Button(Janela_gerenciamento, text="voltar", command=Fechar)
    botao_voltar.grid(column=4, row= 2, padx=15, pady= 5, columnspan=3)




    Janela_gerenciamento.mainloop()

def Enviar_Emails():
    Janela_Mensagem = Tk()
    Janela_Mensagem.title("Escolher mensagem")
    Janela_main.iconify()

    lista_mensagens =[]
    lista_chaves = []
    
    def fechar_Janela_Mensagem():
        Janela_main.deiconify()
        Janela_Mensagem.destroy()
        
    def enviar_email():

        id_msg_send = Id_lista_msg.get()
        dados_msg = Cadastro.ler_dado_id(tabela_mensagem, int(id_msg_send))
        lista_chaves_envia = str(list(dados_msg[0])[3]).replace("  ", "").split(" ")
        

        caminho_img = str(list(dados_msg[0])[4])
        titulo = str(list(dados_msg[0])[2])


        
        for ids in range(0, len(lista_chaves_envia)-1):
            dados_usuario = list(Cadastro.ler_dado_chave(Tabela_cadastro,lista_chaves_envia[ids]))[0]
                
            destinatario = ""
            destinatario = dados_usuario[3]

            Nome = ""
            Sobrenome =""
            Nome =  dados_usuario[1]
            Sobrenome =  dados_usuario[2]
                
            corpo = ""
            corpo = str(list(dados_msg[0])[1]).replace("{Nome, Sobrenome}", f"{Nome} {Sobrenome}")
            
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_username = list(Cadastro.ler_dado_id(tabela_email_salvo, 1)[0])[0]
            smtp_password = list(Cadastro.ler_dado_id(tabela_email_salvo, 1)[0])[1]
                
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = destinatario
            msg['Subject'] = titulo
            msg.attach(MIMEText(corpo, 'plain'))
            with open(caminho_img, 'rb') as imagem_arquivo:
                imagem = MIMEImage(imagem_arquivo.read())
                imagem.add_header('Content-Disposition', 'attachment', filename='imagem.jpg')
                msg.attach(imagem)

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, destinatario, msg.as_string())
            server.quit()

        resultado['text'] = f"OK"
    
    def detalhe_msg():
        try:
            Janela_detalhe_msg = Tk()
            Janela_detalhe_msg.title("Detalhes da msg")
            Janela_Mensagem.iconify()
            def preview():
                def enviar_preview():
                    try:
                        id_msg_send = Id_lista_msg.get()
                        dados_msg = Cadastro.ler_dado_id(tabela_mensagem, int(id_msg_send))
                        caminho_img = str(list(dados_msg[0])[4])
                        titulo = str(list(dados_msg[0])[2])
                        destinatario = email_viewer.get()
                        corpo = str(list(dados_msg[0])[1])
                        smtp_server = 'smtp.gmail.com'
                        smtp_port = 587
                        smtp_username = list(Cadastro.ler_dado_id(tabela_email_salvo, 1)[0])[0]
                        smtp_password = list(Cadastro.ler_dado_id(tabela_email_salvo, 1)[0])[1]
                        
                        msg = MIMEMultipart()
                        msg['From'] = smtp_username
                        msg['To'] = destinatario
                        msg['Subject'] = titulo
                        msg.attach(MIMEText(corpo, 'plain'))
                        with open(caminho_img, 'rb') as imagem_arquivo:
                            imagem = MIMEImage(imagem_arquivo.read())
                            imagem.add_header('Content-Disposition', 'attachment', filename='imagem.jpg')
                            msg.attach(imagem)
                        server = smtplib.SMTP(smtp_server, smtp_port)
                        server.starttls()
                        server.login(smtp_username, smtp_password)
                        server.sendmail(smtp_username, destinatario, msg.as_string())
                        server.quit()
                        email_viewer.delete(0,END)
                        email_viewer_instrucao['text']="Email enviado com sucesso!"
                    except:
                        email_viewer_instrucao['text'] ="Não foi possivel enviar o email"    
                email_viewer_instrucao = Label(Janela_detalhe_msg, text="insira seu email para ver a preview")
                email_viewer_instrucao.grid(row=14, column=0)

                email_viewer = Entry(Janela_detalhe_msg)
                email_viewer.grid(row=15, column=0)
                
                botao_enviar_preview = Button(Janela_detalhe_msg, text="confirmar", command=enviar_preview)
                botao_enviar_preview.grid(row=16, column=0)
                
                
            def preview_pdf():
                try:     
                        id_msg_send = Id_lista_msg.get()
                        dados_msg = Cadastro.ler_dado_id(tabela_mensagem, int(id_msg_send))
                
                        caminho_img = str(list(dados_msg[0])[4])
                        titulo = str(list(dados_msg[0])[2])
                        corpo = str(list(dados_msg[0])[1])
                        pdf_file = f"Mensage_{id_msg_send}.pdf"

                        doc = SimpleDocTemplate(pdf_file, pagesize=letter)

                        story = []

                        styles = getSampleStyleSheet()
                        title_style = styles["Title"]
                        title = Paragraph(titulo, title_style)
                        story.append(title)

                        text = corpo
                        story.append(Paragraph(text, styles["Normal"]))

                        image_path = caminho_img
                        img = Image(image_path, width=300, height=200)
                        story.append(img)

                        doc.build(story)
                        criacao_pdf['text'] = f"Pdf {titulo} foi criado com sucesso"
                except:
                        criacao_pdf['text'] = f"Pdf não foi criado"
                        pass
            def fechar():
                Janela_Mensagem.deiconify()
                Janela_detalhe_msg.destroy()
                
            id_escolhido_msg = Id_lista_msg.get()
            id_escolhido_msg_nao_tratado = Cadastro.selecionar_linhas(tabela_mensagem,int(id_escolhido_msg))
            id_escolhido_msg_nao_tratado =  list(id_escolhido_msg_nao_tratado)
                
            mensagem_email = id_escolhido_msg_nao_tratado[1]
            mensagem_titulo = id_escolhido_msg_nao_tratado[2]
            chaves_usuarios = id_escolhido_msg_nao_tratado[3]
            caminho = str(id_escolhido_msg_nao_tratado[4]).replace("\\", "\\\\")
        
            instrucao_0 = Label(Janela_detalhe_msg, text="Titulo:")
            instrucao_0.grid(row=0, column=0)
            titulo = Label(Janela_detalhe_msg, text=mensagem_titulo)
            titulo.grid(row=1, column=0)
            instrucao_0 = Label(Janela_detalhe_msg, text="Mensagem:")
            instrucao_0.grid(row=2, column=0)
            mensagem = Label(Janela_detalhe_msg, text=mensagem_email)
            mensagem.grid(row=3, column=0)
            instrucao_1 = Label(Janela_detalhe_msg, text="Chaves que serão enviadas:")
            instrucao_1.grid(row=4, column=0)
            chaves_usu = Label(Janela_detalhe_msg, text=chaves_usuarios)
            chaves_usu.grid(row=5, column=0)
            instrucao_2 = Label(Janela_detalhe_msg, text="Imagem escolhida")
            instrucao_2.grid(row=6, column=0)
            instrucao_2 = Label(Janela_detalhe_msg, text= caminho)
            instrucao_2.grid(row=7, column=0)
                
            preview_pdf_button = Button(Janela_detalhe_msg, text="PDF", command=preview_pdf)
            preview_pdf_button.grid(row=11, column=0)
            criacao_pdf = Label(Janela_detalhe_msg, text= "")
            criacao_pdf.grid(row=12, column=0)
                
            preview_emails_button = Button(Janela_detalhe_msg, text="preview email", command=preview)
            preview_emails_button.grid(row=13, column=0)
            fechar_button = Button(Janela_detalhe_msg, text="Fechar", command=fechar)
            fechar_button.grid(row=17, column=0)


            Janela_detalhe_msg.mainloop()
        except:
            Janela_Mensagem.deiconify()
            Janela_detalhe_msg.destroy()
            resultado['text'] = "Não foi possivel encontrar tal mensagem"
            pass
    
    def deletar_msg():
        try:
            Cadastro.apagar_dados_linha(tabela_mensagem,int(Id_lista_msg.get()))
            resultado['text'] = "Mensagem deletada!"
        except:
            resultado['text'] = "Não foi possivel deletar mensagem"
            pass
    
    def atualizar_msg ():
        try:
            Janela_Atualizar = Tk()
            Janela_Atualizar.title("atualize a mensagem")
            Janela_Mensagem.iconify()
            def caminho_img():
                filepath = filedialog.askopenfilename(title="Escolha uma imagem")
                filepath = filepath.replace("/", "\\")
                Nova_imagem.delete(0,END)
                Nova_imagem.insert(0, filepath)
                print(filepath)
                
                
            def Fechar_Janela_Atualizar():
                Janela_Mensagem.deiconify()
                Janela_Atualizar.destroy()
                
                
            def Salvar():
                try:
                    atualizacao = f"Mensagem='{Nova_Mensagem.get()}',Titulo='{Novo_titulo.get()} ', Chaves_Usuarios='{Novas_chaves.get()}', Imagem='{Nova_imagem.get()}'"
                    
                    Cadastro.atualizar_dados(tabela_mensagem,int(Id_lista_msg.get()),atualizacao )
                    Confirma_salvamento = Label(Janela_Atualizar, text="Usuario modificado!")
                    Confirma_salvamento.grid(row=9, column=0, columnspan=4)
                except:
                        pass
                    

            
            confirma_atualizacao =  Button(Janela_Atualizar, text="Salvar", command=Salvar)
            confirma_atualizacao.grid(row=12, column=0, columnspan=4)
                
            Novo_titulo_instrucao = Label(Janela_Atualizar, text="Edite seu titulo:")
            Novo_titulo_instrucao.grid(row=1, column=0, columnspan=4)
            Novo_titulo =  Entry(Janela_Atualizar, width=50)
            Novo_titulo.grid(row=2, column=0, columnspan=4)
            
            Nova_Mensagem_instrucao =  Label(Janela_Atualizar, text="Edite a Mensagem:")
            Nova_Mensagem_instrucao.grid(row=3, column=0, columnspan=4)
            Nova_Mensagem = Entry(Janela_Atualizar, width=50)
            Nova_Mensagem.grid(row=4, column=0, columnspan=4)
            
            Novas_chaves_instrucao =  Label(Janela_Atualizar, text="Edite as chaves:")
            Novas_chaves_instrucao.grid(row=5, column=0, columnspan=4)
            Novas_chaves = Entry(Janela_Atualizar, width=50)
            Novas_chaves.grid(row=6, column=0, columnspan=4)
            
            Nova_imagem_instrucao =  Label(Janela_Atualizar, text="Edite a imagem:")
            Nova_imagem_instrucao.grid(row=7, column=0, columnspan=4)
            Nova_imagem = Entry(Janela_Atualizar, width=50)
            Nova_imagem.grid(row=8, column=0, columnspan=4)
            botao_selecao_nova_img =  Button(Janela_Atualizar, text="escolher imagem", command=caminho_img)
            botao_selecao_nova_img.grid(row=10,column=0, columnspan=4)
            
            botao_fechar =  Button(Janela_Atualizar,text="Voltar", command=Fechar_Janela_Atualizar)
            botao_fechar.grid(row=13, column=0, columnspan=4)



            informacoes_usuario = list(Cadastro.selecionar_linhas(tabela_mensagem,int(Id_lista_msg.get())))
            Novo_titulo.insert(0, informacoes_usuario[2])
            Nova_Mensagem.insert(0, informacoes_usuario[1])
            Novas_chaves.insert(0, informacoes_usuario[3])
            Nova_imagem.insert(0, informacoes_usuario[4])    
            
            Janela_Atualizar.mainloop()
        except:
            Janela_Atualizar.destroy()
            Janela_Mensagem.deiconify()
            resultado['text'] = "Não foi atualizar mensagem"
            pass
    
    def nova_mensagem ():
        Janela_Mensagem.iconify()
        Janela_Nova_Mensagem = Tk()
        Janela_Nova_Mensagem.title("Escolher mensagem")

        def Fechar_Janela_Nova_Mensagem():
            Janela_Mensagem.deiconify()
            Janela_Nova_Mensagem.destroy()
        
        
        def criar_mensagem ():
            try:
                chaves = ""
                ids_tratados = ID_usuario.get().split(",")
                for i in range(0 ,len(ids_tratados)):
                    lista_dados = list(Cadastro.ler_dado_id(Tabela_cadastro,int(ids_tratados[i]))[0])
                    chaves += f"{lista_dados[0]} "

                msg = Nova_msg.get()
                img = caminho_img.get()
                titl = Novo_titulo.get()

                Cadastro.inserir_dados(tabela_mensagem,"'Mensagem','Titulo' ,'Chaves_Usuarios' ,'Imagem'", f"'{msg}','{titl}' ,'{chaves}', '{img}'", 0)
            except:
                confirmar_nova_msg['text'] = "Não foi possivel criar nova mensagem"
                Nova_msg.delete(0, END)
                ID_usuario.delete(0,END)
                caminho_img.delete(0,END)
                pass
                
        def Adicionar_imagem():
            filepath = filedialog.askopenfilename(title="Escolha uma imagem")
            filepath = filepath.replace("/", "\\\\")
            caminho_img.grid(row=10, column=5)
            caminho_img.insert(0,filepath)

        global Nomes_das_listas
        lista_nome_limpa = []
        Nomes_das_listas =[]
        dados_coluna = Cadastro.selecionar_colunas(Tabela_cadastro, "Nome, Sobrenome")
        for dados in range (0, len(dados_coluna)):
            lista_de_nome = list(dados_coluna[dados])
            for i in range (0,len(lista_de_nome)-1):
                lista_de_nome[i] += " " + lista_de_nome[i+1]
                lista_de_nome[i] = str(lista_de_nome[i]).title()
                lista_de_nome.remove(lista_de_nome[i+1])
                lista_nome_limpa.append(lista_de_nome[i])


        tabela_listas = ttk.Treeview(Janela_Nova_Mensagem, columns=("id" ,"Nome de todos usuarios"), show="headings", height=15)
        tabela_listas.column('id' ,minwidth=0, width=50)
        tabela_listas.column('Nome de todos usuarios' ,minwidth=0, width=150)
        tabela_listas.heading('id', text="ID")
        tabela_listas.heading('Nome de todos usuarios', text="NOME USUARIOS")
        tabela_listas.grid(row= 0, column=0, columnspan= 5, rowspan= 18)

        for labels in range  (0, len(lista_nome_limpa)):
            lista_nome_limpa[labels] = str(lista_nome_limpa[labels]).replace("'", " ").replace("(", "").replace(")", "").replace(",","")

        for id in range(0,len(lista_nome_limpa)):
            tabela_listas.insert("", "end",values=(id + 1, lista_nome_limpa[id]))
            
        ID_usuario_instrucao =  Label(Janela_Nova_Mensagem, text="ID's dos usuarios que irão receber a mensagem")
        ID_usuario_instrucao.grid(row=0, column=5)
        ID_usuario = Entry(Janela_Nova_Mensagem, width=35)
        ID_usuario.grid(row=1, column=5, columnspan=1)
        
        instrucao_nova_mensagem =  Label(Janela_Nova_Mensagem, text="Nova mensagem \n OBS: para adicionar o nome do cliente \n ulilizar {Nome, Sobrenome } ")
        instrucao_nova_mensagem.grid(row=7, column=5)
        
        Nova_msg = Entry(Janela_Nova_Mensagem, width=35)
        Nova_msg.grid(row=8, column=5, columnspan=1)
        
        instrucao_novo_titulo =  Label(Janela_Nova_Mensagem, text="Novo Titulo")
        instrucao_novo_titulo.grid(row=5, column=5)
        
        Novo_titulo = Entry(Janela_Nova_Mensagem, width=35)
        Novo_titulo.grid(row=6, column=5, columnspan=1)

        Adicionar_img = Button(Janela_Nova_Mensagem, text="Adicionar imagem", command=Adicionar_imagem)
        Adicionar_img.grid(row=9, column=5)
        
        caminho_img = Entry(Janela_Nova_Mensagem)

        botao_criar_msg = Button(Janela_Nova_Mensagem, text="Confirma", command=criar_mensagem)
        botao_criar_msg.grid(row=11, column=5)
        
        confirmar_nova_msg = Label(Janela_Nova_Mensagem, text="")
        confirmar_nova_msg.grid(row=12, column=5)
        
        botao_fechar_Janela_Nova_Mensagem = Button(Janela_Nova_Mensagem, text="voltar", command=Fechar_Janela_Nova_Mensagem)
        botao_fechar_Janela_Nova_Mensagem.grid(row=13, column=5)

        Janela_Nova_Mensagem.mainloop()
    

        
        
    dados_coluna_mensagems = Cadastro.selecionar_colunas(tabela_mensagem, "Mensagem")
    for dados in range (0, len(dados_coluna_mensagems)):
        lista_mensagens.append(dados_coluna_mensagems[dados])
        
    dados_coluna_chave = Cadastro.selecionar_colunas(tabela_mensagem, "Chaves_Usuarios")
    for dados in range (0, len(dados_coluna_chave)):
        lista_chaves.append(dados_coluna_chave[dados])

    tabela_listas = ttk.Treeview(Janela_Mensagem, columns=("id" ,"Mensagem", "Chaves"), show="headings")
    tabela_listas.column('id' ,minwidth=0, width=50)
    tabela_listas.column('Mensagem' ,minwidth=0, width=250)
    tabela_listas.column('Chaves' ,minwidth=0, width=150)

    tabela_listas.heading('id', text="ID")
    tabela_listas.heading('Mensagem', text="Mensagem")
    tabela_listas.heading('Chaves', text="Chaves dos usuarios presentes")

    tabela_listas.grid(row= 0, column=0, columnspan= 3, rowspan= 15)

    for labels in range  (0, len(lista_mensagens)):
        lista_mensagens[labels] = str(lista_mensagens[labels]).replace("'", " ").replace("(", "").replace(")", "").replace(",","")

    for chaves in range  (0, len(lista_chaves)):
        lista_chaves[chaves] = str(lista_chaves[chaves]).replace("'", " ").replace("(", "").replace(")", "").replace(",","    ")

    for id in range(0,len(lista_mensagens)):
        tabela_listas.insert("", "end",values=(id + 1, lista_mensagens[id], lista_chaves[id]))
        
        
    instrucao_id_msg = Label(Janela_Mensagem, text="Id da mensagem")
    instrucao_id_msg.grid(row= 1, column=3, columnspan= 3)

    Id_lista_msg =  Entry(Janela_Mensagem)
    Id_lista_msg.grid(row= 2, column=3, columnspan= 3)

    botao_confirmar_msg =  Button(Janela_Mensagem, text="Confirma", command=enviar_email)
    botao_confirmar_msg.grid(row= 3, column=3, columnspan= 3)

    botao_mudar_msg = Button(Janela_Mensagem, text="Atualizar mensagem " ,command=atualizar_msg)
    botao_mudar_msg.grid(row=4, column=3, columnspan=3)

    botao_delete_msg = Button(Janela_Mensagem, text="deletar linha", command= deletar_msg)
    botao_delete_msg.grid(row= 5, column=3, columnspan=3)

    botao_detalhes = Button(Janela_Mensagem, text="Sobre", command=detalhe_msg)
    botao_detalhes.grid(row=6, column=3, columnspan=3)

    resultado = Label(Janela_Mensagem, text="")
    resultado.grid(row=7, column=3, columnspan=3)

    botao_criar_nova_msg =  Button(Janela_Mensagem, text="Criar nova mensagem", command=nova_mensagem)
    botao_criar_nova_msg.grid(row= 12, column=3, columnspan= 3)
    

    botao_fechar = Button(Janela_Mensagem, text="Voltar", command=fechar_Janela_Mensagem)
    botao_fechar.grid(row= 14, column=3, columnspan= 3)

    Janela_Mensagem.mainloop()

def Respostas():
    Janela_resposta = Tk()
    Janela_resposta.title("Respostas")
    Janela_main.iconify()

    def Voltar_Janela_resposta():
        Janela_main.deiconify()
        Janela_resposta.destroy()

    botao_voltar_Janela_resposta = Button(Janela_resposta, text="Voltar", command=Voltar_Janela_resposta)
    botao_voltar_Janela_resposta.grid(column=0, row=0)
    Janela_resposta.mainloop()


def login():
    Janela_login = Tk()
    Janela_login.title("Login")
    Janela_main.iconify()
    
    def Voltar_Janela_main():
        Janela_main.deiconify()
        Janela_login.destroy()


    def verificacao_senha():
        if(senha.get() == '0123'):
            Janela_configuracoes = Tk()
            Janela_configuracoes.title("configuracoes")
            Janela_login.iconify()
            
            def Fechar():
                Janela_main.deiconify()
                Janela_configuracoes.destroy()
                Janela_login.destroy()


            def Salvar_email():
                try :
                    Cadastro.ler_dado_id(tabela_email_salvo, 1) 
                    Aviso_Janela_config['text']= "Já existe um email cadastrado!"
                except:
                        try:
                            valores = f"'{email_de_envio.get()}','{senha_email.get()}'"
                            Cadastro.inserir_dados(nome_tabela=tabela_email_salvo,valores=valores,nome_coluna=coluna_email_salvo ,tipo_da_tabela=1)
                            Aviso_Janela_config["text"]= "Salvo!"
                            email_de_envio.delete(0,END)
                            senha_email.delete(0,END)
                        except:
                            Aviso_Janela_config['text']= "Invalido!"
                    



            email_de_envio_instrucao = Label(Janela_configuracoes, text="Email de envio")
            email_de_envio_instrucao.grid(column =0, row=0)

            email_de_envio = Entry(Janela_configuracoes)
            email_de_envio.grid(column =0, row=1)

            senha_email_instrucao = Label(Janela_configuracoes, text="Senha de app")
            senha_email_instrucao.grid(column=0, row=2)

            senha_email = Entry(Janela_configuracoes)
            senha_email.grid(column=0, row=3)

            Janela_configuracoes_salvar = Button(Janela_configuracoes, text="Salvar", command = Salvar_email)
            Janela_configuracoes_salvar.grid(column=0, row=4)

            Janela_configuracoes_fechar= Button(Janela_configuracoes, text="Fechar", command = Fechar)
            Janela_configuracoes_fechar.grid(column=0, row=5)

            Aviso_Janela_config = Label(Janela_configuracoes, text="")
            Aviso_Janela_config.grid(column=0, row=6)

            Janela_configuracoes.mainloop()



    instrucao_senha = Label(Janela_login, text = "Senha")
    instrucao_senha.grid(column=0, row=1)

    senha = Entry(Janela_login)
    senha.grid(column = 0, row=2)

    botao_senha = Button(Janela_login, text="confirma", command = verificacao_senha)
    botao_senha.grid(column=0, row=3)

    botao_Janela_login_voltar = Button(Janela_login,text="voltar", command=Voltar_Janela_main)
    botao_Janela_login_voltar.grid(column=0, row = 4)
    

    Janela_login.mainloop()


texto_bem_vindo = Label(Janela_main, text= "Bem vindo ao programa de envio e cadastro de emails!!")
texto_bem_vindo.grid(column=0, row= 0, padx=15, pady= 5, columnspan=3)


botao_pag_cadastro = Button(Janela_main, text= "Cadastrar novos Emails", command= pagina_Cadastrar)
botao_pag_cadastro.grid(column=0, row=1,padx=15, pady= 5, columnspan=3)

botao_pag_gerenciamento= Button(Janela_main, text= "Gerenciar emails", command= gerenciamento_emails)
botao_pag_gerenciamento.grid(column=0, row=2,padx=15, pady= 5, columnspan=3)

botao_pag_envio = Button(Janela_main, text= "Enviar Emails", command=Enviar_Emails)
botao_pag_envio.grid(column=0, row=3,padx=15, pady= 5, columnspan=3)


botao_ver_respostas = Button(Janela_main, text= "Ver Respostas", command=Respostas)
botao_ver_respostas.grid(column=0, row=4,padx=15, pady= 5, columnspan=3)

botao_ver_respostas = Button(Janela_main, text= "Area do administrador", command=login)
botao_ver_respostas.grid(column=0, row=4,padx=15, pady= 5, columnspan=3)

botao_sair = Button(Janela_main, text= "Fechar", command=Sair)
botao_sair.grid(column=0, row=5,padx=15, pady= 5, columnspan=3)

Janela_main.mainloop()
