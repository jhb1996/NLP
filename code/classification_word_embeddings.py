import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from scipy import spatial
import csv
'''
Aim: Is a given speech Obama's or Trump's?
Data: Testing:  The Obama and Trump excerpts given
      Training: Pre-trained word embeddings from stanford (glove100)

1) Compute the vector representation of Obama's and Trump's training data: find the average of each vector in the list of words of obama's and trump's speeches that we have been given

2) Compute a vector representation of the speech excerpt to be classified
    - find the corresponding vector representation for each of words in the speech by using the embeddings list
    
3) Use the cosine similarity index to check if the excerpt is closer to Obama's or Trump's speeches
'''

length_of_each_embedding=300 #for glove300

def sum_len(data):
    return [sum(l) / len(l) for l in zip(*data)]

embeddings = {}
with open('..\\Assignment1_resources\\train\\glove300.txt',  "rb") as f:
    for line in f:
        line = line.decode("utf-8")
        columns = line.strip().split()
        embeddings[columns[0]] = [float(n) for n in columns[1:]]

def word2vec(words):
    vectors=[]
    for x in words:
        if x in embeddings:
            vectors.append(embeddings[x])
        else:
            vectors.append([0]*length_of_each_embedding)  #if word not seen in dictionary set the corresponding vector to 0
    return vectors


with open ("..\\Assignment1_resources\\train\\obama.txt", "r", encoding="utf8") as myfile:
    obama_text=myfile.read()

with open ("..\\Assignment1_resources\\train\\trump.txt", "r", encoding="utf8") as myfile:
    trump_text=myfile.read()


obama_words = [word_tokenize(i) for i in [obama_text]]
obama_words=obama_words[0]
trump_words = [word_tokenize(i) for i in [trump_text]]
trump_words=trump_words[0]

obama_speech_representation = word2vec(obama_words) #obama_speech_representation is the vector represntation of all of obama's training data
obama_avg=sum_len(obama_speech_representation)


trump_speech_representation = word2vec(trump_words)
trump_avg=sum_len(trump_speech_representation)

def predict(test): 
    test_words = [word_tokenize(i) for i in [test]]
    test_words = test_words[0]
    test_vectors =[] #A list of vectors - one vector per word in the test speech
    test_vectors = word2vec(test_words)    
    test_avg = np.average(test_vectors, axis=0) #test_average is the average of the vector representations of each word in the speech to be predicted

    #Comparing similarity
    obama_similarity = 1 - spatial.distance.cosine(test_avg, obama_avg)
    trump_similarity = 1 - spatial.distance.cosine(test_avg, trump_avg)
    
    if(obama_similarity>trump_similarity):
        return 0
    else:
        return 1

with open('..\\Assignment1_resources\\test\\test_mod.txt',  "rb") as f: 
    test_text=[]
    for line in f:
        line = line.decode("utf-8")
        test_text.append(line.strip())


#Write predictions to file    
count=0
with open('word_embeddings_predictions.csv', mode='w', newline='') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=',')
    for speech in test_text:
        employee_writer.writerow([count, predict(speech)])
        count+=1
        

