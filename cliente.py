from threading import Thread

keys = []
bytes = []

database = {'keys': keys, 'bytes': bytes}


def databaser(comand, key, value):

    print('[DB] Received: '+str(comand))

    if comand == 'select':
        keys = database['keys']
        for key in keys:
            print('[IDX:'+str(key)+'] - '+str(database['bytes'][key])+'')


    if comand == 'insert':
        print('[DB] Inserting: '+str(value))
        count = len(database['keys'])
        database['keys'].append(count)
        database['bytes'].append(bytearray(value, 'utf8'))


    if comand == 'update':
        print('[DB] Updating Key: '+str(key))
        database['bytes'][int(key)] = bytearray(value, 'utf8')


    if comand == 'delete':
        print('[DB] Deleting Key: '+str(key))
        database['bytes'][int(key)] = None


    #print('[DB] Key: '+str(key))


def menu():

    count = 0

    stop = False

    while not stop:

        print('[1] - Listar registros')
        print('[2] - Adicionar registro')
        print('[3] - Atualizar registro')
        print('[4] - Excluir registro')
        print('[5] - Sair')

        opt = input("Selecione um comando:")

        if opt == "1": 
            print("\n Listando registros")

            thread2 = Thread(target = databaser, args = ('select','',''))
            thread2.start()
            thread2.join()


        elif opt == "2":
            print("\n Registro Adicionado") 
            
            thread3 = Thread(target = databaser, args = ('insert','','11'))
            thread3.start()
            thread3.join()
            
        elif opt == "3":
            print("\n Registro Atualizado")

            thread3 = Thread(target = databaser, args = ('update','2','22'))
            thread3.start()
            thread3.join()

        elif opt == "4":
            print("\n Registro Excluído") 

            thread4 = Thread(target = databaser, args = ('delete','4',''))
            thread4.start()
            thread4.join()

        elif opt == "5":
            print("\n Fechando conexão")
            stop = True 
        elif opt !="":
            print("\n Digite um comando válido") 



if __name__ == "__main__":

    t1 = Thread(target = menu)
    t1.setDaemon(True)
    t1.start()

    while True:
      pass