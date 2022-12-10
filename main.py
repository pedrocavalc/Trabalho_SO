import datetime
import random
import time
from lib.config import config
from lib.classes import System, Process
from lib.interface import *

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
                    print(system.memory_table)
                    print(system.memory_positions)
                else:
                    aaa(f'Processo em espera{process.id, process.memory}')
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
            
# def best_fit(process_list,system):
#     process_running = []
#     process_queue = []
#     time_initial = time.time()
#     while True:
#         for process in process_list:
#                 flag = system.best_fit(process.memory,process.id)
#                 if flag == 0:
#                     process.run_time = time.time()
#                     print(f' processo de id {process.id} foi instanciado')
#                     print(system.memory_table)
#                     print(system.memory_positions) 
   
   
def main():
    '''
    Main function call, para configuração do sistema e escolha do algoritmo
    '''
    window = Tk()

    backgroundTop = (Image.open('assets/city.jpg'))
    resized_background_top = backgroundTop.resize((800,600), Image.ANTIALIAS)
    background_image_top = ImageTk.PhotoImage(resized_background_top)

    button_image_top = create_button(path_img='assets/start_button.png',scale=0.5)

    main_window(window, background_image_top, button_image_top)

    args = config(True)
    if(configs_dict != {}):
        system = System(**args)
        properties = vars(system)
        print(f'A configuração do sistema é:\n {properties}')
        process_list = create_processes(system)
        system.memory_structure()
        system.foot_algorithm(system.system_memory)
        if properties['strategy'] == 'first':
            first_fit(process_list,system)
        
        if properties['strategy'] == 'best':
            best_fit(process_list,system)

        if properties['strategy'] == 'worst':
            worst_fit(process_list,system)
    
    
    window.mainloop()
                
    

if __name__ == '__main__':
    main()
