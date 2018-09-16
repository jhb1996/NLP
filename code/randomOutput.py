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
    f=open('T_bigram_prob_dict.json')
    data = json.load(f)
    bigram = {}
    for tup in list(data.keys()):
        bigram[make_tuple(tup)] = data[tup]

    f=open('T_unigram_prob_dict.json')
    unigram = json.load(f)

    print("\n")
    print("----Senetance generated from Unigram ---------")
    print(fromUnigram(unigram) + '\n')
    print("----Senetance generated from Bigram ---------")
    print(fromBigram(bigram,unigram)  + '\n')

if __name__ == "__main__":
    main()