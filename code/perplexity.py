import training
import math
import json
from ast import literal_eval as make_tuple

def unigramPerplexity(unigram,speech):
	count = 0
	prob = 0

	for paragraph in speech:
		for word in paragraph:
			print(word)
			print(unigram[word])
			prob += (math.log(unigram[word])*(-1))
			count += 1

	return math.exp(prob*(1/count))

def bigramPerplexity(bigram,speech):
	count = 0
	prob = 0

	for paragraph in speech:
		prevWord = ''
		for word in paragraph:
			if(prevWord == ''):
				prob += 0
				prevWord = word
				count += 1
			else:
				prob += (math.log(bigram[(word,prevWord)])*(-1))
				prevWord = word
				count += 1
				
	return math.exp(prob*(1/count))



def main():
    (obama,trump) = training.getSpeeches('../Assignment1_resources/development/obama.txt','../Assignment1_resources/development/trump.txt');
    
    print("creating bigram probabilities from json")

    f=open('T_bigram_prob_dict.json')
    data = json.load(f)
    bigram = {}
    for tup in list(data.keys()):
        bigram[make_tuple(tup)] = data[tup]

    print("creating unigram probabilities from json")
    f=open('T_unigram_prob_dict.json')
    unigram = json.load(f)
    f.close()

    print(unigramPerplexity(unigram,obama))

if __name__ == "__main__":
    main()
