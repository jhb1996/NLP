import math
import numpy as np
import nltk
import gensim
import time

def cosine(v1,v2):
	return np.dot(v1,v2)/(math.sqrt(np.dot(v1,v1))) * math.sqrt(np.dot(v2,v2))

def analogy(x1, x2, y1,model):
	start = time.time()
	result = model.most_similar(positive=[y1, x2], negative=[x1])
	end = time.time()
	print(end - start)
	return result[0][0]

def bestWord(v_a,v_b,v_c,words):
	start = time.time()
	bestWord = ''
	maxVal = -9999.0
	for i in range(0, words.syn0.shape[0]):
		v_d = words.syn0[i]
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
	f=open('analogy_test_personal.txt','rt')
	raw = f.read()
	split = raw.split("\n")
	tokenizedFile = []

	for line in split:
		tokenizedFile.append(nltk.word_tokenize(line))

	return tokenizedFile

def test():
	print("generating Model...")
	model = gensim.models.KeyedVectors.load_word2vec_format('../Assignment1_resources/GoogleNews-vectors-negative300.bin', binary=True)
	#model = gensim.models.KeyedVectors.load_word2vec_format("gensim_glove_vectors.txt", binary=False)
	print("done generating Model")
	analogyFile = getAnalogyFile()
	f = open("Analogy_Personal_PredictionResults_Word2Vec.txt","w+")
	countCorrect = 0
	countTotal = 0
	l = len(analogyFile)
	print("\nfinding bestWords...")
	for i in range(l):
		if not i == []:
			print(str(countTotal)+"/"+str(l))
			print("\n")
			row = analogyFile[i]
			#word = bestWord(model[row[0]],model[row[1]],model[row[2]],model)
			word = analogy(row[0].lower(),row[1].lower(),row[2].lower(),model)
			correct = (word == row[3].lower())
			if(correct):
				countCorrect += 1
			countTotal += 1
			f.write("\nGiven: "+str(row[0]) + " " + str(row[1]) + " " + str(row[2])+ " Model Predicted: " + str(word) + " "+str(correct))
	f.write("\nScore: " +str(countCorrect) + "/" + str(countTotal))
	f.close()
		
def topSimilar():
	model_1 = gensim.models.KeyedVectors.load_word2vec_format('../Assignment1_resources/GoogleNews-vectors-negative300.bin', binary=True)
	model_2 = gensim.models.KeyedVectors.load_word2vec_format("gensim_glove_vectors.txt", binary=False)
	print("enter:")
	print(model_1.similar_by_vector(model_1['enter'], topn=10, restrict_vocab=None))
	print("increase:")
	print(model_1.similar_by_vector(model_1['increase'], topn=10, restrict_vocab=None))
	print("return")
	print(model_1.similar_by_vector(model_1['return'], topn=10, restrict_vocab=None))
	print("close")
	print(model_1.similar_by_vector(model_1['close'], topn=10, restrict_vocab=None))
	print("enter2:")
	print(model_2.similar_by_vector(model_2['enter'], topn=10, restrict_vocab=None))
	print("increase2:")
	print(model_2.similar_by_vector(model_2['increase'], topn=10, restrict_vocab=None))
	print("return2")
	print(model_2.similar_by_vector(model_2['return'], topn=10, restrict_vocab=None))
	print("close2")
	print(model_2.similar_by_vector(model_2['close'], topn=10, restrict_vocab=None))

def main():
	print("running from main")
	topSimilar()
	#test()
	#f=open('analogy_test.txt','rt')
	#raw = f.read()
	#split = raw.split("\n")
	#tokenizedFile = []

	#for line in split:
	#	tokenizedFile.append(nltk.word_tokenize(line))

	#numTrue=0
	#numTotal=0

	#for line in tokenizedFile:
	#	if(not line == []):
	#		if(line[9] == 'True'):
	#			numTrue += 1
	#		numTotal += 1
	#print(numTrue)
	#print(numTotal)

if __name__ == "__main__":
    main()