import math
import numpy as np
import nltk
import gensim
import time

def cosine(v1,v2):
	assert len(v1)==len(v2), print("vectors not same length")
	return np.dot(v1,v2)/(math.sqrt(np.dot(v1,v1))) * math.sqrt(np.dot(v2,v2))

def bestWord(v_a,v_b,v_c,words):
	start = time.time()
	v_a = np.array(v_a)
	v_b = np.array(v_b)
	v_c = np.array(v_c)
	bestWord = ''
	maxVal = -9999.0
	print("finding bestWord...")
	for i in range(0, words.syn0.shape[0]):
		v_d = np.array(words.syn0[i])
		val = cosine(v_d,v_b-v_a+v_c)
		if(maxVal < val and not np.array_equal(v_d, v_a) and not np.array_equal(v_d, v_b) and not np.array_equal(v_d, v_c)):
			bestWord = i
			maxVal = val
	word= [k for k in words.vocab if words.vocab[k].__dict__['index']==bestWord]
	end = time.time()
	print(val)
	print("time took to find bestWord: ")
	print(end - start)
	return word
 
def getAnalogyFile():
	f=open('../Assignment1_resources/analogy_test.txt','rt')
	raw = f.read()
	split = raw.split("\n")
	tokenizedFile = []

	for line in split:
		tokenizedFile.append(nltk.word_tokenize(line))

	return tokenizedFile

def test():
	print("generating Model...")
	model = gensim.models.KeyedVectors.load_word2vec_format('../Assignment1_resources/GoogleNews-vectors-negative300.bin', binary=True)
	analogyFile = getAnalogyFile()
	print("done generating Model")
	f = open("AnalogyPredictionResults","w+")
	countCorrect = 0
	countTotal = 0
	for i in range(10):
		row = analogyFile[i]
		word = bestWord(model[row[0]],model[row[1]],model[row[2]],model)
		correct = (word[0] == row[3])
		if(correct):
			countCorrect += 1
		countTotal += 1
		f.write("\nGiven: "+str(row[0]) + " " + str(row[1]) + " " + str(row[2])+ " Model Predicted: " + str(word) + " "+str(correct))
	f.write("\nScore: " +str(countCorrect) + "/" + str(countTotal))
	f.close()
		

def main():
	print("running from main")
	test()

if __name__ == "__main__":
    main()