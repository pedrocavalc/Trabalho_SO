from tkinter import *
import tkinter
from tkinter.scrolledtext import ScrolledText
from tokenize import Double
from PIL import Image,ImageTk
from threading import Thread
from multiprocessing import Semaphore
import time
import sys

CLIENTS_COUNT = 0
ID = 0
id = 0
SENHA = 0
TEMPO = 0
CAIXAS_COUNT = 0
s_caixas = Semaphore(0)
s_clientes = Semaphore()
s_mutex = Semaphore(1)
l_caixas = []
TAC = 0


class Cliente(Thread):
    def __init__(self, id, ta, senha):
        Thread.__init__(self)
        self.id = id
        self.ta = ta
        self.senha = senha

    def run(self):
        global TAC, canvas, clientImage, l_caixas
        drawClient = canvas.create_image(0, 500, anchor=NW, image=clientImage)
        s_clientes.acquire()
        
        s_mutex.acquire()
        TAC = int(self.ta)
        i = 0
        for caixa in l_caixas:
            if caixa.disponivel == True:
                
                caixa_cliente = caixa
                caixa_cliente.disponivel = False
                
                break


        while i < 350 + ((int(caixa_cliente.id) - 1) * 140):
            canvas.move(drawClient, 10, 0)
            i = i + 10
        
        s_caixas.release()
        

        print(f"{self.id} está sendo atendido por {caixa_cliente.id}\n \n")
        
        t_end = time.time() + int(self.ta)
        while time.time() < t_end:
            a=1

        canvas.delete(drawClient)

        print(f"Fim do atendimento de {self.id}\n")
        print("=========================================\n")
        

class Caixa(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id = id
        self.disponivel = TRUE
        self.ta = 0

    def run(self):
            global TAC
            while True:
                s_caixas.acquire()             
                t_end = time.time() + TAC
                s_mutex.release()
                print(f"O caixa {self.id} está atendendo um cliente \n \n")
                self.disponivel = False
                
                
                while time.time() < t_end:
                    a=1


                print(f"O caixa {self.id} está livre \n \n")
                self.disponivel = TRUE

                s_clientes.release()

        

class PrintLogger(object):  # create file like object
    def __init__(self, textbox):  # pass reference to text widget
        self.textbox = textbox  # keep ref
    def write(self, text):
        self.textbox.configure(state="normal")  # make field editable
        self.textbox.insert("end", text)  # write text to textbox
        self.textbox.see("end")  # scroll to end
        self.textbox.configure(state="disabled")  # make field readonly
    def flush(self):  # needed for file like object
        pass




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
    global CLIENTS_COUNT, id
    TEMPO = tempo_atendimento_entry.get()
    if TEMPO.strip() == '':
        print('invalido')
    id = id + 1
    ta = TEMPO
    senha = CLIENTS_COUNT + 1
    Cliente(id, ta, senha).start()


def click_initial_button():
    global s_clientes, l_caixas, CAIXAS_COUNT, img, canvas, imgCaixa
    num_Caixas = t_entry.get()
    for i in range(int(num_Caixas)):
        l_caixas.append(Caixa(CAIXAS_COUNT+1))
        CAIXAS_COUNT+=1

        drawCaixa = canvas.create_image(350 + (i*140), 440, anchor=NW, image=imgCaixa)



    for caixa in l_caixas:
        caixa.start()
    s_clientes = Semaphore(int(num_Caixas))



# inicializando a janela
window = Tk()
# min e max size da janela
window.minsize(1366,768)
window.maxsize(1366,768)
window.configure(bg=rgb_to_hex((204,255,255)))

imgCaixa = create_button("assets/caixa.png", 0.15)

# criando um canvas
canvas = Canvas(window,width = 1366,height = 600)
canvas.pack()



# setando o back ground
background = (Image.open('assets/background.png'))
resized_background = background.resize((1366,600), Image.ANTIALIAS)
background_image = ImageTk.PhotoImage(resized_background)


top= Toplevel(window)

canvasTop = Canvas(top ,width = 500,height = 500)
canvasTop.pack()

backgroundTop = (Image.open('assets/city.jpg'))
resized_backgroundTop = backgroundTop.resize((500,500), Image.ANTIALIAS)
background_imageTop = ImageTk.PhotoImage(resized_backgroundTop)

canvasTop.create_image(0,0,anchor=NW,image = background_imageTop)

top.minsize(500,500)
top.maxsize(500,500)
top.title("Quantidade de caixas")
t_text = Label(top,text='Insira a quantidade de caixas',font=('Cascadia Code SemiBold',10), bg='#696969', fg='#fff')
t_text.place(x = 150, y = 190)
t_entry = Entry(top,width = 5,font=('Arial',20))
t_entry.place(x=210,y = 220)

initial_img = create_button(path_img='assets/start_button.png',scale=0.5)
initial_button = Button(top, bd ='2',command=click_initial_button)
initial_button.config(image = initial_img)
initial_button.place(x = 180,y = 270)


# colocando o background na janela
canvas.create_image(0,0,anchor=NW,image = background_image)


clientImage = create_button('assets/client.png', 0.125)


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

log_widget = ScrolledText(window, height=10, width=70, font=("consolas", "8", "normal"))
log_widget.pack()
log_widget.place(x = 900, y =620)

logger = PrintLogger(log_widget)
sys.stdout = logger
sys.stderr = logger



window.mainloop()