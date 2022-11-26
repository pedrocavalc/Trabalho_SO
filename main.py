from lib.config import config
from lib.classes import System, Process

def create_processes(system):
    '''
    Função para a criação dos processos a serem alocados na memória
    '''
    process_list = []
    for i in range(system.num_process):
        process = Process(system.interval_memory,system.interval_create, system.interval_time)
        process_list.append(process)
    for process in process_list:
        properties = vars(process)
        print(properties)
    return process_list
            
   
def main():
    args = config(True)
    system = System(**args)
    properties = vars(system)
    print(f'A configuração do sistema é:\n {properties}')
    process_list = create_processes(system)
    system.memory_structure()
    system.allocate_SO(system.system_memory)

if __name__ == '__main__':
    main()
