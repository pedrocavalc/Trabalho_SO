from pickle import FALSE, TRUE
from threading import Thread
from multiprocessing import Semaphore
import time

nClientes = 4
nCaixas = 2
waiting = 0
count = 0

s_caixas = Semaphore(0)
s_atendimento = Semaphore(nCaixas)
s_clientes = Semaphore(nCaixas)
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
        global TAC
        s_clientes.acquire()
        s_caixas.release()
        
        TAC = self.ta
        for caixa in l_caixas:
            if caixa.disponivel == TRUE:
                
                caixa_cliente = caixa
                
                break

        print(f"{self.id} está sendo atendido por {caixa_cliente.id}\n \n")
        
        t_end = time.time() + self.ta
        while time.time() < t_end:
            a=1



        print(f"Fim do atendimento de {self.id}")
        print("=========================================")
        

class Caixa(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id = id
        self.disponivel = TRUE

    def run(self):
            global TAC
            while True:
                s_caixas.acquire()
                

                print(f"O caixa {self.id} está atendendo um cliente \n \n")
                self.disponivel = FALSE
                
                t_end = time.time() + TAC
                while time.time() < t_end:
                    a=1


                print(f"O caixa {self.id} está livre \n \n")
                self.disponivel = TRUE

                s_clientes.release()

        


def criarCliente(nClientes):
    global waiting
    if nClientes > 0:
        for i in range(nClientes):
            id = i + 1
            ta = int(input("Informe o TA: "))
            senha = i + 1
            Cliente(id, ta, senha).start()


if __name__ == "__main__":
    for j in range(nCaixas):
        l_caixas.append(Caixa(count+1))
        count+=1

    for caixa in l_caixas:
        caixa.start()

    criarCliente(nClientes)
