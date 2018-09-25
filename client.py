# coding: utf-8
from threading import Thread
import socket
import sys


def menu():

    stop = False

    while not stop:
        print("")
        print("")
        print("-------------------------------")
        print('[1] - Listar registros')
        print('[2] - Adicionar registro')
        print('[3] - Atualizar registro')
        print('[4] - Excluir registro')
        print('[5] - Sair')

        # captura a opção desejada
        opt = str(input("Selecione uma opção: "))

        if opt == "1":

            # cria uma thread para executar a operação separadamente
            thread2 = Thread(target=send_message, args=('select', '', ''))
            thread2.start()
            thread2.join()

        elif opt == "2":

            value = input("Valor a ser adicionado: ")

            # cria uma thread para executar a operação separadamente
            thread3 = Thread(target=send_message, args=('insert', '', value))
            thread3.start()
            thread3.join()

        elif opt == "3":

            key = input("Digite a chave a ser atualizada: ")
            value = input("Digite o novo valor: ")

            # cria uma thread para executar a operação separadamente
            thread4 = Thread(target=send_message, args=('update', key, value))
            thread4.start()
            thread4.join()

        elif opt == "4":

            key = input("Digite a chave a ser deletada: ")

            # cria uma thread para executar a operação separadamente
            thread5 = Thread(target=send_message, args=('delete', key, ''))
            thread5.start()
            thread5.join()

        elif opt == "5":

            print("\n Fechando conexão")
            stop = True

        elif opt != "":

            print("\n Digite um comando válido")


def send_message(option, key, value):
    ''' Envia para o server.py as mensagens de CRUD através da porta 10001 '''

    message = str(option)+"/"+str(key)+"/"+str(value)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # cria um socket TCP que será utilizado para estabelecer a conexão

    server_address = ('localhost', 10001)
    print('Conectando a: {} porta: {}'.format(*server_address))
    sock.connect(server_address)
    # conectando no socket através da porta especificada

    try:
        print('enviando {!r}'.format(message))
        sock.sendall(message.encode('utf-8'))

        amount_received = 0
        amount_expected = len(message)

        '''
            vai lendo o socket de 1024 em 1024 bytes para não
            correr o risco de exceder o limite da pilha de memória
        '''
        while amount_received < amount_expected:
            data = sock.recv(1024)
            amount_received += len(data)
            print('recebendo {!r}'.format(data))

    finally:
        print('Fechando conexão')
        sock.close()


def clear():
    ''' Função para limpar o leitor de entrada do python '''
    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')

if __name__ == "__main__":
    # Verifica se a execução do python começou nesse arquivo

    t1 = Thread(target=menu)
    t1.setDaemon(True)
    t1.start()
    t1.join()
