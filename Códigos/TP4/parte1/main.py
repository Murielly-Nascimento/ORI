import re
import csv
import demoji
import unidecode
from textblob import TextBlob
from googletrans import Translator

def RemoveCaracteres(linha):
	linha = re.sub(r'http\S+', '', linha)
	termo = unidecode.unidecode(linha.lower())
	termo = re.sub(r'[^\w\s]','',termo)
	termo = re.sub(r'[0-9]+','',termo)
	termo = re.sub("@[A-Za-z0-9_]+","", termo)
	termo = re.sub("#[A-Za-z0-9_]+","", termo)
	termo = re.sub("-[A-Za-z0-9_]+","", termo)
	return termo

def RemoveEmojis(linha):
	emoji = demoji.findall(linha)
	for termo in emoji.keys():
		linha = linha.replace(termo, '')
	return linha

def TrataTermos(linha):	
	linha = RemoveCaracteres(linha)

	linha = RemoveEmojis(linha)

	translator = Translator()
	linha = translator.translate(linha).text

	return linha

def ExtraiSentimentos(linha):
	sentimento = TextBlob(linha)
	return sentimento.sentiment.polarity

def AnaliseSentimentos():	
	matrix = []
	with open("reforma_previdencia_rotulado.csv", 'r', encoding="utf8") as file:
		csvreader = csv.reader(file, delimiter=';')
		for row in csvreader:
			tweetTranslated = TrataTermos(row[0])
			feeling = ExtraiSentimentos(tweetTranslated)
			pair = []
			pair.append(tweetTranslated)
			pair.append(feeling)
			matrix.append(pair)

	return matrix

def EscreveArquivo(data):
	classificacao = ""
	with open('rotulados.csv','w', newline = '') as csvfile:
		tweetWriter = csv.writer(csvfile, delimiter = ';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for row in data:
			
			if row[1] >= 0.5 and row[1] <=1: classificacao = "Positivo"
			elif row[1] <= -0.5 and row[1] >= -1: classificacao = "Negativo"
			else: classificacao = "Neutro"

			tweetWriter.writerow([row[0]] + [row[1]] + [classificacao])

def main():
	matrix = AnaliseSentimentos()
	EscreveArquivo(matrix)

if __name__ == "__main__":
	main()
