###############################################################################
# Univesidade Federal de Pernambuco -- UFPE (http://www.ufpe.br)
# Centro de Informatica -- CIn (http://www.cin.ufpe.br)
# Bacharelado em Sistemas de Informacao
# IF968 -- Programacao 1
#
# Autor:    Fulano de Tal
#            Beltrano do Cin
#
# Email:    fdt@cin.ufpe.br
#            bdc@cin.ufpe.br
#
# Data:        2016-06-10
#
# Descricao:  Este e' um modelo de arquivo para ser utilizado para a implementacao
#                do projeto pratico da disciplina de Programacao 1. 
#                 A descricao do projeto encontra-se no site da disciplina e trata-se
#                de uma adaptacao do projeto disponivel em 
#                http://nifty.stanford.edu/2016/manley-urness-movie-review-sentiment/
#                O objetivo deste projeto e' implementar um sistema de analise de
#                sentimentos de comentarios de filmes postados no site Rotten Tomatoes.
#
# Licenca: The MIT License (MIT)
#            Copyright(c) 2016 Fulano de Tal, Beltrano do Cin
#
###############################################################################

import sys
import re
from string import punctuation

import os



def removeSpecialWords(query):

    stopwords = ["'t","'d","'ll","'m","'ve","'s","'re","n't"]
    querywords = query.split()

    resultwords  = [word for word in querywords if word.lower() not in stopwords]
    result = ' '.join(resultwords)

    return result


def strip_punctuation(s):
    '''remove a pontuação de uma string'''
        
    return ''.join(c for c in s if c not in punctuation)

def clean_up(s):
    ''' Retorna uma versao da string 's' na qual todas as letras sao
        convertidas para minusculas e caracteres de pontuacao sao removidos
        de ambos os extremos. A pontuacao presente no interior da string
        e' mantida intacta.
    '''    
    punctuation = ''''!"',;:.-?)([]<>*#\n\t\r'''
    result = s.lower().strip(punctuation)
    return result


stop_words = dict()
    
stop_f = open("stopwords.txt",'r')
'''cria um dicionários de stopwords'''
for line in stop_f:
    stop_words[clean_up(strip_punctuation(line))] = False

stop_f.close()



def split_on_separators(original, separators):
    '''    Retorna um vetor de strings nao vazias obtido a partir da quebra
        da string original em qualquer dos caracteres contidos em 'separators'.
        'separtors' e' uma string formada com caracteres unicos a serem usados
        como separadores. Por exemplo, '^$' e' uma string valida, indicando que
        a string original sera quebrada em '^' e '$'.
    '''            
    return filter(lambda x: x != '',re.split('[{0}]'.format(separators),original))
                    


def readTrainingSet(fname):
    '''    Recebe o caminho do arquivo com o conjunto de treinamento como parametro
        e retorna um dicionario com triplas (palavra,freq,escore) com o escore
        medio das palavras no comentarios.
    '''

    words = dict()

    cont = 0
    
    f = open(fname,'r')
    for line in f:
       
        scoore = int(line[:1])
        line = list(split_on_separators(clean_up(strip_punctuation(removeSpecialWords(line[1:])))," "))
        
        for word in line:
            if stop_words.get(word) == None:
                if words.get(word):
                    words[word][0] += 1
                    words[word][1] = ((words[word][1] + scoore)/(words[word][0]))
                else:
                    aux = []
                    aux.append(int(1))
                    aux.append(scoore)
                    words[word] = aux
                
    f.close()

    return words


    


def readTestSet(fname):
    ''' Esta funcao le o arquivo contendo o conjunto de teste
	retorna um vetor/lista de pares (escore,texto) dos
	comentarios presentes no arquivo.
    '''
    #reviews=None
    reviews = []
    listAux = []
    f = open(fname,'r')
    for line in f:
        listAux.append(int(line[:1]))
        listAux.append(clean_up(strip_punctuation(removeSpecialWords(line[1:]))))
        reviews.append(listAux)
        
        listAux = []
  
    f.close()
    return reviews


def computeSentiment(review,words):
    ''' Retorna o sentimento do comentario recebido como parametro.
        O sentimento de um comentario e' a media dos escores de suas
        palavras. Se uma palavra nao estiver no conjunto de palavras do
        conjunto de treinamento, entao seu escore e' 2.
        Review e' a parte textual de um comentario.
        Words e' o dicionario com as palavras e seus escores medios no conjunto
        de treinamento.
    '''
    score = 0.0
    count = 0
    
    
    review = list(split_on_separators(review," "))
    
    for word in review:
        if stop_words.get(word) == None:
            if words.get(word):
                
                score+= words[word][1]
                count+= 1
            else:
                score += 2
                count += 1
    if count != 0:
        return score/count
    else:
        return 0
    

def computeSumSquaredErrors(reviews,words):
    '''    Computa a soma dos quadrados dos erros dos comentarios recebidos
        como parametro. O sentimento de um comentario e' obtido com a
        funcao computeSentiment. 
        Reviews e' um vetor de pares (escore,texto)
        Words e' um dicionario com as palavras e seus escores medios no conjunto
        de treinamento.    
    '''
   
    sse = 0
    
    for review in reviews:
        
        sse += ((computeSentiment(review[1],words) - review[0]) * (computeSentiment(review[1],words) - review[0]))        
    
    sse = (sse/len(reviews))
    return sse





def main():
    
    # Os arquivos sao passados como argumentos da linha de comando para o programa
    # Voce deve buscar mais informacoes sobre o funcionamento disso (e' parte do
    # projeto).
    
    # A ordem dos parametros e' a seguinte: o primeiro e' o nome do arquivo
    # com o conjunto de treinamento, em seguida o arquivo do conjunto de teste.
    
    if len(sys.argv) < 3:
        print('Numero invalido de argumentos')
        print('O programa deve ser executado como python sentiment_analysis.py <arq-treino> <arq-teste>')
        os.system("Pause")
        sys.exit(0)
    
    # Lendo conjunto de treinamento e computando escore das palavras
    words = readTrainingSet(sys.argv[1])
    #words = readTrainingSet("trainSet.txt")
    # Lendo conjunto de teste
    reviews = readTestSet(sys.argv[2])
    #reviews = readTestSet("testSet.txt")
    # Inferindo sentimento e computando soma dos quadrados dos erros
    sse = computeSumSquaredErrors(reviews,words)
    
    print('A soma do quadrado dos erros e\': {0}'.format(sse))
    os.system("Pause")

if __name__ == '__main__':
   main()

    
