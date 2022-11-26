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
    
    
    def memory_structure(self):
        '''
        Método para criação da tabela de endereçamento de memória
        '''
        page_size = 30
        num_pages = int(self.memory_size / page_size)
        self.memory_table = [None] * num_pages
        print(self.memory_table)
        print(f'O número de páginas para alocação de memória é {len(self.memory_table)}')

    def split_process(self,process_memory):
        '''
        Método para calcular o número de páginas que o processo necessita
        '''
        page_size = 30
        num_pages = math.ceil(process_memory / page_size)
        print(f'O número de páginas ocupadas pelo processo é {num_pages}')
        return num_pages
    
    
    def max_table(self):
        self.memory_positions = {}
        index_init = 0
        index_end = 0
        count = 0
        for i, page in enumerate(self.memory_table):
            if page == None and count == 0:
                index_init = i
                count = 1
            if (page != None and count == 1) or (i == len(self.memory_table)-1 and count == 1):
                index_end = i
                self.memory_positions[f'table{i}'] = {'table_init':index_init,'table_end':index_end,'tamanho':index_end - index_init}
                count = 0
                 
        print(self.memory_positions)
    
    def allocate_SO(self,memory):
        '''
        Método para alocar a memória do processo
        '''
        process_pages = self.split_process(memory)
        self.max_table()
        for i in range(process_pages):
            self.memory_table[i] = 1
        print(self.memory_table)
        self.max_table()

            
        
        
class Process():
    def __init__(self,interval_memory,interval_create,interval_time):
        '''
        Método para a instanciação de um processo dentro do intervalo
        '''
        self.memory = random.randrange(interval_memory[0],interval_memory[1])
        self.create_time = random.randrange(interval_create[0],interval_create[1])
        self.execution_time = random.randrange(interval_time[0],interval_time[1])
        
    def dealocate(self):
        pass

