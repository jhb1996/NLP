import training
import math
import json
from ast import literal_eval as make_tuple

def unigramPerplexity(unigram,speech):
	count = 0
	prob = 0

	for paragraph in speech:
		for word in paragraph:
			if word in unigram:
				prob += (math.log(unigram[word])*(-1))
			else:
				prob += (math.log(unigram['<unk>'])*(-1))
			count += 1

	return math.exp(prob*(1/count))

def bigramPerplexity(bigram,unigram,speech):
	count = 0
	prob = 0

	for paragraph in speech:
		prevWord = ''
		for word in paragraph:
			if(prevWord == ''):
				prob += 0
			else:
				if word not in unigram:
					if prevWord not in unigram:
						prob += (math.log(bigram[('<unk>','<unk>')])*(-1))
					else: 
						prob += (math.log(bigram[(prevWord,'<unk>')])*(-1))

				elif prevWord not in unigram:
					prob += (math.log(bigram[('<unk>',word)])*(-1))
				else:
					try:
						prob += (math.log(bigram[(prevWord,word)])*(-1))
					except:
						print(prevWord)
						print(word)
						print(bigram[(prevWord,word)])
			prevWord = word
			count += 1

	return math.exp(prob*(1/count))

def main():
    (obama,trump) = training.getSpeeches('../Assignment1_resources/development/obama.txt','../Assignment1_resources/development/trump.txt');
    print("creating bigram probabilities from json")

    f=open('smoothed_T_bigram_cnt_dict_tup.json')
    data = json.load(f)
    t_bigram = {}
    for tup in list(data.keys()):
        t_bigram[make_tuple(tup)] = data[tup]

    print("creating unigram probabilities from json")
    f=open('T_unigram_prob_dict.json')
    t_unigram = json.load(f)
    f.close()

    print("creating bigram probabilities from json")
    f=open('smoothed_O_bigram_cnt_dict_tup.json')
    data = json.load(f)
    o_bigram = {}
    for tup in list(data.keys()):
        o_bigram[make_tuple(tup)] = data[tup]

    print("creating unigram probabilities from json")
    f=open('O_unigram_prob_dict.json')
    o_unigram = json.load(f)
    f.close()

    print("----unigram obama perplexity ------ \n")
    print(unigramPerplexity(o_unigram,obama))
    print("----unigram trump perplexity ------")
    print(unigramPerplexity(t_unigram,trump))
    print("----bigram trump perplexity ------ \n")
    print(bigramPerplexity(t_bigram,t_unigram,trump))
    print("----bigram obama perplexity ------ \n")
    print(bigramPerplexity(o_bigram,o_unigram,obama))

if __name__ == "__main__":
    main()
