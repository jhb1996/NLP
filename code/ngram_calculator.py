from training import getSpeeches
import json
import numpy

def _unigram_cnt_dict(doc_lst):
    d = {};
    # print (doc_lst)
    for doc in doc_lst:
        for t in doc:
            if t in d:
                if d!='\n': #ignore the enter charecter
                    d[t]+=1
            else:
                d[t]=1
    return d

def _bigram_cnt_dict(doc_lst):
    #assumes all tokens are relavent
    dTup = {};
    dNest = {};
    for doc in doc_lst:
        for i in range(len(doc)-1):
            t1 = doc[i]
            t2 = doc[i+1]
            bi = str((t1, t2)) #create a bigram using underscores
            if bi in dTup: # if it + the next entry is in the dictionary inc the val
                dTup[bi]+=1
            else:
                dTup[bi]=1

            if t1 in dNest: # if it + the next entry is in the dictionary inc the val
                innerDict = dNest[t1]
                if t2 in innerDict:
                    innerDict[t2]+=1
                else:
                    innerDict[t2] = 1
            else:
                dNest[t1]={}
                dNest[t1][t2]=1
    return dTup, dNest

#generate the count dict with 0s for the other entries
def _bigram_cnt_full_dict(doc_lst, unigram_cnt_dict):
    #assumes all tokens are relavent
    dTup = {};
    dNest = {};
    for doc in doc_lst:
        for i in range(len(doc)-1):
            t1 = doc[i]
            t2 = doc[i+1]
            bi = str((t1, t2)) #create a bigram using underscores
            if bi in dTup: # if it + the next entry is in the dictionary inc the val
                dTup[bi]+=1
            else:
                dTup[bi]=1

            if t1 in dNest: # if it + the next entry is in the dictionary inc the val
                innerDict = dNest[t1]
                if t2 in innerDict:
                    innerDict[t2]+=1
                else:
                    innerDict[t2] = 1
            else:
                dNest[t1]={}
                dNest[t1][t2]=1

    for t1 in unigram_cnt_dict:
        for t2 in unigram_cnt_dict:
            bi = str((t1, t2))
            if bi not in dTup:
                dTup[bi]=0
                if t1 in dNest: # if it + the next entry is in the dictionary inc the val
                    innerDict = dNest[t1]
                    innerDict[t2] = 0
                else:
                    dNest[t1]={}
                    dNest[t1][t2]=0
    return dTup, dNest

def compute_unigram_prob_dict(dCount):
    dProb = {}
    totTokCnt = sum(dCount.values())#totTokCnt = sum over all occurences of each token
    for t in dCount:
        dProb[t] = dCount[t]/totTokCnt
    return dProb

def compute_bigram_prob_dict(uni_dCount, bi_dCount_Nest):
    dCount = bi_dCount_Nest;
    dProb = {}
    i = 1
    for t1 in uni_dCount:
        print(i)
        i+=1
        for t2 in uni_dCount:
            #totTokBiCnt = number of occurences of bigrams starting with that token
            if t1 in dCount:
                innerD = dCount[t1]
                totTokBiCnt = sum(innerD.values())

                if t1 in dCount:
                    if t2 in dCount[t1]:
                        dProb[str((t1, t2))] = dCount[t1][t2]/totTokBiCnt
                    else:
                        dProb[str((t1, t2))] = 0
                else:
                    dProb[str((t1, t2))] = 0
            else:
                dProb[str((t1, t2))] = 0
    return dProb


    #Done super inefficiently - could refactor to create a double dict t1->t2->cnt and increase speed
    # dProb = {}
    # for t1 in uni_dCount:
    #     for t2 in uni_dCount:
    #     #totTokBiCnt = number of occurences of bigrams starting with that token
    #         totTokBiCnt = sum([bi_dCount[(bi1,bi2)] for bi1,bi2 in bi_dCount.keys() if bi1 == t1])
    #         if (t1, t2) in bi_dCount:
    #             dProb[(t1,t2)] = bi_dCount[(t1,t2)]/totTokBiCnt
    #         else:
    #             dProb[(t1, t2)] = 0
    # return dProb

def trainDocLst(doc_lst):
    print('running ngram_calculator')
    #doc_tup = getSpeeches('../Assignment1_resources/train/obama.txt','../Assignment1_resources/train/trump.txt')
    # print (doc_lst)
    #print('got speeches')

    #doc_lst = doc_tup[0]
    #doc_lst = [['security', '...', 'but', 'i', 'heard', 'it'], ['.', 'i', 'read', 'it', 'i', 'heard', 'it', 'ing']]#hardcoded temp

    unigram_cnt_dict = _unigram_cnt_dict(doc_lst)
    print(len(unigram_cnt_dict));
    #print ('unigram_cnt_dict', unigram_cnt_dict)
    unigram_prob_dict = compute_unigram_prob_dict(unigram_cnt_dict)
    # print ('compute_unigram_prob_dict', unigram_prob_dict)

    bigram_cnt_dict_tup,  bigram_cnt_dict_nest = _bigram_cnt_dict(doc_lst)
    #print ('bigram_cnt_dict_nest', bigram_cnt_dict_nest)
    print ('calculating bigram probabilities')
    bigram_prob_dict = compute_bigram_prob_dict(unigram_cnt_dict, bigram_cnt_dict_nest)

    return unigram_cnt_dict, unigram_prob_dict, bigram_cnt_dict_tup, bigram_cnt_dict_nest, bigram_prob_dict


def trainTrump():
    doc_lsts = getSpeeches('../Assignment1_resources/train/obama.txt','../Assignment1_resources/train/trump.txt')
    T_unigram_cnt_dict, T_unigram_prob_dict, T_bigram_cnt_dict_tup, T_bigram_cnt_dict_nest, T_bigram_prob_dict = trainDocLst(doc_lsts[1])
    return     T_unigram_cnt_dict, T_unigram_prob_dict, T_bigram_cnt_dict_tup, T_bigram_cnt_dict_nest, T_bigram_prob_dict

def trainObama():
    doc_lsts = getSpeeches('../Assignment1_resources/train/obama.txt','../Assignment1_resources/train/trump.txt')
    O_unigram_cnt_dict, O_unigram_prob_dict, O_bigram_cnt_dict_tup, O_bigram_cnt_dict_nest, O_bigram_prob_dict = trainDocLst(doc_lsts[1])
    return     O_unigram_cnt_dict, O_unigram_prob_dict, O_bigram_cnt_dict_tup, O_bigram_cnt_dict_nest, O_bigram_prob_dict

def trainBoth():
    doc_lst = getSpeeches('../Assignment1_resources/train/obama.txt','../Assignment1_resources/train/trump.txt')
    #doc_lst = [[['security', '...', 'but', 'i', 'heard', 'it'], ['.', 'i', 'read', 'it', 'i', 'heard', 'it', 'ing']],[['security', '...', 'but', 'i', 'heard', 'it'], ['.', 'i', 'read', 'it', 'i', 'heard', 'it', 'ing']]]#hardcoded temp

    T_unigram_cnt_dict, T_unigram_prob_dict, T_bigram_cnt_dict_tup, T_bigram_cnt_dict_nest, T_bigram_prob_dict = trainDocLst(doc_lst[1])
    print('finished training trump');
    print('starting to train obama');
    O_unigram_cnt_dict, O_unigram_prob_dict, O_bigram_cnt_dict_tup, O_bigram_cnt_dict_nest, O_bigram_prob_dict = trainDocLst(doc_lst[0])
    return T_unigram_cnt_dict, T_unigram_prob_dict, T_bigram_cnt_dict_tup, T_bigram_cnt_dict_nest, T_bigram_prob_dict, \
            O_unigram_cnt_dict, O_unigram_prob_dict, O_bigram_cnt_dict_tup, O_bigram_cnt_dict_nest, O_bigram_prob_dict

def saveFullDictsTrump():
    saveFullDicts('T')

def saveFullDictsObama():
    saveFullDicts('O')

def saveFullDicts(TorO):
    if TorO=='O':
        f_name = 'obama.txt'
    else:
        f_name = 'trump.txt'
    doc_lst = getSpeeches('../Assignment1_resources/train/'+f_name)
    unigram_cnt_dict = _unigram_cnt_dict(doc_lst)
    print('generating bigram full');
    bigram_cnt_full_dict_tup, bigram_cnt_full_dict_nest = _bigram_cnt_full_dict(doc_lst, unigram_cnt_dict)
    print('starting write');
    with open(TorO+'_bigram_cnt_full_dict_tup.json', 'w') as outfile:
        json.dump(bigram_cnt_full_dict_tup, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)
    print('finished writing full Trump dict')

def runAndSaveTrump():
    T_unigram_cnt_dict, T_unigram_prob_dict, T_bigram_cnt_dict_tup, T_bigram_cnt_dict_nest, T_bigram_prob_dict = trainTrump()
    print('starting to output to jsons');
    with open('T_unigram_cnt_dict.json', 'w') as outfile:
        json.dump(T_unigram_cnt_dict, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)

    with open('T_unigram_prob_dict.json', 'w') as outfile:
        json.dump(T_unigram_prob_dict, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)

    with open('T_bigram_cnt_dict_tup.json', 'w') as outfile:
        json.dump(T_bigram_cnt_dict_tup, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)

    with open('T_bigram_cnt_dict_nest.json', 'w') as outfile:
        json.dump(T_bigram_cnt_dict_nest, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)

    with open('T_bigram_cnt_dict_nest.json', 'w') as outfile:
        json.dump(T_bigram_cnt_dict_nest, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)

    with open('T_bigram_prob_dict.json', 'w') as outfile:
        json.dump(T_bigram_prob_dict, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)
    print('finished outputting trump to json');

if __name__ == '__main__':
    #runAndSaveTrump()
    saveFullDictsTrump()
    saveFullDictsObama()




#################
    # with open('O_unigram_cnt_dict.json', 'w') as outfile:
    #     json.dump(O_unigram_cnt_dict, outfile, sort_keys=True, indent=4,
    #               ensure_ascii=False)
    #
    # with open('O_unigram_prob_dict.json', 'w') as outfile:
    #     json.dump(O_unigram_prob_dict, outfile, sort_keys=True, indent=4,
    #               ensure_ascii=False)
    #
    # with open('O_bigram_cnt_dict_tup.json', 'w') as outfile:
    #     json.dump(O_bigram_cnt_dict_tup, outfile, sort_keys=True, indent=4,
    #               ensure_ascii=False)
    #
    # with open('O_bigram_cnt_dict_nest.json', 'w') as outfile:
    #     json.dump(O_bigram_cnt_dict_nest, outfile, sort_keys=True, indent=4,
    #               ensure_ascii=False)
    #
    # with open('O_bigram_cnt_dict_nest.json', 'w') as outfile:
    #     json.dump(O_bigram_cnt_dict_nest, outfile, sort_keys=True, indent=4,
    #               ensure_ascii=False)
    #
    # with open('O_bigram_prob_dict.json', 'w') as outfile:
    #     json.dump(O_bigram_prob_dict, outfile, sort_keys=True, indent=4,
    #               ensure_ascii=False)

    print('finished outputing to jsons');

#unigram
#for each list entry.
    #if it is in the dictionary inc the val
    #else val =1

# for each list entry.
# if it + the next entry is in the dictionary inc the val
# else val =1

