import csv
import json
from training import getSpeeches
import nltk
from math import log
from numpy import argmax

#https://realpython.com/python-csv/#writing-csv-file-from-a-dictionary-with-csv
#https://realpython.com/python-csv/#writing-csv-files-with-csv

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
    hyperList = [.001,.01,.1,3,.5,.9]

    for hyper in hyperList:
        print ('now validating:', hyper)
        O_cor, O_incor = testHyperparameter(O_token_lst_lst, hyper, 0, O_bigram_prob_dict_smooth, T_bigram_prob_dict_smooth)
        T_cor, T_incor = testHyperparameter(T_token_lst_lst, hyper, 1, O_bigram_prob_dict_smooth, T_bigram_prob_dict_smooth)
        tot_cor = O_cor+T_cor
        tot_incor = O_incor+T_incor
        acc = tot_cor/tot_cor+tot_incor
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
        # first is unknown #TODO make this more robust
        O_prob = unkWeight
        # if str(('<unk>',t2)) in T_bigram_prob_dict_smooth:
        #     O_prob = T_bigram_prob_dict_smooth[str(('<unk>',t2))]*f_unk_hyp

    bi = str((t1,t2))
    if bi in T_bigram_prob_dict_smooth:
        T_prob = T_bigram_prob_dict_smooth[bi]
    else:
        #first is unknown #TODO make this more robust
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

        print('O_prob,T_prob =', O_prob,T_prob,)
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

def output(hyper,overide):

    pred_lst = []
    if overide:
        print('reading in Obama bi prob dict')
        with open('O_bigram_prob_dict_tup_smooth.json', 'r') as f:
            O_bigram_prob_dict_smooth = json.load(f)
        print('reading in Trump bi prob dict')
        with open('T_bigram_prob_dict_tup_smooth.json', 'r') as f:
            T_bigram_prob_dict_smooth = json.load(f)
        print('Done reading in prob dicts')

        testFile = open('../Assignment1_resources/test/test.txt','rt')
        raw = testFile.read()
        split = raw.split("\n")
    else:
        T_fakeDict = {
            "('and', 'we')": 0.6,
            "('<unk>', '<unk>')": 0.5,
            "('and', '<unk>')": 0.4,
            "('<unk>', 'and')": 0.3,
            "('on', 'television')": 0.2,
            "('best', 'person')": 0.2,
        }
        T_bigram_prob_dict_smooth =  T_fakeDict
        O_fakeDict = {
            "('and', 'we')": 0.2,
            "('<unk>', '<unk>')": 0.1,
            "('and', '<unk>')": 0.3,
            "('<unk>', 'and')": 0.4,
            "('on', 'television')": 0.8,
            "('best', 'person')": 0.9,
        }
        O_bigram_prob_dict_smooth =  O_fakeDict


        split = ['and we don get reimbursement. we lose \
on    everything. we \
lose    on    everything. so, we re    going \
 to negotiate and renegotiate trade deals, military \
deals, many     other \
deals    that  s going \
to    get the costs \
down    for running our country very significantly. i m not showing a big number in that.but i believe that if i become president, those numbers are going to be massive.',
    'no, they all    agree.they \
all    agree.they \
just    didnt \
want    to \
go    through \
the    unfair \
questions    because \
they    weren t \
questions; \
they    were \
statements. you \
see they    were \
asking they were \
giving    statements in a\
    sarcastic, disgusting\
    way.    and a\
    woman    was\
    on    television\
    this    morning, and she\
    said,  you    know, mr.trump, and she\
    was    telling\
    other    people, and i\
    actually    called\
    her, and she\
    said,  you    know, mr.trump, i\
    always    was\
    against    guns.',    'fords\
    leaving. theyre    closing\
    plants    all\
    over    michigan\
    to    build\
    a    plant in in mexico.how\
    the    hell\
    does    that\
    help    us ? ok.who \
    are    the people\
    that     think    this is a good    thing    for us ? and in the meantime, in michigan and other places, we have plants closing all over the place and they re spending — think about a $ 2.5 billion — then they ’ re going to sell cars, trucks and parts into the united states, no tax, no nothing.\
    if you want to become a citizen of mexico, you could take the best person in this room, the most qualified, you ’ re not going to do it.they don ’ t do that.']

    for i,paragraph in enumerate(split):
        tokens = nltk.word_tokenize(paragraph)
        tokens = cleanText(tokens)
        #classify the tokens
        pred = classify(tokens, hyper,O_bigram_prob_dict_smooth, T_bigram_prob_dict_smooth)
        pred_lst.append((i,pred))
        #append to a list
    #testFile.close()

    print ('finished generating predictions')
    print('preds:', pred_lst)

    with open('predictions.csv', mode='w') as predictions_file:
        writer = csv.writer(predictions_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['Id','Prediction'])
        for (i,pred) in pred_lst:
            writer.writerow([i, pred])

def findOptimalHyperParams():
    print('reading in Obama bi prob dict')
    with open('O_bigram_prob_dict_tup_smooth.json', 'r') as f:
        O_bigram_prob_dict_smooth = json.load(f)
    print('reading in Trump bi prob dict')
    with open('T_bigram_prob_dict_tup_smooth.json', 'r') as f:
        T_bigram_prob_dict_smooth = json.load(f)
    print('Done reading in prob dicts')

    # fakeDict = {
    # "('opinion', 'learned')": 0.0017231682815846332,
    # "('opinion', 'learning')": 0.0017231682815846332,
    # "('opinion', 'least')": 0.0017231682815846332,
    # "('opinion', 'leave')": 0.0017231682815846332,
    # "('opinion', 'leaves')": 0.0017231682815846332,
    # "('opinion', 'leaving')": 0.0017231682815846332,
    # "('opinion', 'lebanon')": 0.0017231682815846332,
    # "('opinion', 'led')": 0.0017231682815846332,
    # "('opinion', 'left')": 0.0017231682815846332,
    # "('opinion', 'legacy')": 0.0017231682815846332,
    # "('opinion', 'legal')": 0.0017231682815846332,
    # "('opinion', 'legally')": 0.0017231682815846332,
    # "('opinion', 'legendary')": 0.0017231682815846332,
    # "('opinion', 'lesbian')": 0.0017231682815846332,
    # "('opinion', 'less')": 0.0017231682815846332,
    # "('opinion', 'let')": 0.0017231682815846332,
    # "('opinion', 'letter')": 0.0017231682815846332,
    # }

    #bestHyper = validation(fakeDict, fakeDict)

    bestHypers = validation(O_bigram_prob_dict_smooth, T_bigram_prob_dict_smooth)
    print ('bestHyper', bestHypers)
    optimal_hyper_params = bestHypers
    with open('optimal_hyper_params.json', 'w') as outfile:
        json.dump(optimal_hyper_params, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)



if __name__ == "__main__":
    #findOptimalHyperParams()
    hyper = .01
    output(hyper, True)