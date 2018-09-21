from threading import Thread

keys = []
bytes = []

database = {'keys': keys, 'bytes': bytes}


def databaser(comand, key, value):

    print('[DB] Received: '+str(comand))

    if comand == 'select':

        clear()
        print("[DB] Listing:")

        keys = database['keys']

        if len(keys) > 0:
            for key in keys:
                print('[IDX:'+str(key)+'] - '+str(database['bytes'][key])+'')
        else:
            print("\n Tabela vazia")

    if comand == 'insert':

        clear()
        print('[DB] Inserting: '+str(value))

        count = len(database['keys'])
        database['keys'].append(count)
        database['bytes'].append(bytearray(value, 'utf8'))
        print("\n Registro Adicionado")


    if comand == 'update':

        clear()
        print('[DB] Updating Key: '+str(key))

        try:
            database['bytes'][int(key)] = bytearray(value, 'utf8')
            print("\n Registro Atualizado")
        except Exception:
            print("\n Chave não encontrada")

    if comand == 'delete':
        clear()
        print('[DB] Deleting Key: '+str(key))

        try:
            database['bytes'][int(key)] = None
            print("\n Registro Excluído")
        except Exception:
            print("\n Chave não encontrada")
         


    #print('[DB] Key: '+str(key))


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

        opt = input("Selecione uma opção:")

        if opt == "1": 

            thread2 = Thread(target = databaser, args = ('select','',''))
            thread2.start()
            thread2.join()

        elif opt == "2":
            
            value = input("Valor a ser adicionado:")

            thread3 = Thread(target = databaser, args = ('insert', '', value))
            thread3.start()
            thread3.join()
            
        elif opt == "3":

            key = input("Digite a chave a ser atualizada:")
            value = input("Digite o novo valor:")

            thread3 = Thread(target = databaser, args = ('update', key, value))
            thread3.start()
            thread3.join()

        elif opt == "4":

            key = input("Digite a chave a ser deletada:")

            thread4 = Thread(target = databaser, args = ('delete', key, ''))
            thread4.start()
            thread4.join()

        elif opt == "5":

            print("\n Fechando conexão")
            stop = True 

        elif opt !="":

            print("\n Digite um comando válido") 


def clear():
    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')

if __name__ == "__main__":

    t1 = Thread(target = menu)
    t1.setDaemon(True)
    t1.start()
    t1.join()