def config(debug=False):
    '''
    Função para configuração da simulação
    '''
    if debug:
        args = {'num_process':4,'strategy':'best','memory_size':2000,'system_memory':500,'interval_memory':(200,300),'interval_create':(1,2),'interval_time':(6,10)}
        return args
    args = {}
    args['num_process'] = int (input('Digite o numero de processos a serem criados\n'))
    args['strategy'] = input('Digite o algoritmo a ser utilizado\n')
    args['memory_size'] = int(input('Digite o tamanho de memória virtual a ser criado\n'))
    args['memory_system'] = int(input('Digite o tamanho de memória a ser ocupado pelo SO\n'))
    interval_memory = input('Digite o intervalo de memória a ser usado para criação de processos\n')
    args['interval_memory'] = tuple(int(elemento) for elemento in interval_memory.split())
    interval_create = input('Digite o intervalo de tempo no qual os processos serão criados\n')
    args['interval_create'] = tuple(int(elemento) for elemento in interval_create.split())
    interval_time = input('Digite o intervalo dos tempos de execução dos processos\n')
    args['interval_time'] = tuple(int(elemento) for elemento in interval_time.split())
    return args