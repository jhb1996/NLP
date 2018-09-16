import numpy as np

def fromUnigram(unigram):

    words = list(unigram.keys())
    prob = list(unigram.values())
    sentance = ''
    genWord = ''

    while genWord != '.':
        genWord = np.random.choice(words,1,prob)
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

    return sentance

def main():
    unigram = {'he':.1,'will':.1,'is':.2,'live':.2,'die':.2,'.':.2}
    bigram = {("he","will"):.2,("he","is"):.8,("will","live"):.5,("will","die"):.5,("is","."):.5,("is","live"):.5,(".","he"):.5,(".","he"):.5,
               ("live","."):1, ("die","."):1 }
    #print(fromUnigram(unigram))
    print(fromBigramSeed(".",bigram, unigram))
if __name__ == "__main__":
    main()