from tkinter import *

from PIL import Image,ImageTk
from tkinter.scrolledtext import ScrolledText
import datetime
import random
import time
import sys

plot_rectangles = False
rectangles_dict = {}

import random
import math

class System():
    def __init__(self, num_process, strategy, memory_size, system_memory, interval_memory, interval_create, interval_time):
        self.num_process = num_process
        self.strategy = strategy
        self.memory_size = memory_size
        self.system_memory = system_memory
        self.interval_memory = interval_memory
        self.interval_create = interval_create
        self.interval_time = interval_time
        self.rect_dict = {}
        self.label_dict = {}
        self.empty_labels = []
    
    def memory_structure(self):
        '''
        Método para criação da tabela de endereçamento de memória
        '''
        page_size = 30
        num_pages = int(self.memory_size / page_size)
        self.memory_table = [None] * num_pages

    def split_process(self,process_memory,id):
        '''
        Método para calcular o número de páginas que o processo necessita
        '''
        page_size = 30
        num_pages = math.ceil(process_memory / page_size)
        return num_pages
    
    
    def max_table(self):
        '''
        Função responsável por gerenciar as posições de memorias livres e seus respectivos tamanhos
        '''
        self.memory_positions = {}
        index_init = 0
        index_end = 0
        table_id = 0
        count = 0

        for i in self.empty_labels:
            i.destroy()
        self.empty_labels.clear()

        for i, page in enumerate(self.memory_table):
            if page == None and count == 0:
                index_init = i
                count = 1
            if (page != None and count == 1) or (i == len(self.memory_table)-1 and count == 1):
                index_end = i
                table_id +=1
                if index_end == len(self.memory_table) - 1:
                    self.memory_positions[f'table{table_id}'] = {'table_init':index_init,'table_end':index_end,'tamanho':index_end + 1 - index_init}

                    label = Label(window,text=f'tam: {index_end + 1 - index_init }',font=('Cascadia Code SemiBold',9), bg=rgb_to_hex((204,255,255)))
                    self.empty_labels.append(label)

                else:
                    self.memory_positions[f'table{table_id}'] = {'table_init':index_init,'table_end':index_end,'tamanho':index_end - index_init}

                    label = Label(window,text=f'tam: {index_end - index_init}',font=('Cascadia Code SemiBold',9), bg=rgb_to_hex((204,255,255)))
                    self.empty_labels.append(label)

                count = 0
                y_label = ((rectangles_dict[f'{round(index_init)}']['y0'] + rectangles_dict[f'{round(index_init)}']['y1'])/2)
                label.place(x = 350, y = y_label)

        # label = Label(window,text=f'Process {id}',font=('Cascadia Code SemiBold',9), bg=rgb_to_hex((204,255,255)))
        # self.label_dict[f'{id}'] = label
        # y_label = ((rectangles_dict[f'{i}']['y0'] + rectangles_dict[f'{i}']['y1'])/2)
        # label.place(x = 200, y = y_label - 50)
                 
    
    def test(self,id='bebug'):
        '''
        Função para testar
        '''
        process_pages = self.split_process(500)
        self.max_table()
        table_names = self.memory_positions.keys()
        for table in table_names:
            tam = self.memory_positions[table]['tamanho']
            if process_pages < tam:
                index_init = self.memory_positions[table]['table_init']
            
    
    def first_fit_alloc(self,memory,id=0):
        '''
        Algoritmo baseline
        '''
        process_pages = self.split_process(memory,id)
        self.max_table()
        table_names = self.memory_positions.keys()
        if len(table_names) != 0:
            for table in table_names:
                tam = self.memory_positions[table]['tamanho']
                if process_pages <= tam: # Se houver alguma tabela com páginas suficientes na memória aloca o processo
                    index_init = self.memory_positions[table]['table_init']
                    #print(f'O processo {id} pode ser alocado a partir da posição {index_init} utilizando {process_pages} páginas de tamanho')
                    self.allocate_process(process_pages,index_init,id)
                    sucess = True
                    break
                    #print(self.memory_positions)
                else:
                    #print(f'O process {id} não pode ser alocado pois não há espaço suficiente')
                    sucess = False
            if(sucess):
                return 0
            else:
                return 1
        else:
            return 1



            
    def best_fit_alloc(self,memory,id):
        '''
        Algoritmo de best fit 
        '''
        process_pages = self.split_process(memory,id)
        self.max_table()
        sorted_keys = sorted(self.memory_positions, key=lambda x: self.memory_positions[x]['tamanho'])
        if len(sorted_keys) != 0:
            for i, table in enumerate(sorted_keys):
                tam = self.memory_positions[table]['tamanho']
                if process_pages <= tam: # Se houver alguma tabela com páginas suficientes na memória aloca o processo
                    index_init = self.memory_positions[table]['table_init']
                    #print(f'O processo {id} pode ser alocado a partir da posição {index_init} utilizando {process_pages} páginas de tamanho')
                    self.allocate_process(process_pages,index_init,id)
                    sucess = True
                    break
                    #print(self.memory_positions)
                else:
                    #print(f'O process {id} não pode ser alocado pois não há espaço suficiente')
                    sucess = False
            if(sucess):
                return 0
            else:
                return 1
        else:
            return 1
        

    def worst_fit_alloc(self,memory,id):
        '''
        Algoritmo de best fit 
        '''
        process_pages = self.split_process(memory,id)
        self.max_table()
        sorted_keys = sorted(self.memory_positions, key=lambda x: self.memory_positions[x]['tamanho'], reverse=True)
        
        if len(sorted_keys) != 0:
            for i, table in enumerate(sorted_keys):
                tam = self.memory_positions[table]['tamanho']
                if process_pages <= tam: # Se houver alguma tabela com páginas suficientes na memória aloca o processo
                    index_init = self.memory_positions[table]['table_init']
                    #print(f'O processo {id} pode ser alocado a partir da posição {index_init} utilizando {process_pages} páginas de tamanho')
                    self.allocate_process(process_pages,index_init,id)
                    sucess = True
                    break
                    #print(self.memory_positions)
                else:
                    #print(f'O process {id} não pode ser alocado pois não há espaço suficiente')
                    sucess = False
            if(sucess):
                return 0
            else:
                return 1
        else:
            return 1
            
        
        
        
    def allocate_process(self,process_pages,index_init,id = 0):
        '''
        Método para alocar a memória do processo
        '''
        global rectangles_dict, window
        index_end = index_init + process_pages
        number_of_colors = 8
        color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_colors)]
        rectangles = []
        for i in range(index_init, index_end):
            self.memory_table[i] = id
            rectangles.append(canvas.create_rectangle(rectangles_dict[f'{i}']['x0'], rectangles_dict[f'{i}']['y0'], rectangles_dict[f'{i}']['x1'], rectangles_dict[f'{i}']['y1'], fill=color[0]))
        
        label = Label(window,text=f'Process {id}',font=('Cascadia Code SemiBold',9), bg=rgb_to_hex((204,255,255)))
        self.label_dict[f'{id}'] = label
        y_label = ((rectangles_dict[f'{i}']['y0'] + rectangles_dict[f'{i}']['y1'])/2)
        label.place(x = 80, y = y_label - 30)
        self.rect_dict[f'{id}'] = rectangles
            
        #print(self.memory_table)
        self.max_table()
        
    def deallocate_process(self,id):
        global canvas, window
        self.memory_table = [None if x == id else x for x in self.memory_table]
        for i in self.rect_dict[f'{id}']:
            canvas.delete(i)
        self.label_dict[f'{id}'].destroy()
        self.max_table()
        #(self.memory_positions)

            
        
        
class Process():
    def __init__(self,interval_memory,create_time,interval_time,id):
        '''
        Método para a instanciação de um processo dentro do intervalo
        '''
        self.memory = random.randrange(interval_memory[0],interval_memory[1])
        self.create_time = create_time
        self.execution_time = random.randrange(interval_time[0],interval_time[1])
        self.id = id
        

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
    return process_list

queue_labels_list = []
def plot_queue(process_queue):
    y = 50
    for i in queue_labels_list:
        i.destroy()
    queue_labels_list.clear()
    for i in process_queue:
        label = Label(window,text=f'Processo {i.id} em espera, precisa de {math.ceil(i.memory / 30)} MU',font=('Cascadia Code SemiBold',9), bg='red')
        queue_labels_list.append(label)

        label.place(x = 500, y = y)
        y = y + 25
     
                 
def first_fit(process_list,system):
    '''
    Função para escalonamento de processos utilizando o algoritmo first_fit
    '''
    process_running = []
    process_queue = []
    time_initial = time.time()
    while True:
        plot_queue(process_queue)
        for process in process_list:
            time_creation = process.create_time + time_initial
            if time.time() >= time_creation:
                flag = system.first_fit_alloc(process.memory,process.id)
                if flag == 0:
                    process.run_time = time.time()
                    process_running.append(process)
                    process_list.remove(process)

                else:
                    print(f'Processo {process.id} em espera, precisa de {math.ceil(process.memory / 30)} MU')
                    process_queue.append(process)
                    process_list.remove(process)
                    break
        for i in range(len(process_queue)):
            flag = system.first_fit_alloc(process_queue[0].memory,process_queue[0].id)
            if flag == 0:
                process_queue[0].run_time = time.time()
                process_running.append(process_queue[0])
                process_queue.pop(0)

            else:
                break         
        for process in process_running:
            time_stop = process.run_time + process.execution_time
            if time.time() >= time_stop:
                system.deallocate_process(process.id)
                process_running.remove(process)
            else: 
                break
        window.update()
        if len(process_running) == 0 and len(process_list) == 0 and len(process_queue) == 0:

            return 0
        

def best_fit(process_list,system):
    '''
    Função para escalonamento de processos utilizando o algoritmo best_fit
    '''
    process_running = []
    process_queue = []
    time_initial = time.time()
    # system.allocate_process(10,30,10)
    # system.allocate_process(10,50,11)
    while True:
        plot_queue(process_queue)
        for process in process_list:
            time_creation = process.create_time + time_initial
            if time.time() >= time_creation:
                flag = system.best_fit_alloc(process.memory,process.id)
                if flag == 0:
                    process.run_time = time.time()
                    process_running.append(process)
                    process_list.remove(process)
      
                else:
                    print(f'Processo {process.id} em espera, precisa de {math.ceil(process.memory / 30)} MU')
                    process_queue.append(process)
                    process_list.remove(process)
                    break
        for i in range(len(process_queue)):
            flag = system.best_fit_alloc(process_queue[0].memory,process_queue[0].id)
            if flag == 0:
                process_queue[0].run_time = time.time()
                process_running.append(process_queue[0])
                process_queue.pop(0)
 
            else:
                break         
        for process in process_running:
            time_stop = process.run_time + process.execution_time
            if time.time() >= time_stop:
                system.deallocate_process(process.id)
                process_running.remove(process)
            else: 
                break
        window.update()
        if len(process_running) == 0 and len(process_list) == 0 and len(process_queue) == 0:

            return 0


def worst_fit(process_list,system):
    '''
    Função para escalonamento de processos utilizando o algoritmo worst_fit
    '''
    process_running = []
    process_queue = []
    time_initial = time.time()
    while True:
        plot_queue(process_queue)
        for process in process_list:
            time_creation = process.create_time + time_initial
            if time.time() >= time_creation:
                flag = system.worst_fit_alloc(process.memory,process.id)
                if flag == 0:
                    process.run_time = time.time()
                    process_running.append(process)
                    process_list.remove(process)

                else:
                    print(f'Processo {process.id} em espera, precisa de {math.ceil(process.memory / 30)} MU')
                    process_queue.append(process)
                    process_list.remove(process)
                    break
        for i in range(len(process_queue)):
            flag = system.worst_fit_alloc(process_queue[0].memory,process_queue[0].id)
            if flag == 0:
                process_queue[0].run_time = time.time()
                process_running.append(process_queue[0])
                process_queue.pop(0)

            else:
                break         
        for process in process_running:
            time_stop = process.run_time + process.execution_time
            if time.time() >= time_stop:
                system.deallocate_process(process.id)
                process_running.remove(process)
            else: 
                break
        window.update()
        if len(process_running) == 0 and len(process_list) == 0 and len(process_queue) == 0:

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



def click_top_button():
        global canvas, plot_rectangles, imgCaixa, window, rectangles_dict
        configs_dict = {
        'num_process': int(num_process.get()),
        'strategy': strategy.get(),
        'memory_size': int(memory_size.get()),
        'system_memory':int(memory_system.get()),
        'interval_memory': tuple(int(elemento) for elemento in interval_memory.get().split()),
        'interval_create': tuple(int(elemento) for elemento in interval_create.get().split()),
        'interval_time': tuple(int(elemento) for elemento in interval_time.get().split())
        }

        system = System(**configs_dict)

        properties = vars(system)
        process_list = create_processes(system)
        system.memory_structure()
        pile_size = len(system.memory_table)
        page_size = 500/pile_size
        count = 0
        count2 = 0
        for i in range(pile_size):
            y0 = 50 + count
            count = count + page_size
            y1 = 50 + page_size + count2
            count2 = count2 + page_size
            canvas.create_rectangle(150, y0, 350, y1)

            actual_dict = {
                'x0': 150,
                'y0': y0,
                'x1': 350,
                'y1': y1,
            }

            rectangles_dict[f'{i}'] = actual_dict

        window.update()
        system.first_fit_alloc(system.system_memory)
        # system.allocate_process(5, 30, 10)
        # system.allocate_process(5, 50, 11)


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
resized_background = background.resize((800,600), Image.ANTIALIAS)
background_image = ImageTk.PhotoImage(resized_background)
canvas.create_image(0,0,anchor=NW,image = background_image)

label = Label(window,text=f'Lista de espera:',font=('Cascadia Code SemiBold',12), bg='red')

label.place(x = 500, y = 25)


top= Toplevel(window)

canvasTop = Canvas(top ,width = 800,height = 800)
canvasTop.pack()
backgroundTop = (Image.open('assets/background.png'))
resized_background_top = backgroundTop.resize((800,600), Image.ANTIALIAS)
background_image_top = ImageTk.PhotoImage(resized_background_top)

button_image_top = create_button(path_img='assets/start_button.png',scale=0.5)

canvasTop.create_image(0,0,anchor=NW,image = background_image_top)
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

