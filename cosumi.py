import spacy
import csv
import pandas as pd
import ollama

nlp = spacy.load('pt_core_news_sm')

from ollama_interact import interact_with_ollama

fakeocurrence = ollama.generate(model='llama3', prompt='Simule um  texto  fake de ocorrência policial  informando o nome da vítima para um teste de segurança')


doc = nlp(fakeocurrence['response'])

cont = 1


x = [(token.text, token.pos, token.pos_) for token in doc]

fraseanominizada = ""
'''
for i in range(len(x)):

    if x[i][2] == "PROPN" and i!=(len(x)-1):
        fraseanominizada += "P"+str(cont) + " "
        cont+=1
    elif  x[i][2] == "PROPN" and i==(len(x)-1):
        fraseanominizada += "P"+str(cont) 
    elif i!=(len(x)-1):
        fraseanominizada += x[i][0] + " "

    else:
        fraseanominizada += x[i][0]

print(fraseanominizada)

'''



z = ollama.generate(model='example', prompt='Informe o nome da vítima da ocorrência, a região da ocorrência, o tipo de ocorrência e se for possível o golpista ou Agressor : ' + fakeocurrence['response'])

doc = nlp(z['response'])

print(z['response'])