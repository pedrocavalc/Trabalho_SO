from tkinter import *

from PIL import Image,ImageTk
from classes import System, Process
import datetime
import random
import time

plot_rectangles = False
global system

def create_processes(system):
    '''
    Função para a criação dos processos a serem alocados na memória
    '''
    process_list = []
    final_time = 0
    for id in range(system.num_process):
        id += 1
        create_time = random.randrange(system.interval_create[0],system.interval_create[1])
        create_time = create_time + final_time
        process = Process(system.interval_memory,create_time, system.interval_time,id)
        final_time = process.create_time
        process_list.append(process)
    for process in process_list:
        properties = vars(process)
        print(properties)
    return process_list
     
                 
def first_fit(process_list,system):
    '''
    Função para escalonamento de processos utilizando o algoritmo first_fit
    '''
    process_running = []
    process_queue = []
    time_initial = time.time()
    while True:
        for process in process_list:
            time_creation = process.create_time + time_initial
            if time.time() >= time_creation:
                flag = system.foot_algorithm(process.memory,process.id)
                if flag == 0:
                    process.run_time = time.time()
                    process_running.append(process)
                    process_list.remove(process)
                    print(f' processo de id {process.id} foi instanciado')
                    print(system.memory_table)
                    print(system.memory_positions)
                else:
                    print(f'Processo em espera{process.id, process.memory}')
                    process_queue.append(process)
                    process_list.remove(process)
                    break
        for i in range(len(process_queue)):
            flag = system.foot_algorithm(process_queue[0].memory,process_queue[0].id)
            if flag == 0:
                process_queue[0].run_time = time.time()
                print(f' processo de id {process_queue[0].id} foi instanciado')
                process_running.append(process_queue[0])
                process_queue.pop(0)
                print(system.memory_table)
                print(system.memory_positions)
            else:
                break         
        for process in process_running:
            time_stop = process.run_time + process.execution_time
            if time.time() >= time_stop:
                system.deallocate_process(process.id)
                print(system.memory_table)
                process_running.remove(process)
            else: 
                break
        if len(process_running) == 0 and len(process_list) == 0 and len(process_queue) == 0:
            print(process_running)
            print(system.memory_table)
            return 0

def best_fit(process_list,system):
    '''
    Função para escalonamento de processos utilizando o algoritmo best_fit
    '''
    process_running = []
    process_queue = []
    time_initial = time.time()
    while True:
        for process in process_list:
            time_creation = process.create_time + time_initial
            if time.time() >= time_creation:
                flag = system.best_fit_alloc(process.memory,process.id)
                if flag == 0:
                    process.run_time = time.time()
                    process_running.append(process)
                    process_list.remove(process)
                    print(f' processo de id {process.id} foi instanciado')
                    print(system.memory_table)
                    print(system.memory_positions)
                else:
                    print(f'Processo em espera{process.id, process.memory}')
                    process_queue.append(process)
                    process_list.remove(process)
                    break
        for i in range(len(process_queue)):
            flag = system.best_fit_alloc(process_queue[0].memory,process_queue[0].id)
            if flag == 0:
                process_queue[0].run_time = time.time()
                print(f' processo de id {process_queue[0].id} foi instanciado')
                process_running.append(process_queue[0])
                process_queue.pop(0)
                print(system.memory_table)
                print(system.memory_positions)
            else:
                break         
        for process in process_running:
            time_stop = process.run_time + process.execution_time
            if time.time() >= time_stop:
                system.deallocate_process(process.id)
                print(system.memory_table)
                process_running.remove(process)
            else: 
                break
        if len(process_running) == 0 and len(process_list) == 0 and len(process_queue) == 0:
            print(process_running)
            print(system.memory_table)
            return 0


def worst_fit(process_list,system):
    '''
    Função para escalonamento de processos utilizando o algoritmo worst_fit
    '''
    process_running = []
    process_queue = []
    time_initial = time.time()
    while True:
        for process in process_list:
            time_creation = process.create_time + time_initial
            if time.time() >= time_creation:
                flag = system.worst_fit_alloc(process.memory,process.id)
                if flag == 0:
                    process.run_time = time.time()
                    process_running.append(process)
                    process_list.remove(process)
                    print(f' processo de id {process.id} foi instanciado')
                    print(system.memory_table)
                    print(system.memory_positions)
                else:
                    print(f'Processo em espera{process.id, process.memory}')
                    process_queue.append(process)
                    process_list.remove(process)
                    break
        for i in range(len(process_queue)):
            flag = system.worst_fit_alloc(process_queue[0].memory,process_queue[0].id)
            if flag == 0:
                process_queue[0].run_time = time.time()
                print(f' processo de id {process_queue[0].id} foi instanciado')
                process_running.append(process_queue[0])
                process_queue.pop(0)
                print(system.memory_table)
                print(system.memory_positions)
            else:
                break         
        for process in process_running:
            time_stop = process.run_time + process.execution_time
            if time.time() >= time_stop:
                system.deallocate_process(process.id)
                print(system.memory_table)
                process_running.remove(process)
            else: 
                break
        if len(process_running) == 0 and len(process_list) == 0 and len(process_queue) == 0:
            print(process_running)
            print(system.memory_table)
            return 0
            



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
    pass


def click_top_button():
        global canvas, plot_rectangles, imgCaixa, window
        print(num_process.get())
        configs_dict = {
        'num_process': int(num_process.get()),
        'strategy': strategy.get(),
        'memory_size': int(memory_size.get()),
        'system_memory':int(memory_system.get()),
        'interval_memory': tuple(int(elemento) for elemento in interval_memory.get().split()),
        'interval_create': tuple(int(elemento) for elemento in interval_create.get().split()),
        'interval_time': tuple(int(elemento) for elemento in interval_time.get().split())
        }

        print(configs_dict)
        system = System(**configs_dict)
        properties = vars(system)
        print(f'A configuração do sistema é:\n {properties}')
        process_list = create_processes(system)
        system.memory_structure()
        system.foot_algorithm(system.system_memory)


        pile_size = len(system.memory_table)
        page_size = 500/pile_size
        count = 0
        count2 = 0
        for i in range(pile_size):
            print(i)
            y0 = 50 + count
            count = count + page_size
            y1 = 58 + count2
            count2 = count2 + page_size
            variavel = canvas.create_rectangle(500, y0, 300, y1)
            
        
        window.update()

        if properties['strategy'] == 'first':
            first_fit(process_list,system)

        if properties['strategy'] == 'best':
            best_fit(process_list,system)

        if properties['strategy'] == 'worst':
            worst_fit(process_list,system)

        

# inicializando a janela
window = Tk()
# min e max size da janela
window.minsize(800,600)
window.maxsize(800,600)
window.configure(bg=rgb_to_hex((204,255,255)))


# criando um canvas
canvas = Canvas(window,width = 800, height = 800)
canvas.pack()

canvas.create_rectangle(500, 50, 300, 500)
# if(plot_rectangles == True):
#     pile_size = len(system.memory_table)
#     page_size = 500/pile_size
#     count = 0
#     count2 = 0
#     for i in range(pile_size):
#         print(i)
#         y0 = 50 + count
#         count = count + page_size
#         y1 = 58 + count2
#         count2 = count2 + page_size
#         variavel = canvas.create_rectangle(500, y0, 300, y1)
    

# setando o back ground
background = (Image.open('assets/background.png'))
resized_background = background.resize((800,500), Image.ANTIALIAS)
background_image = ImageTk.PhotoImage(resized_background)


top= Toplevel(window)

canvasTop = Canvas(top ,width = 800,height = 800)
canvasTop.pack()
backgroundTop = (Image.open('assets/city.jpg'))
resized_background_top = backgroundTop.resize((800,600), Image.ANTIALIAS)
background_image_top = ImageTk.PhotoImage(resized_background_top)

button_image_top = create_button(path_img='assets/start_button.png',scale=0.5)

canvasTop.create_image(0,0,anchor=NW,image = background_image_top)
imgCaixa = create_button("assets/caixa.png", 0.1)
top.minsize(800,600)
top.maxsize(800,600)

top.title("Iniciar programa")

t_text = Label(top,text='Insira a quantidade de processos',font=('Cascadia Code SemiBold',10), bg='#696969', fg='#fff')
t_text.place(x = 50, y = 50)
num_process= Entry(top,width = 5,font=('Arial',20))
num_process.place(x=50,y = 80)

t_text = Label(top,text='Insira a estrategia(first, best ou worst)',font=('Cascadia Code SemiBold',10), bg='#696969', fg='#fff')
t_text.place(x = 50, y = 120)
strategy = Entry(top,width = 5,font=('Arial',20))
strategy.place(x=50,y = 150)

t_text = Label(top,text='Insira o tamanho da memória',font=('Cascadia Code SemiBold',10), bg='#696969', fg='#fff')
t_text.place(x = 50, y = 190)
memory_size = Entry(top,width = 5,font=('Arial',20))
memory_size.place(x=50,y = 220)

t_text = Label(top,text='Insira a quantidade de memoria do sistema',font=('Cascadia Code SemiBold',10), bg='#696969', fg='#fff')
t_text.place(x = 50, y = 260)
memory_system = Entry(top,width = 5,font=('Arial',20))
memory_system.place(x=50,y = 290)

t_text = Label(top,text='Insira o range do intervalo de memoria(separado por espaço)',font=('Cascadia Code SemiBold',10), bg='#696969', fg='#fff')
t_text.place(x = 50, y = 330)
interval_memory = Entry(top,width = 5,font=('Arial',20))
interval_memory.place(x=50,y = 360)

t_text = Label(top,text='Insira o range do intervalo de tempo de criação de processos(separado por espaço)',font=('Cascadia Code SemiBold',10), bg='#696969', fg='#fff')
t_text.place(x = 50, y = 400)
interval_create = Entry(top,width = 5,font=('Arial',20))
interval_create.place(x=50,y = 430)

t_text = Label(top,text='Insira o range do intervalo de execução dos processos(separado por espaço)',font=('Cascadia Code SemiBold',10), bg='#696969', fg='#fff')
t_text.place(x = 50, y = 470)
interval_time = Entry(top,width = 5,font=('Arial',20))
interval_time.place(x=50,y = 500)

initial_button = Button(top, bd ='2',command=click_top_button)
initial_button.config(image = button_image_top)
initial_button.place(x = 340,y = 530)

window.mainloop()

