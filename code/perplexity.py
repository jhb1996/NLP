import training
import math

def unigramPerplexity(unigram,speech):
	count = 0
	prob = 0

	for paragraph in speech:
		for word in paragraph:
			prob += (math.log(unigram[word])*(-1))
			count += 1

	return math.exp(prob*(1/count))

def bigramPerplexity(bigram,speech):
	count = 0
	prob = 0

	for paragraph in speech:
		prevWord = ''
		for word in paragraph:
			if(prevWord = ''):
				prob += 0
				prevWord = word
				count += 1
			else:
				prob += (math.log(bigram[(word,prevWord)])*(-1))
				prevWord = word
				count += 1
				
	return math.exp(prob*(1/count))



def main():
    (obama,trump) = training.getSpeeches('Assignment1_resources/development/obama.txt','Assignment1_resources/development/trump.txt');
    print(trump)


if __name__ == "__main__":
    main()
