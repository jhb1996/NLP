import nltk
from ngram_dict_reader import read_in_dicts
# import ssl
#
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
#
#
# nltk.download('punkt')
#nltk.download('punkt')

def getSpeeches(path1,path2=None):
    f=open(path1,'rt')
    raw = f.read()
    split = raw.split("\n")
    obama = []
    for paragraph in split:
        obamaTokens = nltk.word_tokenize(paragraph)
        obamaTokens = cleanText(obamaTokens)
        obama.append(obamaTokens)
    f.close()

    #if running on test data path2 will=null
    if path2 != None:
        f=open(path2,'rt')
        raw = f.read()
        split = raw.split("\n")
        trump = []
        for paragraph in split:
            trumpTokens = nltk.word_tokenize(paragraph)
            trumpTokens = cleanText(trumpTokens)
            trump.append(trumpTokens)
        f.close()
    else:
        return obama

    return (obama,trump);

def cleanText(tokens):
    #remove certain puncuations 
    #unwanted = ["--", ",", "``", "“", "”"] 
    unwanted = ["``", "“", "”", "''"] #with commas and dashes
    tokens = [word for word in tokens if word not in unwanted]
    #
    # for (i, word) in enumerate(tokens):
    #     tokens[i]=(word.replace("'", ''))

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
    # (obama,trump) = getSpeeches('../Assignment1_resources/train/obama.txt','../Assignment1_resources/train/trump.txt');
    # print(trump[2])#
    print ('running main from training.py');
    print('reading in dicts');
    T_unigram_cnt_dict, T_unigram_prob_dict, T_bigram_cnt_dict_tup, T_bigram_cnt_dict_nest, T_bigram_prob_dict = read_in_dicts()
    #T_unigram_cnt_dict, T_unigram_prob_dict, T_bigram_cnt_dict_tup, T_bigram_cnt_dict_nest, T_bigram_prob_dict#, \
    #O_unigram_cnt_dict, O_unigram_prob_dict, O_bigram_cnt_dict_tup, O_bigram_cnt_dict_nest, O_bigram_prob_dict = read_in_dicts()
    print('finished reading in dicts');
    print('T_unigram_cnt_dict', T_unigram_cnt_dict)
    print('T_unigram_prob_dict', T_unigram_prob_dict)
    print('T_bigram_cnt_dict_nest', T_bigram_cnt_dict_nest)
    print('T_bigram_prob_dict', T_bigram_prob_dict)


if __name__ == "__main__":
    main()