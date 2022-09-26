from http import client
from threading import Thread
from multiprocessing import Semaphore
from multiprocessing import BoundedSemaphore
from random import randint
import time

nCaixas = 2
# 2 clientes
waiting = 0

count = 0

qtdClientes = 2
s_caixas = Semaphore(0)
s_atendimento = Semaphore(0)
s_clientes = Semaphore(nCaixas)
s_mutex = Semaphore(nCaixas)
l_clientes = []
l_caixas = []
lista = []
caixasLivres = nCaixas

class Cliente(Thread):
    def __init__(self, id, ta, senha):
        Thread.__init__(self)
        self.id = id
        self.ta = ta
        self.senha = senha

    def run(self):
        global caixasLivres, waiting
        s_clientes.acquire()
        s_mutex.release()
        waiting += 1
        s_atendimento.release()

        print(f"{self.id} está sendo atendido \n \n")
        
        t_end = time.time() + self.ta
        while time.time() < t_end:
            a=1

        s_caixas.release()

        print(f"Fim do atendimento de {self.id}")
        print("=========================================")

class Caixa(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id = id

    def run(self):
        
        while True:
            global waiting, caixasLivres
            s_mutex.acquire()
            if waiting > 0:
                waiting -= 1
                print(f"O caixa {self.id} está atendendo um cliente \n \n")
                s_caixas.acquire()
                print(f"O caixa {self.id} está livre \n \n")

                s_clientes.release()
            else:
                s_atendimento.acquire()


def criarCliente(nClientes):
    global waiting
    if nClientes > 0:
        for i in range(nClientes):
            id = i + 1
            ta = 10
            senha = i + 1
            Cliente(id, ta, senha).start()


if __name__ == "__main__":
    for j in range(nCaixas):
        l_caixas.append(Caixa(count+1))
        count+=1

    for caixa in l_caixas:
        caixa.start()

    nClientes = 4
    lista = criarCliente(nClientes)
