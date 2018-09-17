import csv
import json
from training import getSpeeches
import nltk


#https://realpython.com/python-csv/#writing-csv-file-from-a-dictionary-with-csv
#https://realpython.com/python-csv/#writing-csv-files-with-csv


# def validate():


def getProbOandT(t1,t2,O_bigram_prob_dict,T_bigram_prob_dict):
    bi = str((t1,t2))
    if bi in T_bigram_prob_dict_smooth:
        prob_T = T_bigram_prob_dict_smooth[bi]
    else:
        print('TODO')

    if bi in O_bigram_prob_dict_smooth:
        prob_O = O_bigram_prob_dict_smooth[bi]
    else:
        print('TODO')

# Takes a string and output a 0 (obama) or a 1 (trump).
def classify(tokens,O_bigram_prob_dict,T_bigram_prob_dict):
    for i in range (len(tokens)):
        t1 = tokens[i]
        t2 = tokens[i+1]
        prob_O,prob_T = getProbOandT(t1,t2, O_bigram_prob_dict,T_bigram_prob_dict)

        #print(tokens)
    return 1

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

def output():
    pred_lst = []
    print('reading in Obama bi prob dict')
    with open('smoothed_T_bigram_cnt_dict_tup.json', 'w') as outfile:
        json.dump(smoothed_T_bigram_cnt, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)
    print('reading in Trump bi prob dict')
    with open('O_bigram_cnt_full_dict_tup.json', 'r') as f:
        O_bigram_cnt_full_dict_tup = json.load(f)
    print('Done reading in prob dicts')
    testFile = open('../Assignment1_resources/test/test.txt','rt')
    raw = testFile.read()
    split = raw.split("\n")
    for i,paragraph in enumerate(split):
        tokens = nltk.word_tokenize(paragraph)
        tokens = cleanText(tokens)
        #classify the tokens
        pred = classify(tokens, O_bigram_prob_dict, T_bigram_prob_dict)
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


if __name__ == "__main__":
    output()