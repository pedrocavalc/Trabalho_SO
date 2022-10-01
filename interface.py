from asyncio.windows_events import NULL
from os import popen
from tkinter import *
import tkinter
from tokenize import Double
from PIL import Image,ImageTk
from fluxograma import *
clients_count = 0
ID = 0
SENHA = 0
TEMPO = 0

def rgb_to_hex(rgb):
    '''
    Função para converter hex to rgb
    '''
    return "#%02x%02x%02x" % rgb  

def KeyboardInterruptcreate_button(path_img,scale):
    '''
    Função para criar resizes de imagens do botão e retorna-las para uso
    '''
    button_img = (Image.open(path_img))
    width, height = button_img.size
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized_img = button_img.resize((new_width,new_height), Image.ANTIALIAS)
    resized_img = ImageTk.PhotoImage(resized_img)
    return resized_img

def create_button(path_img,scale):
    '''
    Função para criar resizes de imagens do botão e retorna-las para uso
    '''
    button_img = (Image.open(path_img))
    width, height = button_img.size
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized_img = button_img.resize((new_width,new_height), Image.ANTIALIAS)
    resized_img = ImageTk.PhotoImage(resized_img)
    return resized_img

def click():
    '''
    Função para lidar com o click do start button
    '''
    TEMPO = tempo_atendimento_entry.get()
    if TEMPO.strip() == '':
        print('invalido')
    else:
        print(TEMPO)
    id = clients_count + 1
    ta = TEMPO
    senha = clients_count + 1
    Cliente(id, ta, senha).start()

def open_popup():
   top= Toplevel(window)
   top.geometry("500x500")
   top.title("Quantidade de caixas")
   t_text = Label(top,text='Insira a quantidade de caixas',font=('Arial',10))
   t_text.place(x = 200, y = 200)
   t_entry = Entry(top,width = 5,font=('Arial',20))
   t_entry.place(x=200,y = 220)

   initial_img = create_button(path_img='assets/start_button.png',scale=0.5)
   initial_button = Button(top, bd ='2',command=print('henrique bobão'))
   initial_button.config(image = initial_img)
   initial_button.place(x = 220,y = 270)
# inicializando a janela
window = Tk()
# min e max size da janela
window.minsize(1366,768)
window.maxsize(1366,768)
window.configure(bg=rgb_to_hex((204,255,255)))

# criando um canvas
canvas = Canvas(window,width = 1366,height = 600)
canvas.pack()

open_popup()

# setando o back ground
background = (Image.open('assets/background.png'))
resized_background = background.resize((1366,600), Image.ANTIALIAS)
background_image = ImageTk.PhotoImage(resized_background)

# colocando o background na janela
canvas.create_image(0,0,anchor=NW,image = background_image)

# criando os botões de start e exit

start_img = create_button(path_img='assets/start_button.png',scale=0.8)
start_button = Button(window, bd ='5',command=click)
start_button.config(image = start_img)
start_button.place(x = 100,y = 630)

exit_img = create_button(path_img='assets/exit_button.png',scale=0.8)
exit_button = Button(window,bd = '5', command=window.destroy)
exit_button.config(image = exit_img )
exit_button.place(x = 600,y= 630)

# criando as entry

tempo_atendimento_text = Label(window,text='Insira o tempo de atendimento',font=('Arial',10), bg=rgb_to_hex((204,255,255)))
tempo_atendimento_text.place(x = 350, y = 630)
tempo_atendimento_entry = Entry(window,width = 5,font=('Arial',20))
tempo_atendimento_entry.place(x=350,y = 650)



window.mainloop()