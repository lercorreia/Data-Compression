import random
import glob
import time
import random
import numpy as np
from pathlib import Path
from struct import *

import os
random.seed(2000)

from collections import Counter


def dic(size):
    dicionario = {}
    for i in range(size):
        dicionario[chr(i)] = i
    return dicionario


value = 9

def lzw_test(dicionario, test_sample):
    target = Path(test_sample)
    size = len(dicionario)
    k = value
    max_size = 2**k
    lzw_msg = []
    file = open(target, encoding="latin-1")
    msg = file.read()

    anterior = ""

    for i in range(len(msg)):
        atual = msg[i] + anterior
        if atual in dicionario:
            anterior = atual
        else:
            lzw_msg.append(dicionario[anterior])
            anterior = msg[i]
        if anterior in dicionario:
            lzw_msg.append(dicionario[anterior])

    file.close()
    return len(lzw_msg)


def lzw_pastas(data):
    size = 256
    k = value
    dicionario = dic(size)
    max_size = 2**k
    for imagem in data:
        tpath = Path(imagem)
        lzw_msg = []
        file = open(tpath, encoding="latin-1")
        msg = file.read()
        anterior = ""
        for i in range(len(msg)):
            atual = msg[i] + anterior
            if atual in dicionario:
                anterior = atual
            else:
                lzw_msg.append(dicionario[anterior])
                if len(dicionario) <= max_size:
                    dicionario[atual] = size
                    size += 1
                anterior = msg[i]
        if anterior in dicionario:
            lzw_msg.append(dicionario[anterior])
        file.close()

    return {"categoria": data[0].split("\\")[1], "dicionario": dicionario}



def knn_categoria(data, x, k):
    distances = []
    for dictio in data:
        dist = lzw_test(dictio["dicionario"], x)
        distances.append([dist, dictio["categoria"]])
    distances.sort(key=lambda x: x[0])  # Ordena as distâncias em ordem crescente
    k_nearest = distances[:k]  # Seleciona os K vizinhos mais próximos, no caso k=1
    
    return k_nearest[0][1]  # Retorna a categoria da imagem enviada para teste


diretorio = glob.glob("data/*")
pastas = [[] for _ in range(len(diretorio))]
teste_imagem = []
teste_categoria = []

for i, dir in enumerate(diretorio):
    images = glob.glob(dir + "/*")
    random.shuffle(images)

    categoria = dir.split("\\")[1]
    teste_imagem.append(images[5])
    teste_categoria.append(categoria)
    images.pop(5)
    for img in images[:9]:
        pastas[i].append(img)

    

print("Começo dos testes")
inicio = time.time()

dicionario_pastas = []
for p in pastas:
    dicionario_pastas.append(lzw_pastas(p))

knn_categoria = [knn_categoria(data=dicionario_pastas, x=x, k=1) for x in teste_imagem]

fim = time.time()
print("Tempo de execução: ", round(fim - inicio, 2), " s")

print("categorias")
print(knn_categoria)
print("teste_categoria")


categorias = np.array(knn_categoria)
teste_categoria = np.array(teste_categoria)
print(teste_categoria)
taxa_acerto = 0
for i in range(len(categorias)):
    if categorias[i] == teste_categoria[i]:
        taxa_acerto+=1

taxa_acerto = taxa_acerto/len(teste_categoria)
print("Taxa de acerto:")
print(taxa_acerto)