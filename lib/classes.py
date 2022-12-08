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
                print(self.memory_positions)
                return 0
            else:
                #print(f'O process {id} não pode ser alocado pois não há espaço suficiente')
                return 1
            
    def best_fit(self,memory,id):
        '''
        Algoritmo de best fit 
        '''
        process_pages = self.split_process(memory,id)
        self.max_table()
        table_names = self.memory_positions.keys()
        print(self.memory_positions['table1']['tamanho'])
        menor_tam = self.memory_positions['table1']['tamanho']
        index = 0
        for i, table in enumerate(table_names):
            tam = self.memory_positions[table]['tamanho']
            if tam < menor_tam:
                menor_tam = tam
                index = i
        #print(table[i])
        
            
        
        
        
    def allocate_process(self,process_pages,index_init,id = 0):
        '''
        Método para alocar a memória do processo
        '''
        index_end = index_init + process_pages
        for i in range(index_init, index_end):
            self.memory_table[i] = id
        #print(self.memory_table)
        self.max_table()
        
    def deallocate_process(self,id):
        self.memory_table = [None if x == id else x for x in self.memory_table]
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
        