# coding: utf-8
from threading import Thread
import socket
import sys


database = {}

def databaser(comand, key, value):

    print('[DB] Received: '+str(comand))

    if comand == 'select':
        # limpa a tela para evitar excesso de informação
        clear()
        print("[DB] Listando chave: "+str(key))

        msg = ''

        result = database.get(str(key))
        if result:
            msg = 'OK - Chave ' + key + ' / valor: ' + str(database[key])
        else:
            msg = 'NOK - Chave ' + key + ' não tem valores atribuídos'

        print(msg)
        return msg

    if comand == 'insert':
        # limpa a tela para evitar excesso de informação
        clear()
        print('[DB] Inserindo chave: '+str(key)+' / valor: '+str(value))

        result = database.get(str(key))
        if result:
            database[key] = bytearray(value, 'utf8')
            msg = "\n OK - Registro Adicionado"
        else:
            msg =  "\n NOK - Já existe um registro com essa chave"

        print(msg)
        return msg


    if comand == 'update':
        # limpa a tela para evitar excesso de informação
        clear()
        print('[DB] Atualizando chave: '+str(key))

        result = database.get(str(key))
        msg = ''

        if result:
            database[key] = bytearray(value, 'utf8')
            msg =  "\n OK - Registro Atualizado"
        else:
            msg =  "\n NOK - Chave não encontrada"

        print(msg)
        return msg

    if comand == 'delete':
        # limpa a tela para evitar excesso de informação
        clear()
        print('[DB] Removendo chave: '+str(key))

        result = database.get(str(key))
        msg = ''

        if result:
            database.pop(key)
            msg = "\n Registro Excluído"
        except Exception:
            msg = "\n NOK - Chave não encontrada"

        print(msg)
        return msg

    #print('[DB] Key: '+str(key))


def server():

    # cria um socket para comunicação via TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # configura o socket para receber comandos na porta 10001
    server_address = ('localhost', 10001)
    print('Iniciando conexão na {} porta {}'.format(*server_address))
    sock.bind(server_address)

    # começa a escutar
    sock.listen(1)

    while True:

        print('Esperando por conexões')
        connection, client_address = sock.accept()

        try:
            print('Conexão de', client_address)

            while True:

                # tenta ler o socket
                data = connection.recv(1024)

                print('recebido {!r}'.format(data))

                if data:
                    # caso tenha dados na conexão, tenta decodificar
                    comands = data.decode("UTF-8")
                    # separa os comandos para identificar o que deve ser feito
                    message = str(comands).split("/")
                    comand = message[0]
                    key = message[1]
                    value = message[2]

                    # chama a função que executa os comandos
                    back_message = databaser(comand, key, value)

                    # se o retorno for uma lista, transforma em string
                    if (type(back_message) == list):
                        back_message = ''.join(back_message)

                    print('enviando dados para o cliente')
                    connection.sendall(back_message.encode("UTF-8"))
                else:
                    print('no data from', client_address)
                    break

        finally:
            # fecha a conexão do socket
            connection.close()


def clear():
    ''' Função para limpar o leitor de entrada do python '''
    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')


if __name__ == "__main__":
    # Verifica se a execução do python começou nesse arquivo

    t1 = Thread(target = server)
    t1.setDaemon(True)
    t1.start()
    t1.join()
