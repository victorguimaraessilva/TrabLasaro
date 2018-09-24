from threading import Thread
import socket
import sys


keys = []
bytes = []

database = {'keys': keys, 'bytes': bytes}

def databaser(comand, key, value):

    print('[DB] Received: '+str(comand))

    if comand == 'select':
        clear()
        print("[DB] Listing:")

        keys = database['keys']
        response = []
        
        if len(keys) > 0:
            for key in keys:
                print('[IDX:'+str(key)+'] - '+str(database['bytes'][key])+'')
                response.append(str('[IDX:'+str(key)+'] - '+str(database['bytes'][key])+''))
        else:
            print("\n Tabela vazia")
            return str("\n Tabela vazia")

        return response

    if comand == 'insert':
        clear()
        print('[DB] Inserting: '+str(value))

        count = len(database['keys'])
        database['keys'].append(count)
        database['bytes'].append(bytearray(value, 'utf8'))
        print("\n Registro Adicionado")
        return str("\n Registro Adicionado")


    if comand == 'update':
        clear()
        print('[DB] Updating Key: '+str(key))

        try:
            database['bytes'][int(key)] = bytearray(value, 'utf8')
            print("\n Registro Atualizado")
            return str("\n Registro Atualizado")
        except Exception:
            print("\n Chave não encontrada")
            return str("\n Chave não encontrada")

    if comand == 'delete':
        clear()
        print('[DB] Deleting Key: '+str(key))

        try:
            database['bytes'][int(key)] = None
            print("\n Registro Excluído")
            return str("\n Registro Excluído")
        except Exception:
            print("\n Chave não encontrada")
            return str("\n Chave não encontrada")
         

    #print('[DB] Key: '+str(key))


def server():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 10001)
    print('Iniciando conexão na {} porta {}'.format(*server_address))
    sock.bind(server_address)

    sock.listen(1)

    while True:

        print('Esperando por conexões')
        connection, client_address = sock.accept()

        try:
            print('Conexão de', client_address)

            while True:

                data = connection.recv(1024)

                print('recebido {!r}'.format(data))

                if data:
                    comands = data.decode("UTF-8")
                    message = str(comands).split("/")
                    comand = message[0]
                    key = message[1]
                    value = message[2]

                    back_message = databaser(comand, key, value)

                    if (type(back_message) == list):
                        back_message = ''.join(back_message)

                    print('enviando dados para o cliente')
                    connection.sendall(back_message.encode("UTF-8"))
                else:
                    print('no data from', client_address)
                    break

        finally:
            # Clean up the connection
            connection.close()


def clear():
    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')


if __name__ == "__main__":

    t1 = Thread(target = server)
    t1.setDaemon(True)
    t1.start()
    t1.join()