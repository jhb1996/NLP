import json

def read_in_dicts():
    with open('T_unigram_cnt_dict.json', 'r') as f:
        T_unigram_cnt_dict = json.load(f)
    with open('T_unigram_prob_dict.json', 'r') as f:
        T_unigram_prob_dict = json.load(f)
    with open('T_bigram_cnt_dict_tup.json', 'r') as f:
        T_bigram_cnt_dict_tup = json.load(f)
    with open('T_bigram_cnt_dict_nest.json', 'r') as f:
        T_bigram_cnt_dict_nest = json.load(f)
    with open('T_bigram_cnt_dict_nest.json', 'r') as f:
        T_bigram_cnt_dict_nest = json.load(f)
    with open('T_bigram_prob_dict.json', 'r') as f:
        T_bigram_prob_dict = json.load(f)
    print ('finished reading in Trump dicts')
#################
    # with open('O_unigram_cnt_dict.json', 'r') as f:
    #     O_unigram_cnt_dict = json.load(f)
    # with open('O_unigram_prob_dict.json', 'r') as f:
    #     O_unigram_prob_dict = json.load(f)
    # with open('O_bigram_cnt_dict_tup.json', 'r') as f:
    #     O_bigram_cnt_dict_tup = json.load(f)
    # with open('O_bigram_cnt_dict_nest.json', 'r') as f:
    #     O_bigram_cnt_dict_nest = json.load(f)
    # with open('O_bigram_cnt_dict_nest.json', 'r') as f:
    #     O_bigram_cnt_dict_nest = json.load(f)
    # with open('O_bigram_prob_dict.json', 'r') as f:
    #     O_bigram_prob_dict = json.load(f)

    return T_unigram_cnt_dict, T_unigram_prob_dict, T_bigram_cnt_dict_tup, T_bigram_cnt_dict_nest, T_bigram_prob_dict#, \
          #  O_unigram_cnt_dict, O_unigram_prob_dict, O_bigram_cnt_dict_tup, O_bigram_cnt_dict_nest, O_bigram_prob_dict
