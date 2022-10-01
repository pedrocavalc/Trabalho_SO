from os import popen
from tkinter import *
import tkinter
from PIL import Image,ImageTk
ID = 0
SENHA = 0
TEMPO = 0

def rgb_to_hex(rgb):
    '''
    Função para converter hex to rgb
    '''
    return "#%02x%02x%02x" % rgb  

def click_start():
    '''
    Função para lidar com o click do botão start
    '''
    print(f'cliente criado com id: {ID}, senha: {SENHA}, tempo: {TEMPO}')
    ID = 0
    SENHA = 0
    TEMPO = 0

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
    if TEMPO == 0:
        print('invalido')
    else:
        print(TEMPO)
# inicializando a janela
window = Tk()

# min e max size da janela
window.minsize(1366,768)
window.maxsize(1366,768)
window.configure(bg=rgb_to_hex((204,255,255)))

# criando um canvas
canvas = Canvas(window,width = 1366,height = 600)
canvas.pack()

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

tempo_atendimento_text = Label(window,text='Insira o tempo de atendimento',font=('Arial',10))
tempo_atendimento_text.place(x = 350, y = 630)
tempo_atendimento_entry = Entry(window,width = 5,font=('Arial',20))
tempo_atendimento_entry.place(x=350,y = 650)



window.mainloop()