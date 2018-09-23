import csv
import json
from training import getSpeeches
import nltk
from math import log
from numpy import argmax


#runs the classifier with different settings for the <unk> classifier to find the optimal value
def validation(O_bigram_prob_dict_smooth,T_bigram_prob_dict_smooth):
    T_token_lst_lst = []
    T_val_file = open('../Assignment1_resources/development/trump.txt', 'rt')
    T_raw = T_val_file.read()
    T_split = T_raw.split("\n")
    for i, paragraph in enumerate(T_split):
        T_tokens = nltk.word_tokenize(paragraph)
        T_tokens = cleanText(T_tokens)
        T_token_lst_lst.append(T_tokens)

    O_token_lst_lst = []
    O_val_file = open('../Assignment1_resources/development/obama.txt', 'rt')
    O_raw = O_val_file.read()
    O_split = O_raw.split("\n")
    for i, paragraph in enumerate(O_split):
        O_tokens = nltk.word_tokenize(paragraph)
        O_tokens = cleanText(O_tokens)
        O_token_lst_lst.append(O_tokens)

    best_acc = 0
    hyperList = [.001,.01,.1,.5,2,5,10,100,1000,10000,100000, 1000000, 10000000, 100000000, 1000000000, 10000000000, 100000000000, 100000000000, 10000000000000, 100000000000000, 1000000000000000,10000000000000000,10000000000000000000,100000000000000000000, 1000000000000000000000, 10000000000000000000000, 100000000000000000000000,1000000000000000000000000]

    for hyper in hyperList:
        print ('now validating:', hyper)
        O_cor, O_incor = testHyperparameter(O_token_lst_lst, hyper, 0, O_bigram_prob_dict_smooth, T_bigram_prob_dict_smooth)
        T_cor, T_incor = testHyperparameter(T_token_lst_lst, hyper, 1, O_bigram_prob_dict_smooth, T_bigram_prob_dict_smooth)
        tot_cor = O_cor+T_cor
        tot_incor = O_incor+T_incor
        acc = tot_cor/(tot_cor+tot_incor)
        print('hyper:', hyper, 'acc=', acc)
        if acc > best_acc:
            best_acc = acc
            best_hyper = hyper
    print ("best_hyper=", best_hyper)
    return [best_hyper]


def testHyperparameter(token_lst_lst, unkWeight, correctAnswer, O_bigram_prob_dict_smooth,T_bigram_prob_dict_smooth):#unkWeight is a hyperParamater setting
    numCorrect = 0
    numIncorrect = 0
    for token_lst in token_lst_lst: #iterate through each paragraph
        O_neg_log_pagraph_prob = 0
        T_neg_log_pagraph_prob = 0
        for i in range (len(token_lst)-1): #iterate through each token
            t1,t2 = token_lst[i],token_lst[i+1]
            O_prob,T_prob = getProbOandT(t1, t2, unkWeight, O_bigram_prob_dict_smooth, T_bigram_prob_dict_smooth)
            if O_prob == 0:
                O_prob = .001
            if T_prob == 0:
                T_prob = .001
            O_neg_log_pagraph_prob += log(O_prob)
            T_neg_log_pagraph_prob += log(T_prob)
            #classification happens here
            ZeroOrOne = argmax([O_neg_log_pagraph_prob*-1,T_neg_log_pagraph_prob*-1])

        if correctAnswer == ZeroOrOne: numCorrect +=1
        else: numIncorrect +=1

    return numCorrect, numIncorrect


def getProbOandT(t1,t2, unkWeight,O_bigram_prob_dict_smooth,T_bigram_prob_dict_smooth):
    bi = str((t1, t2))
    if bi in O_bigram_prob_dict_smooth:
        O_prob = O_bigram_prob_dict_smooth[bi]
    else:
        O_prob = unkWeight
        # if str(('<unk>',t2)) in T_bigram_prob_dict_smooth:
        #     O_prob = T_bigram_prob_dict_smooth[str(('<unk>',t2))]*f_unk_hyp

    bi = str((t1,t2))
    if bi in T_bigram_prob_dict_smooth:
        T_prob = T_bigram_prob_dict_smooth[bi]
    else:
        T_prob = unkWeight
        # if str(('<unk>',t2)) in T_bigram_prob_dict_smooth:
        #     T_prob = T_bigram_prob_dict_smooth[str(('<unk>',t2))]*f_unk_hyp

    return O_prob, T_prob



# Takes a string and output a 0 (obama) or a 1 (trump).
def classify(tokens,  unkWeight, O_bigram_prob_dict_smooth,T_bigram_prob_dict_smooth):
    O_neg_log_pagraph_prob = 0
    T_neg_log_pagraph_prob = 0
    for i in range (len(tokens)-1):
        t1 = tokens[i]
        t2 = tokens[i+1]
        O_prob,T_prob = getProbOandT(t1,t2, unkWeight, O_bigram_prob_dict_smooth,T_bigram_prob_dict_smooth)

        if O_prob == 0:
            O_prob = .001
        if T_prob == 0:
            T_prob = .001
        O_neg_log_pagraph_prob += log(O_prob)
        T_neg_log_pagraph_prob += log(T_prob)
        #classification happens here
    ZeroOrOne = argmax([O_neg_log_pagraph_prob*-1,T_neg_log_pagraph_prob*-1])

    return ZeroOrOne

def cleanText(tokens):
    #remove certain puncuations
    #unwanted = ["--", ",", "``", "“", "”"]
    unwanted = ["``", "“", "”"] #with commas and dashes
    tokens = [word for word in tokens if word not in unwanted]

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

#output actual predictions of the test set as a csv
def output(hyper, unsmoothed):
    split = ''
    pred_lst = []
    #testFile =
    if not unsmoothed:
        print('reading in Obama bi prob dict')
        with open('O_bigram_prob_dict_tup_smooth.json', 'r') as f:
            O_bigram_prob_dict = json.load(f)
        print('reading in Trump bi prob dict')
        with open('T_bigram_prob_dict_tup_smooth.json', 'r') as f:
            T_bigram_prob_dict = json.load(f)
        print('Done reading in prob dicts')


    else:
        with open('O_bigram_prob_dict.json', 'r') as f:
            O_bigram_prob_dict = json.load(f)
        print('reading in Trump bi prob dict')
        with open('T_bigram_prob_dict.json', 'r') as f:
            T_bigram_prob_dict = json.load(f)
        print('Done reading in prob dicts')

    testFile = open('../Assignment1_resources/test/test.txt','rt')
    raw = testFile.read()
    split = raw.split("\n")
    for i, paragraph in enumerate(split):
        if i!= len(split)-1:
            tokens = nltk.word_tokenize(paragraph)
            tokens = cleanText(tokens)
            print(i, tokens)
            #classify the tokens
            pred = classify(tokens, hyper, O_bigram_prob_dict, T_bigram_prob_dict)
            pred_lst.append((i,pred))
            #append to a list
    testFile.close()

    print ('finished generating predictions')
    print('preds:', pred_lst)

    with open('predictions.csv', mode='w') as predictions_file:
        writer = csv.writer(predictions_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['Id','Prediction'])
        for (i,pred) in pred_lst:
            writer.writerow([i, pred])

def findOptimalHyperParams(unsmoothed):
    if not unsmoothed:
        print('reading in Obama bi prob dict')
        with open('O_bigram_prob_dict_tup_smooth.json', 'r') as f:
            O_bigram_prob_dict = json.load(f)
        print('reading in Trump bi prob dict')
        with open('T_bigram_prob_dict_tup_smooth.json', 'r') as f:
            T_bigram_prob_dict = json.load(f)
        print('Done reading in prob dicts')


    else:
        print('reading in obama unsmoothed prob dict')
        with open('O_bigram_prob_dict.json', 'r') as f:
            O_bigram_prob_dict = json.load(f)
        print('reading in Trump bi prob dict')
        with open('T_bigram_prob_dict.json', 'r') as f:
            T_bigram_prob_dict = json.load(f)
        print('Done reading in prob dicts')

    bestHypers = validation(O_bigram_prob_dict, T_bigram_prob_dict)
    print ('bestHyper', bestHypers)
    optimal_hyper_params = bestHypers
    with open('optimal_hyper_params.json', 'w') as outfile:
        json.dump(optimal_hyper_params, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)



if __name__ == "__main__":
    findOptimalHyperParams(unsmoothed=True)
    with open('optimal_hyper_params.json', 'r') as f:
        optimal_hyper_params_arr = json.load(f)
        hyper = optimal_hyper_params_arr[0]
    #hyper = 100000000000000000000000
    output(hyper, unsmoothed=True)