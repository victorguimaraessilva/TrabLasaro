
import socket
import sys
import time
import string
import re
import threading
import time
import thread
import fileserver
import merkletree


# Definindo var. globais
get = "GET"
put = "PUT"
post = "POST"
delete = "DELETE"
header = "HEAD"
__metaclass__ = type


def recebe_handler(socket):
    """Manuseia o recebimento de dados pelo cliente."""
    message = ''
    cccc = "\n\n"
    ccc = "\r\n\r\n"
    c = "\n\n\n"
    cc = "\r\n\r\n\r\n"
    while 1:
        message += socket.recv(1024)
        # print message
        metodo, caminhoSplitado, corpo, tamanho = Parsing(message)
        # print corpo
        if metodo == get:
            if ccc in message or cccc in message:
                break
        elif metodo == header:
            if ccc in message or cccc in message:
                break
        elif metodo == delete:
            if ccc in message or cccc in message:
                break
        elif metodo == put:
            if tamanho is None:
                if cc in message or c in message:
                    break
            if tamanho is not None:
                if int(len(corpo)) >= int(tamanho):
                    break
        elif metodo == post:
            if tamanho is None:
                if cc in message or c in message:
                    break
            if tamanho is not None:
                if int(len(corpo)) >= int(tamanho):
                    break
    metodo, caminhoSplitado, corpo, tamanho = Parsing(message)
    return metodo, caminhoSplitado, corpo, tamanho


def metodo_handler(metodo, caminho, corpo):
    """Definindo qual metodo e qual handler usar, retorna mensagem."""
    if metodo == get:
        objeto = acha_objeto(caminho)
        resposta = Get_Handler(objeto)
        # fazer a mensagem correta com o codigo e os dados
        return resposta
    elif metodo == post:
        resposta = Post_Handler(caminho, corpo)
        return resposta
    elif metodo == put:
        objeto = acha_objeto(caminho)
        resposta = Put_Handler(objeto, corpo)
        return resposta
    elif metodo == delete:
        objeto = acha_objeto(caminho)
        resposta = Delete_Handler(objeto)
        return resposta
    elif metodo == header:
        objeto = acha_objeto(caminho)
        resposta = Header_Handler(objeto)
        return resposta


def acha_objeto(caminho):
    """Procura o objeto no qual o caminho termina."""
    nodo = fileserver.root
    if len(caminho) == 1 and caminho[0] == '':
        return fileserver.root
    elif caminho[0] != '':
        for i in range(0, len(fileserver.root.filhos), 1):
            if caminho[0] == fileserver.root.filhos[i].nome:
                nodo = fileserver.root.filhos[i]
        for i in range(1, len(caminho), 1):
            for j in range(0, len(nodo.filhos), 1):
                if caminho[i] == nodo.filhos[j].nome:
                    nodo = nodo.filhos[j]
                    break
    if caminho[len(caminho)-1] != nodo.nome:
        nodo = None
        return None
    elif caminho[len(caminho)-1] == nodo.nome:
        return nodo


def Parsing(message):
    """Faz parsing e separa uma lista para o metodo e caminhos splitados."""
    caminhos = message.split("/")
    del caminhos[0]
    return caminhos


def traduz(mensagem):
    """Coloca mensagem em plaintext."""
    mensagem = mensagem.replace("\n", " ")
    return mensagem


def msg200_OK(metodo, objeto):
    """Definindo a mensagem 200 OK."""
    msg = ('HTTP/1.1 ' + str(metodo) + ' 200 OK\n')
    msg2 = ('Version: ' + str(objeto.version) + '\n'
            + 'Creation: ' + str(objeto.created) + '\n'
            + 'Modification: ' + str(objeto.modified) + '\n')
    if metodo != delete:
        msg += msg2
    if objeto.data is None:
        objeto.data = "None"
    corpo = ('Content_Length: ' + str(len(objeto.data)))
    dados = ('\n\n' + str(objeto.data))
    if metodo == header:
        msg += corpo
    if metodo == get:
        msg += corpo
        msg += dados
    return msg


def msg403_Forbidden(metodo, objeto):
    """Definindo mensagem de acesso nao autorizado."""
    msg = "HTTP/1.1 403 Forbidden"
    if metodo == post:
        msg += ('\nVersion: ' + str(objeto.version) + '\n'
                + 'Creation: ' + str(objeto.created) + '\n'
                + 'Modification: ' + str(objeto.modified) + '\n')
    return msg


def msg201_Created():
    """Definindo mensagem 201, Created."""
    msg = """HTTP/1.1 201 Created\nContent-Type: text/html\nConnection: Closed\r\n\r\n
        <!DOCTYPE HTML PUBLIC>
        <html><head>
        <title>201 Created</title>
        </head><body>
        </body></html>"""
    return msg


def msg_204NoContent():
    """Definindo mensagem 204."""
    msg = """HTTP/1.1 204 No content\nContent-Type: text/html\nConnection: Closed\r\n\r\n
        <!DOCTYPE HTML PUBLIC>
        <html><head>
        <title>204 No content</title>
        </head><body>
        </body></html>"""
    return msg


def msg_400BadRequest():
    """Definindo mensagem 400."""
    msg = "HTTP/1.1 400 Bad request"
    return msg


def msg_404NotFound():
    """Definindo mensagem."""
    msg = "HTTP/1.1 404 Not Found"
    return msg


def Get_Handler(objeto):
    """Manejamento do GET."""
    if objeto is None:
        mensagem = msg_404NotFound()
    else:
        mensagem = msg200_OK(get, objeto)
    # Fazer a mensagem correta junto com a msg
    return mensagem


def Post_Handler(caminho, dados):
    """Manejamento do POST(cria)."""
    nodo = fileserver.root
    # checa se o caminho 'e a propria raiz
    if len(caminho) == 1 and caminho[0] == '':
        message = msg_400BadRequest()
        return message
    # acha ate o ultimo nodo que existe no caminho e devolve ele em nodo
    elif caminho[0] != '':
        for i in range(0, len(caminho), 1):
            for j in range(0, len(nodo.filhos), 1):
                if caminho[i] == nodo.filhos[j].nome:
                    nodo = nodo.filhos[j]
                    break
            # devolve a posicao do caminho que ele difere de um existente
            pos = i
            if caminho[i] != nodo.nome:
                pos = i
                break
    if caminho[pos] == nodo.nome:
        msg = msg403_Forbidden(post, nodo)
        return msg
    novonodo = fileserver.arquivo(caminho[pos])
    nodo.insere(novonodo)
    ptnodo = novonodo
    # aloca os novos nodos dependendo de quantos vierem no request
    for k in range(pos+1, len(caminho), 1):
        novonodo = fileserver.arquivo(caminho[k])
        # achar um meio de renomear os novos nodos para insercao
        ptnodo.insere(novonodo)
        ptnodo = novonodo
    ptnodo.data = dados
    message = msg200_OK(post, novonodo)
    return message


def Delete_Handler(objeto):
    """Manejamento do DELETE."""
    if objeto is None:
        mensagem = msg403_Forbidden(delete, objeto)
    else:
        objeto.remove_arq()
        mensagem = msg200_OK(delete, objeto)
    return mensagem


def Put_Handler(objeto, dados):
    """Manejamento do PUT(modifica dados)."""
    if objeto is None:
        mensagem = msg403_Forbidden(put, objeto)
    else:
        objeto.insere_dados(dados)
        objeto.version += 1
        mensagem = msg200_OK(put, objeto)
    return mensagem


def Header_Handler(objeto):
    """Manejamento do Header."""
    if objeto is None:
        mensagem = msg_404NotFound()
    else:
        mensagem = msg200_OK(header, objeto)
    return mensagem
