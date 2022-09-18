import collections
import unidecode
import math
import re
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from operator import le
from typing import Dict
from unicodedata import normalize
from nltk.stem.snowball import SnowballStemmer

# Remove pontos e acentos
def PalavrasChave(palavra):
    termo = unidecode.unidecode(palavra.lower())
    termo = termo.replace(',','')
    termo = termo.replace('.','')
    termo = termo.replace('\n','')
    termo = termo.replace('!','')
    termo = termo.replace('-','')
    termo = termo.replace(',','')
    termo = termo.replace('ã','a')
    termo = termo.replace('õ','o')
    termo = termo.replace('á','a')
    termo = termo.replace('é','e')
    termo = termo.replace('í','i')
    termo = termo.replace('ú','u')
    termo = termo.replace('ó','o')
    termo = termo.replace('à','a')
    termo = termo.replace('ç','c')
    termo = termo.strip('"')
    termo = re.sub(r'[0-9]+','',termo)
    return termo

# Abre um arquivo e retorna a lista com seus termos
def LeArquivo(nome):
	stop_words = set(stopwords.words('portuguese')) 
	stemmer = SnowballStemmer("portuguese")
	lista = []
	arquivo = open(nome, "r")
	for linha in arquivo:
		for palavra in linha.split():
			termo = PalavrasChave(palavra)
			if not termo in stop_words:
				termo = stemmer.stem(termo)
				lista.append(termo)
	arquivo.close()	
	return lista 

# Ordena e remove termos repetidos de uma lista
def CriaIndex(Lista):
    index = list(dict.fromkeys(Lista))
    index.sort()
    return index

# Cria um arquivo texto
def EscreveArq(nome, lista):
    nome = open(nome, "w")
    for cont in lista:
        nome.write(cont)
        nome.write("\n")
    nome.close()

def CriarVocabulario():
    diretorio = input("Pasta com documentos: ")
    quantidade = int(input("Numero de arquivos: "))
    vocab = []

    for i in range(quantidade):
        doc = input("Nome do documento: ")
        str = diretorio + "/" + doc
        vocab.extend(LeArquivo(str))

    vocab = CriaIndex(vocab)

    arq = input("Nome do arquivo vocabulario: ")
    EscreveArq(arq,vocab)
    print("Arquivo com vocabulario criado")	

def ExtraiTermos():
    arq = input("Nome do arquivo vocabulario: ")
    vocab = []
    vocab = LeArquivo(arq)

    matrix = {}

    diretorio = input("Pasta com documentos: ")
    qtd = int(input("Quantidade de aquivos: "))
    for i in range(qtd):
        arq = input("Nome do arquivo: ")
        doc = diretorio + "/" + arq;
        aux = LeArquivo(doc)
        frequency = collections.Counter(aux)
        matrix[i] = frequency

    return matrix, vocab, qtd

# Imprime a Bag Of Words
def BagOfWords():
    matrix, vocab, qtd = ExtraiTermos()

    similaridade = False

    for i in range(qtd):
        print("Documento ",(i+1),": ",end="")
        print("[",end="")
        for termo in vocab:
            if(matrix[i][termo] != 0) : 
                print("1,", end="")	
            else: print("0,", end="")
        print("]")

def CalcularTF(matrix, vocab, qtd):
    tf = collections.defaultdict(dict)
    for item in vocab:
        for i in range(qtd):
            if matrix[i][item] == 0 :
                tf[item][i] = 0
            else: 
                tf[item][i] = 1 + math.log(matrix[i][item],2)

    return tf

def CalcularIDF(matrix, vocab, qtd):
    idf = collections.defaultdict(dict)

    for item in vocab:
        n = 0
        for i in range(qtd):
            if matrix[i][item]!=0 : n+=1
        if n == 0 :
            idf[item] = 0
        else: 
            idf[item] = math.log((qtd/n),2)

    return idf

def CalcularTFIDF():
    matrix, vocab, qtd = ExtraiTermos()

    tf = CalcularTF(matrix, vocab, qtd)
    idf = CalcularIDF(matrix, vocab, qtd)

    tf_idf = collections.defaultdict(dict)

    for item in vocab:
        for i in range(qtd):
            tf_idf[item][i] = idf[item] * tf[item][i]

    for item in vocab:
        n = 0
        print(item," ", end="")
        for i in range(qtd):
            print("  Doc ",(i+1),":  ",end="")
            print("{:.2f}".format(tf_idf[item][i]), " ", end="")
        print()
        
    return tf_idf, vocab, idf, qtd

def CalcularTFIDF_Consulta(vocab, idf):
	# TF-IDF da consulta
	string = input("Digite uma consulta: ")
	consulta = string.split()

	lista = []

	stop_words = set(stopwords.words('portuguese')) 
	stemmer = SnowballStemmer("portuguese")

	for item in consulta:
		termo = PalavrasChave(item)
		if not termo in stop_words:
			termo = stemmer.stem(termo)
			lista.append(termo)


	matrix = {}
	matrix[0] = collections.Counter(lista)
	tf_vocab = CalcularTF(matrix, vocab, 1)
	tf_idf_consulta = collections.defaultdict(dict)
	for item in idf:
		tf_idf_consulta[item] = round((idf[item] * tf_vocab[item][0]), 2)

	return tf_idf_consulta

def CalcularVetorial():
	tf_idf, vocab, idf, qtd = CalcularTFIDF()
	tf_idf_consulta = CalcularTFIDF_Consulta(vocab, idf)

	modulo_consulta = 0
	for item in tf_idf_consulta:
		modulo_consulta = modulo_consulta + pow(tf_idf_consulta[item],2)
	modulo_consulta = math.sqrt(modulo_consulta)

	modulo_matrix = collections.defaultdict(dict)
	for i in range(qtd):
		cont = 0
		for item in tf_idf_consulta:
			cont = cont + pow(tf_idf[item][i],2)
		modulo_matrix[i] = math.sqrt(cont)	

	ranking = collections.defaultdict(dict)
	aux = 0

	for i in range(qtd):
		for item in vocab:
			aux = aux + (tf_idf[item][i] * tf_idf_consulta[item])
			if (modulo_matrix[i] * modulo_consulta) !=0 :
				ranking[i] = round(aux/(modulo_matrix[i] * modulo_consulta),2)
		aux = 0
		print("SIM(D",(i+1),", Q) = ",ranking[i], sep="")

def menu():
    print("<<Organização e Recuperação da Informação>>")
    print("1 - Criar Vocabulário")
    print("2 - Imprime Bag of Words")
    print("3 - Calcular o TF-IDF")
    print("4 - Calcular o Modelo Vetorial")
    print("5 - Sair")

# Programa main
def main():
    while True:
        menu()
        opcao = int(input("Digite uma opcao: "))
        match opcao:
            case 1:
                CriarVocabulario()
            case 2:
                BagOfWords()
            case 3:
                CalcularTFIDF()
            case 4:
                CalcularVetorial()
            case _:
                break

if __name__ == "__main__": 
    main()

            
            
        
    
        
    
    
    

