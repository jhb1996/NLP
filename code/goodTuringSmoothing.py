import operator
import json
import numpy as np
def gtSmoothing(bigramCount):
    
    keysList = list(bigramCount)
    length = len(bigramCount)
    NArr = {} # Records the number of bigrams with count =0, 1, ..., i.e., N0, N1, N2... i.e., NArr={1:13, 4:35, 2:602 ...}. Keys may not be in any particular order
    
    #Computing NArr
    for i in range (length):
        numberOfOccurences = bigramCount[keysList[i]] # numberOfOccurences is the number of times the ith bigram occurs (ith bigram = bigramCount[keysList[i]])
        if(numberOfOccurences in NArr): # Has a bigram with frequency= numberOfOccurences already been encountered?
            NArr[numberOfOccurences]+=1;
        else:
            NArr[numberOfOccurences]=1;
    N=0 # N = sum of frequencies of each word

    #computing N
    for i in range (len(NArr)):
        N+=NArr[list(NArr)[i]]*list(NArr)[i]
        
    NArrNew = {}
    
    NAvg=N/len(NArr) # TEMPORARY HACK
    
    listOfFrequencyBins = list(NArr);
    listOfFrequencyBins.sort()

    #Smoothing
    for c in listOfFrequencyBins:
        #if(c>5):
        #   continue   #According to Katz's rule
        if(c == 0): 
            NArrNew[0] = NArr[1]/NArr[0]
        elif(c == max(NArr)): 
            NArrNew[c] = 0 #WHAT ARE THE SMOOTHED FREQUENCIES OF THE BIGRAMS WITH THE HIGHEST COUNT?
        else:
            if((c+1) not in list(NArr)):
                NArr[c+1]=NAvg #NEED TO IMPLEMENT SIMPLE GOOD TURING INSTEAD OF CURRENT CODE
            NArrNew[c] = (c+1)*NArr[c+1]/NArr[c] #The smoothed frequency count of all bigrams with count NArr[i] is now equal to (i+1)*(NArr[i+1]/N)
            
    probabilitySum=0;#Sanity check
    print('NArr:',NArr)
    for i in listOfFrequencyBins:
        probabilitySum+=NArr[i]*NArrNew[i]/N
    #print('Probability Sum: ',probabilitySum)
    
    #Computing the new counts of each word
    print('bigram count of each key of the dictionary:')
    for i in range (length):
        bigramCount[keysList[i]]=NArrNew[bigramCount[keysList[i]]]    
    return bigramCount
'''            
#Sample execution
table1={
('I', 'I'):0, ('I', 'see'): 1, ('I', 'saw'):0,('I', 'a'):0,
('see', 'I'):0, ('see', 'see'): 0, ('see', 'saw'):2,('see', 'a'):0,
('saw', 'I'):0, ('saw', 'see'): 0, ('saw', 'saw'):0,('saw', 'a'):5,
('a', 'I'):0, ('a', 'see'): 1, ('a', 'saw'):0,('a', 'a'):0
}
table2={
    ('a', 'a'):1, ('a','b'):1, ('a','c'):3,
    ('b','a'):2, ('b','b'):0, ('b','c'):1,
    ('c','a'):2, ('c','b'):1, ('c','c'):0,
    }
'''

# with open('T_bigram_cnt_full_dict_tup.json') as f:
#     x=f.read()
#     data=json.loads(x)
#
# gtSmoothing(data)


if __name__ == "__main__":
    print('reading Trump json')
    with open('T_bigram_cnt_full_dict_tup.json', 'r') as f:
        T_bigram_cnt_full_dict_tup = json.load(f)
    print('finished reading in T_bigram_cnt_full_dict_tup.json');
    smoothed_T_bigram_cnt = gtSmoothing(T_bigram_cnt_full_dict_tup)
    print('finished calculating smoothed_T_bigram_cnt');
    print('writing smoothed_T_bigram_cnt to a json');
    with open('smoothed_T_bigram_cnt_dict_tup.json', 'w') as outfile:
        json.dump(smoothed_T_bigram_cnt, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)
    print('finished Trump');
    print('reading in Obama O_bigram_cnt_full_dict_tup.json');
    with open('O_bigram_cnt_full_dict_tup.json', 'r') as f:
        O_bigram_cnt_full_dict_tup = json.load(f)
    print('finished reading in O_bigram_cnt_full_dict_tup.json');
    print('calculating obama')
    smoothed_O_bigram_cnt = gtSmoothing(O_bigram_cnt_full_dict_tup)
    print('finished calculating smoothed_O_bigram_cnt');
    print('writing calculating smoothed_O_bigram_cnt')
    with open('smoothed_O_bigram_cnt_dict_tup.json', 'w') as outfile:
        json.dump(smoothed_T_bigram_cnt, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)
    print('DONE!')