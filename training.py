import nltk
nltk.download('punkt')

def getSpeeches():
	f=open('Assignment1_resources/train/obama.txt','rt')
	raw = f.read()
	obamaTokens = nltk.word_tokenize(raw)
	obamaTokens = cleanText(obamaTokens)
	f.close()

	f=open('Assignment1_resources/train/trump.txt','rt')
	raw = f.read()
	trumpTokens = nltk.word_tokenize(raw)
	trumpTokens = cleanText(trumpTokens)
	f.close()

	return (obamaTokens,trumpTokens);


def cleanText(tokens):
	#remove certain puncuations 
	unwanted = ["--", ",", "``", "“", "”"]
	tokens = [word for word in tokens if word not in unwanted]

	#combine conjoined words
	result = []
	for i in range(len(tokens)-1):
		if(tokens[i+1] == "’"):
			v = "" + tokens[i]+tokens[i+1]+tokens[i+2]
			result.append(v)
			i = i + 2
		else:
			result.append(tokens[i])
	
	return result

def main():
	(obama,trump) = getSpeeches();
	print(trump[:500])


if __name__ == "__main__":
	main()