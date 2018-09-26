# coding: utf-8
from threading import Thread
import socket
import sys
import os.path
import os


keys = []
bytes = []
database = {'keys': keys, 'bytes': bytes}
operations = []


def databaser(comand, key, value):

    print('[DB] Received: '+str(comand))

    if comand == 'select':
        # limpa a tela para evitar excesso de informação
        clear()
        print("[DB] SELECT:")

        keys = database['keys']
        response = []

        if len(keys) > 0:
            for key in keys:
                msg = 'id {0}: <{1}>'.format(key, database['bytes'][key])
                print(msg)
                response.append(msg)
        else:
            msg = "Tabela vazia"
            print(msg)
            response = [msg]

        return ', '.join(response)

    if comand == 'insert':
        # limpa a tela para evitar excesso de informação
        clear()
        print('[DB] INSERT: '+str(value))

        count = len(database['keys'])
        database['keys'].append(count)
        database['bytes'].append(bytearray(value, 'utf8'))
        print("\n Registro Adicionado")
        return str("\n Registro Adicionado")

    if comand == 'update':
        # limpa a tela para evitar excesso de informação
        clear()
        print('[DB] UPDATE: key '+str(key))

        try:
            database['bytes'][int(key)] = bytearray(value, 'utf8')
            print("\n Registro Atualizado")
            return str("\n Registro Atualizado")
        except Exception:
            print("\n Chave não encontrada")
            return str("\n Chave não encontrada")

    if comand == 'delete':
        # limpa a tela para evitar excesso de informação
        clear()
        print('[DB] DELETE: key '+str(key))

        try:
            database['bytes'][int(key)] = None
            print("\n Registro Excluído")
            return str("\n Registro Excluído")
        except Exception:
            print("\n Chave não encontrada")
            return str("\n Chave não encontrada")

    # print('[DB] Key: '+str(key))


def server():

    if os.path.isfile('db.txt'):
        try:
            file = open('db.txt', 'r')

            for line in file.read().split('\n'):
                message = line.split("/")
                comand = message[0]
                key = message[1]
                value = message[2]
                databaser(comand, key, value)

            file.close()
        except:
            print('erro ao abrir arquivo')

    file = open('db.txt', 'a')

    try:
        # cria um socket para comunicação via TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)

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

                        if comand in ['insert', 'update', 'delete']:
                            operations.append(comands)
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
    except:
        print('Timeout de 5 segundos atingido')
    finally:
        if operations:
            for operation in operations:
                file.writelines(operation)
            file.write('\n')
        file.close()


def clear():
    ''' Função para limpar o leitor de entrada do python '''
    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')


if __name__ == "__main__":
    # Verifica se a execução do python começou nesse arquivo

    t1 = Thread(target=server)
    t1.setDaemon(True)
    t1.start()
    t1.join()
