import numpy as np
import json
from ast import literal_eval as make_tuple

#end sentances after 20 words else sentances are very long (20000 words)
def fromUnigram(unigram):

    words = list(unigram.keys())
    prob = list(unigram.values())
    sentance = ''
    genWord = ''
    count = 0

    while genWord != '.' and count < 20:
        genWord = np.random.choice(words,1,prob)
        count += 1
        if(genWord == '.'):
            sentance+=("\b"+genWord[0])
        else:
            sentance+=(genWord[0] + " ")
    return sentance
 
#bigram is dictionary of (word1,word2)->prob
#{word:{word:prob,word:prob}, word:...}
def fromBigram(bigram,unigram):
    return fromBigramSeed('.',bigram,unigram)

def fromBigramSeed(seed,bigram,unigram):
    dist = {}

    for word in unigram:
        dist[word] = {}

    for (word1,word2) in bigram:
        (dist[word1])[word2] = bigram[word1,word2]
    genWord = ''
    lastWord = seed;
    sentance = ''
    while genWord != '.':
        words = list(dist[lastWord].keys())
        prob = list(dist[lastWord].values())
        if(words == []):
            return  sentance + "."
        genWord = np.random.choice(words,1,prob)
        lastWord = genWord[0]
        if(genWord == '.'):
            sentance+=("\b"+genWord[0])
        else:
            sentance+=(genWord[0] + " ")

     #test sum
    #test = {}
    #for listKey in list(dist.keys()):
    #    li = dist[listKey]
    #    test[listKey] = 0;
    #   for word in list(li.keys()):
    #       test[listKey] = (test[listKey] + li[word])
    #print (test)

    return sentance

def main():
    print("running randomOutput main")
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

    print("writing to output")
    f = open("sentanceGeneratedOutput.txt","w+")
    f.write("----Sentances generated from Unigram ---------\n\n")
    for i in range(20):
        f.write(fromUnigram(unigram) + '\n\n')
    f.write("----Sentances generated from Bigram ---------\n\n")
    for i in range(20):
        f.write(fromBigram(bigram,unigram)  + '\n\n')
    f.close()

    print("done writing to output")

if __name__ == "__main__":
    main()