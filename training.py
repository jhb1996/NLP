import nltk
nltk.download('punkt')

def getSpeeches():
    f=open('Assignment1_resources/train/obama.txt','rt')
    raw = f.read()
    split = raw.split("\n")
    obama = []
    for paragraph in split:
        obamaTokens = nltk.word_tokenize(paragraph)
        obamaTokens = cleanText(obamaTokens)
        obama.append(obamaTokens)
    f.close()

    f=open('Assignment1_resources/train/trump.txt','rt')
    raw = f.read()
    split = raw.split("\n")
    trump = []
    for paragraph in split:
        trumpTokens = nltk.word_tokenize(paragraph)
        trumpTokens = cleanText(trumpTokens)
        trump.append(trumpTokens)
    f.close()

    return (obama,trump);

def cleanText(tokens):
    #remove certain puncuations 
    #unwanted = ["--", ",", "``", "“", "”"] 
    unwanted = ["``", "“", "”"] #with commas and dashes
    tokens = [word for word in tokens if word not in unwanted]

    #combine conjoined words
    i = 0
    result = []
    while i < len(tokens)-3:
        if(tokens[i+1] == "’"):
            v = "" + tokens[i]+tokens[i+1]+tokens[i+2]
            result.append(v)
            i += 3
        elif(tokens[i+1] == "'s"):
            v = "" + tokens[i] + tokens[i+1]
            result.append(v)
            i += 2
        else:
            result.append(tokens[i])
            i += 1

    result += tokens[-3:]
    return result

def main():
    (obama,trump) = getSpeeches();
    print(trump[2])


if __name__ == "__main__":
    main()