import collections
from operator import le
from typing import Dict
import unidecode
import math
from unicodedata import normalize
import codecs
import string

# Remove pontos e acentos
def PalavrasChave(palavra):
	termo = palavra.translate(str.maketrans('','',string.punctuation))
	termo = unidecode.unidecode(termo)
	termo = termo.lower()
	return termo 

# Abre um arquivo e retorna a lista com seus termos
def LeArquivo(nome):
	lista = []
	arquivo = open(nome, "r")
	for linha in arquivo:
		for palavra in linha.split():
			termo = PalavrasChave(palavra)
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
			print(" Doc ",i,": ",end="")
			print("{:.2f}".format(tf_idf[item][i]), " ", end="")
		print()
	return tf_idf
			
def menu():
	print("<<Organização e Recuperação da Informação>>")
	print("1 - Criar Vocabulário")
	print("2 - Imprime Bag of Words")
	print("3 - Calcular o TF-IDF")
	print("4 - Sair")
	

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
			case _:
				break


if __name__ == "__main__": 
    main()


			