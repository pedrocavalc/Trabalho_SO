from tkinter import *

from PIL import Image,ImageTk
import datetime
import random
import time

plot_rectangles = False
rectangles_dict = {}
global system

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
        self.rectangles = []
    
    def memory_structure(self):
        '''
        Método para criação da tabela de endereçamento de memória
        '''
        page_size = 30
        num_pages = int(self.memory_size / page_size)
        self.memory_table = [None] * num_pages
        print(self.memory_table)
        print(f'O número de páginas para alocação de memória é {len(self.memory_table)}')

    def split_process(self,process_memory,id):
        '''
        Método para calcular o número de páginas que o processo necessita
        '''
        page_size = 30
        num_pages = math.ceil(process_memory / page_size)
        #print(f'O número de páginas ocupadas pelo processo de id: {id} é {num_pages}')
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
        for i, page in enumerate(self.memory_table):
            if page == None and count == 0:
                index_init = i
                count = 1
            if (page != None and count == 1) or (i == len(self.memory_table)-1 and count == 1):
                index_end = i
                table_id +=1
                if index_end == len(self.memory_table) - 1:
                    self.memory_positions[f'table{table_id}'] = {'table_init':index_init,'table_end':index_end,'tamanho':index_end + 1 - index_init}
                else:
                    self.memory_positions[f'table{table_id}'] = {'table_init':index_init,'table_end':index_end,'tamanho':index_end - index_init}
                count = 0
                 
    
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
                print(f'pode ser alocado a partir da posição {index_init} utilizando {process_pages} páginas de tamanho')
            
    
    def foot_algorithm(self,memory,id=0):
        '''
        Algoritmo baseline
        '''
        process_pages = self.split_process(memory,id)
        self.max_table()
        table_names = self.memory_positions.keys()
        for table in table_names:
            tam = self.memory_positions[table]['tamanho']
            if process_pages < tam: # Se houver alguma tabela com páginas suficientes na memória aloca o processo
                index_init = self.memory_positions[table]['table_init']
                #print(f'O processo {id} pode ser alocado a partir da posição {index_init} utilizando {process_pages} páginas de tamanho')
                self.allocate_process(process_pages,index_init,id)
                #print(self.memory_positions)
                return 0
            else:
                #print(f'O process {id} não pode ser alocado pois não há espaço suficiente')
                return 1
            
    def best_fit_alloc(self,memory,id):
        '''
        Algoritmo de best fit 
        '''
        process_pages = self.split_process(memory,id)
        self.max_table()
        sorted_keys = sorted(self.memory_positions, key=lambda x: self.memory_positions[x]['tamanho'])

        for i, table in enumerate(sorted_keys):
            tam = self.memory_positions[table]['tamanho']
            if process_pages < tam: # Se houver alguma tabela com páginas suficientes na memória aloca o processo
                index_init = self.memory_positions[table]['table_init']
                #print(f'O processo {id} pode ser alocado a partir da posição {index_init} utilizando {process_pages} páginas de tamanho')
                self.allocate_process(process_pages,index_init,id)
                #print(self.memory_positions)
                return 0
            else:
                #print(f'O process {id} não pode ser alocado pois não há espaço suficiente')
                return 1
        

    def worst_fit_alloc(self,memory,id):
        '''
        Algoritmo de best fit 
        '''
        process_pages = self.split_process(memory,id)
        self.max_table()
        sorted_keys = sorted(self.memory_positions, key=lambda x: self.memory_positions[x]['tamanho'], reverse=True)
        
        for i, table in enumerate(sorted_keys):
            tam = self.memory_positions[table]['tamanho']
            if process_pages < tam: # Se houver alguma tabela com páginas suficientes na memória aloca o processo
                index_init = self.memory_positions[table]['table_init']
                #print(f'O processo {id} pode ser alocado a partir da posição {index_init} utilizando {process_pages} páginas de tamanho')
                self.allocate_process(process_pages,index_init,id)
                #print(self.memory_positions)
                return 0
            else:
                #print(f'O process {id} não pode ser alocado pois não há espaço suficiente')
                return 1
            
        
        
        
    def allocate_process(self,process_pages,index_init,id = 0):
        '''
        Método para alocar a memória do processo
        '''
        global rectangles_dict, window
        index_end = index_init + process_pages
        for i in range(index_init, index_end):
            self.memory_table[i] = id
            self.rectangles.append(canvas.create_rectangle(rectangles_dict[f'{i}']['x0'], rectangles_dict[f'{i}']['y0'], rectangles_dict[f'{i}']['x1'], rectangles_dict[f'{i}']['y1'], fill='blue'))
            
        window.update()
        #print(self.memory_table)
        self.max_table()
        
    def deallocate_process(self,id):
        global canvas, window
        self.memory_table = [None if x == id else x for x in self.memory_table]
        for i in self.rectangles:
            canvas.delete(i)
        window.update()
        self.max_table()
        #(self.memory_positions)
        print(f'processo de id {id} foi desalocado')

            
        
        
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
        global canvas, plot_rectangles, imgCaixa, window, rectangles_dict
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
        pile_size = len(system.memory_table)
        page_size = 500/pile_size
        count = 0
        count2 = 0
        for i in range(pile_size):
            y0 = 50 + count
            count = count + page_size
            y1 = 58 + count2
            count2 = count2 + page_size
            canvas.create_rectangle(500, y0, 300, y1)

            actual_dict = {
                'x0': 500,
                'y0': y0,
                'x1': 300,
                'y1': y1,
            }

            rectangles_dict[f'{i}'] = actual_dict

        window.update()
        system.foot_algorithm(system.system_memory)

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

