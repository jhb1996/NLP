from ngram_calculator import *
from goodTuringSmoothing import *
from kaggleBigram import *



if __name__ == "__main__":
    runAndSaveTrump()
    runAndSaveObama()
    saveFullDictsTrump()
    saveFullDictsObama()
    findOptimalHyperParams(unsmoothed=True)
    with open('optimal_hyper_params.json', 'r') as f:
        optimal_hyper_params_arr = json.load(f)
        hyper = optimal_hyper_params_arr[0]
    # hyper = 100000000000000000000000
    output(hyper, unsmoothed=True)