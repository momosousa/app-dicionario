import requests
import json

from tkinter import *
from tkinter import Tk, ttk
from tkinter import ttk
from PIL import Image, ImageTk
from tkscrolledframe import ScrolledFrame

# CORES
cores = ["#7D7ABF", "#feffff", "#27A4F2", "#0D0D0D", "#F2529D"]
co0, co1, co3, co4, co5 = cores

# CONFIGURANDO A JANELA
janela = Tk()
janela.title("")
janela.geometry("350x430")
janela.configure(background=co1)
janela.resizable(width=FALSE, height=FALSE)

# FRAMES
frameCima = Frame(janela, width=350, height=100, bg=co1, relief="solid",)
frameCima.grid(row=0, column=0)

frameMeio = Frame(janela, width=350, height=65, bg=co1, relief="solid",)
frameMeio.grid(row=1, column=0)

frameBaixo = Frame(janela, width=350, height=290, bg=co1, relief="raised")
frameBaixo.grid(row=2, column=0)

# CRIAR WIDGET DO SCROLLEDFRAME
sf = ScrolledFrame(frameBaixo, width=310, height=240, bg=co1)
sf.pack(fill=BOTH, expand=False, padx=0, pady=35)

# Passando tudo para dentro da frame
framecanva = sf.display_widget(Frame, fit_width=TRUE, bg=co1)

# LOGOTIPO E NOME DO APLICATIVO
app_img = Image.open("img\logotipo.png").resize((50, 50))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameCima, image=app_img, compound=LEFT, padx=5, relief=FLAT, anchor=NW, bg=co1, fg=co4, text="Dicionário", font=('Montserrat 20 bold'))
app_logo.pack(side=LEFT)

# FUNÇÃO - ACESSAR API
def procurar(): 
    # Obter a palavra digitada na entrada
    palavra = e_palavra.get()

    # Atualizar o texto da label para exibir a palavra pesquisada
    l_palavra['text'] = palavra

    # Consumir a API e obter os dados da palavra pesquisada
    try:
        resposta_api = requests.get(f"https://dicio-api-ten.vercel.app/v2/{palavra}")
        dados = resposta_api.json()

        if "error" in dados:
            raise ValueError("Não foi possível obter as informações da palavra.")
    except ValueError as e:
        print("Erro ao obter informações da API:", e)
        l_palavra['text'] = "Sem resultados!"
        dados = {}
    
    # Remover possíveis resultados anteriores
    for widget in framecanva.winfo_children():
        widget.destroy()
    
    # Dicionário para salvar o nome das variáveis dos frames
    frames = {}

    # Contador de linhas para frame
    num_row = 0
    for i in range(len(dados)):
        # Criar um novo frame e posicionar dentro do framecanva
        frames["F{}".format(i)] = Frame(framecanva, width=310, height=100, bg=co1)
        frames["F{}".format(i)].grid(row=num_row, column=0, sticky=NSEW, pady=2)

        # Adicionar o significado da palavra ao label
        l_significado = Label(frames["F{}".format(num_row)], text=dados[i]['partOfSpeech'], height=1, anchor=NW, font=("Montserrat 10 bold"), bg=co1, fg=co5)
        l_significado.place(x=10, y=8)

        # Adicionar os exemplos ao label
        l_exemplo = Label(frames["F{}".format(num_row)], text="", wraplength=300, justify=LEFT, height=5, anchor=NW, font=("Montserrat 9"), bg=co1, fg=co4)
        l_exemplo.place(x=10, y=30)
        for j in dados[i]['meanings']:
            l_exemplo['text'] = j

        # Incrementar o valor da linha
        num_row += 1

# FRAME MEIO
l_palavra = Label(frameMeio, text="Digite a palavra:", height=0, anchor=NW, font=('Montserrat 10 italic bold'), bg=co1, fg=co4)
l_palavra.place(x=8, y=10)
e_palavra = Entry(frameMeio, width=15, font=("Montserrat 14"), justify="center", relief="solid")
e_palavra.place(x=10, y=35)

# BOTÃO PROCURAR - FRAME MEIO
img_procurar = Image.open("img\icone-procurar.png")
img_procurar= img_procurar.resize((18, 18))
img_procurar = ImageTk.PhotoImage(img_procurar)
b_procurar = Button(frameMeio, command=procurar, image=img_procurar, compound=LEFT, width=100, height=23, text="  Procurar",font="Montserrat 10 bold", bg=co1, fg=co4)
b_procurar.place(x=230, y=34)

# LABEL - FRAME BAIXO
l_palavra = Label(frameBaixo, text="", padx=10, width=37, height=1, anchor=NW, font=("Montserrat 12 bold"), bg=co0, fg=co1)
l_palavra.place(x=0, y=10)

# FUNÇÃO - VERIFICAR SE ALGO FOI DIGITADO
def verificar():
    if len(e_palavra.get()) > 0:
        b_procurar['state'] = 'normal'
    else:
        b_procurar['state'] = 'disabled'

e_palavra.bind('<KeyRelease>', lambda event: verificar())
b_procurar['state'] = 'disabled'

janela.mainloop()