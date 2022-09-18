import csv
import math
import itertools
import collections
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

class Ponderacao_Termos:
	def TF(matrix, vocab, qtd):
		tf = collections.defaultdict(dict)
		for item in vocab:
			for i in range(qtd):
				if matrix[i][item] == 0 :
					tf[item][i] = 0
				else: 
					tf[item][i] = 1 + math.log(matrix[i][item],2)

		return tf

	def IDF(matrix, vocab, qtd):
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

	def TF_IDF(matrix, vocab, qtd):

		tf = Ponderacao_Termos.TF(matrix, vocab, qtd)
		idf = Ponderacao_Termos.IDF(matrix, vocab, qtd)

		tf_idf = collections.defaultdict(dict)

		for item in vocab:
			for i in range(qtd):
				tf_idf[item][i] = idf[item] * tf[item][i]

		for item in vocab:
			print(item," ", end="")
			for i in range(qtd):
				print("  Tweet ",(i+1),":  ",end="")
				print("{:.2f}".format(tf_idf[item][i]), " ", end="")
			print()
			
		return tf_idf

class Pre_Processamento:

	def Vocabulario(data):
		vocabulario = list(dict.fromkeys(data))
		vocabulario.sort()
		return vocabulario

	def Extrai_Termos_Vocabulario():
		termos = []
		matrix = collections.defaultdict(dict)
		i = 0
		with open('rotulados.csv','r', newline = '') as csvfile:
			tweetReader = csv.reader(csvfile, delimiter = ';')
			for row in tweetReader:
				lista = []
				
				for termo in row[0].split():
					lista.append(termo)
					termos.append(termo)
				
				frequency = collections.Counter(lista)
				matrix[i] = frequency
				i+=1

		vocabulario = Pre_Processamento.Vocabulario(termos)

		return vocabulario, matrix, i

def Naive_Bayes(data):
	size = len(data) // 2
	i = iter(data.items())

	test = dict(itertools.islice(i, size))
	train = dict(i)

	clf = MultinomialNB()
	clf.fit(test,train)

	predicao = clf.predict(test)
	score = accuracy_score(test, predicao)
	matrix_confusion = confusion_matrix(test, predicao)
	print(score)
	print(matrix_confusion)

	return clf

def main():
	vocabulario, matrix, qtd_tweets = Pre_Processamento.Extrai_Termos_Vocabulario()
	tf_idf = Ponderacao_Termos.TF_IDF(matrix,vocabulario,qtd_tweets)
	model = Naive_Bayes(tf_idf)


if __name__ == "__main__": 
    main()
    	
