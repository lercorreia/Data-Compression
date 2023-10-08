import time
import struct 

def compressor_lzw(data, max_dict_size):
    dicionario = {bytes([i]): i for i in range(256)} #Cria um dicionário com chave inteira e valores em bytes (dicionario ascii)
    dict_size = 256 #Define o tamanho base do dicionário
    resultado = bytearray() #Cria um array de bytes para armazenar o resultado
    buffer = b'' #indica que o buffer armazenará bytes
    i = 0
    while i < len(data):
        symbol = bytes([data[i]]) #pega o próximo simbolo
        if buffer + symbol in dicionario:   #verifica se a nova sequencia esta no dicionario
            buffer += symbol    #Se estiver, coloca no buffer
        else:
            code = dicionario[buffer]   #Caso não esteja, pega o codigo do buffer
            resultado += struct.pack('<H', code)    #coloca o buffer no array que fica a descompressão
            if dict_size < max_dict_size:   # coloca a nova sequencia que nao estava no dicionario
                dicionario[buffer + symbol] = dict_size 
                dict_size += 1
                
            buffer = symbol
        i += 1
    code = dicionario[buffer]
    resultado += struct.pack('<H', code)
    return resultado, dict_size

def descompressor_lzw(data, max_dict_size):
    dicionario = {i: bytes([i]) for i in range(256)}    #Cria um dicionário com chaves em bytes e os valores inteiros
    dict_size = 256
    resultado = bytearray()
    buffer = b'' #buffer em binario
    i = 0
    while i < len(data):
        code = struct.unpack('<H', data[i:i+2])[0]  #desempacota de 2 em 2 bytes
        i += 2
        if code in dicionario:  #verifica se o codigo esta no dicionario
            value = dicionario[code]
        elif code == dict_size: #caso nao esteja, cria uma nova sequencia acrescentando o primeiro caractere do buffer no final
            value = buffer + buffer[0:1]
        
        resultado += value  #coloca o valor na variável que guarda o resultado da descompressão
        if buffer:  # coloca novas sequencias no dicionário
            if dict_size < max_dict_size:   
                dicionario[dict_size] = buffer + value[0:1]
                dict_size += 1
                
            buffer = value
        else:
            buffer = value
    return resultado, dict_size


def Teste(k, filename):
    max_dict_size = 2**k  # Tamanho máximo do dicionário
    data = open(filename, 'rb').read()

    compressed_data, dictSizeCompressao = compressor_lzw(data, max_dict_size)

    compressed_filename = 'exemplo_comprimido_' + filename
    with open(compressed_filename, 'wb') as f:
        f.write(compressed_data)

    data2 = open(compressed_filename, 'rb').read()
    decompressed_data, dict_sizeD = descompressor_lzw(data2, max_dict_size)
    decompressed_filename = 'exemplo_descomprimido_' + filename
    with open(decompressed_filename, 'wb') as f:
        f.write(decompressed_data)


    return f'Tamanho máximo do dicionário: {max_dict_size}, tamanho dicionário compressão:{dictSizeCompressao}, razão de compressão: {len(data)/len(compressed_data):.2f}, razão de compressão 2° fórmula: {len(data)/((len(compressed_data)*k)/8):.2f} \n'

filename = 'disco.mp4'
filename2 = 'corpus16MB.txt'

with open('DADOS.txt', 'w', encoding='utf-8') as arquivo:
    arquivo.write("Arquivo: " + filename + "\n\n")
    for k in range(9, 17):
        start_time = time.time()
        text = Teste(k, filename)
        end_time = time.time()
        execution_time = end_time - start_time
        
        print("Para K =", k, "Tempo:", execution_time, "segundos", file=arquivo)
        print(text, file=arquivo)

    arquivo.write("\n\n\nArquivo: " + filename2 + "\n\n")
    for k in range(9, 17):
        start_time = time.time()
        text = Teste(k, filename2)
        end_time = time.time()
        execution_time = end_time - start_time
        
        print("Para K =", k, "Tempo:", execution_time, "segundos", file=arquivo)
        print(text, file=arquivo)

