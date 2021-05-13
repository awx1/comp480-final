import numpy as np
import pandas as pd
import argparse
from Bloom_filter import BloomFilter
import time


def Find_Optimal_Parameters(max_thres, min_thres, R_sum, train_negative, positive_sample, query_name):
    FP_opt = train_negative.shape[0]

    for threshold in np.arange(min_thres, max_thres+10**(-6), 0.01):
        query = positive_sample.loc[(positive_sample['score'] <= threshold), query_name]
        n = len(query)
        bloom_filter = BloomFilter(n, R_sum)
        bloom_filter.insert(query)
        ML_positive = train_negative.loc[(train_negative['score'] > threshold), query_name]
        bloom_negative = train_negative.loc[(train_negative['score'] <= threshold), query_name]
        BF_positive = bloom_filter.test(bloom_negative, single_key=False)
        FP_items = sum(BF_positive) + len(ML_positive)
        # print('Threshold: %f, False positive items: %d' %(round(threshold, 2), FP_items))
        if FP_opt > FP_items:
            FP_opt = FP_items
            thres_opt = threshold
            bloom_filter_opt = bloom_filter
    return bloom_filter_opt, thres_opt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', action="store", dest="data_path", type=str, required=True,
                        help="path of the dataset")
    parser.add_argument('--threshold_min', action="store", dest="min_thres", type=float, required=True,
                        help="Minimum threshold for positive samples")
    parser.add_argument('--threshold_max', action="store", dest="max_thres", type=float, required=True,
                        help="Maximum threshold for positive samples")
    parser.add_argument('--size_of_LBF', action="store", dest="R_sum", type=int, required=True,
                        help="size of the LBF")

    results = parser.parse_args()
    DATA_PATH = results.data_path
    min_thres = results.min_thres
    max_thres = results.max_thres
    R_sum = results.R_sum

    dataset_name = DATA_PATH.split("/")[-1]
    data = pd.read_csv(DATA_PATH)

    if (dataset_name == "Malware_data.csv"):
        '''
        Load the data and select training data
        '''
        negative_sample = data.loc[(data['label']==0)]
        positive_sample = data.loc[(data['label']==1)]
        train_negative = negative_sample.sample(frac = 0.3)

        '''Stage 1: Find the hyper-parameters (spare 30% samples to find the parameters)'''
        start = time.time()
        bloom_filter_opt, thres_opt = Find_Optimal_Parameters(max_thres, min_thres, R_sum, train_negative, positive_sample, 'md5')
        end = time.time()
        '''Stage 2: Run LBF on all the samples'''
        ### Test queries
        ML_positive = negative_sample.loc[(negative_sample['score'] > thres_opt), 'md5']
        bloom_negative = negative_sample.loc[(negative_sample['score'] <= thres_opt), 'md5']
    elif (dataset_name == "URL_data.csv"):
        '''
        Load the data and select training data
        '''
        negative_sample = data.loc[(data['label']==-1)]
        positive_sample = data.loc[(data['label']==1)]
        train_negative = negative_sample.sample(frac = 0.3)

        '''Stage 1: Find the hyper-parameters (spare 30% samples to find the parameters)'''
        start = time.time()
        bloom_filter_opt, thres_opt = Find_Optimal_Parameters(max_thres, min_thres, R_sum, train_negative, positive_sample, 'url')
        end = time.time()

        '''Stage 2: Run LBF on all the samples'''
        ### Test queries
        ML_positive = negative_sample.loc[(negative_sample['score'] > thres_opt), 'url']
        bloom_negative = negative_sample.loc[(negative_sample['score'] <= thres_opt), 'url']
    elif (dataset_name == "Fake_news_score_clean.csv"):
        '''
        Load the data and select training data
        '''
        negative_sample = data.loc[(data['label']==0)]
        positive_sample = data.loc[(data['label']==1)]
        train_negative = negative_sample.sample(frac = 0.3)

        '''Stage 1: Find the hyper-parameters (spare 30% samples to find the parameters)'''
        start = time.time()
        bloom_filter_opt, thres_opt = Find_Optimal_Parameters(max_thres, min_thres, R_sum, train_negative, positive_sample, 'title')
        end = time.time()
        '''Stage 2: Run LBF on all the samples'''
        ### Test queries
        ML_positive = negative_sample.loc[(negative_sample['score'] > thres_opt), 'title']
        bloom_negative = negative_sample.loc[(negative_sample['score'] <= thres_opt), 'title']
    
    elif (dataset_name == "Fake_news_score_full_clean.csv"):
        '''
        Load the data and select training data
        '''
        negative_sample = data.loc[(data['label']==0)]
        positive_sample = data.loc[(data['label']==1)]
        train_negative = negative_sample.sample(frac = 0.3)

        '''Stage 1: Find the hyper-parameters (spare 30% samples to find the parameters)'''
        start = time.time()
        bloom_filter_opt, thres_opt = Find_Optimal_Parameters(max_thres, min_thres, R_sum, train_negative, positive_sample, 'title')
        end = time.time()

        '''Stage 2: Run LBF on all the samples'''
        ### Test queries
        ML_positive = negative_sample.loc[(negative_sample['score'] > thres_opt), 'title']
        bloom_negative = negative_sample.loc[(negative_sample['score'] <= thres_opt), 'title']
        
    else:
        print("Should not reach this case")

    score_negative = negative_sample.loc[(negative_sample['score'] < thres_opt), 'score']
    start2 = time.time()
    BF_positive = bloom_filter_opt.test(bloom_negative, single_key = False)
    end2 = time.time()
    FP_items = sum(BF_positive) + len(ML_positive)
    FPR = FP_items/len(negative_sample)
    timee = (end-start) + (end2-start2)
    QPS = len(negative_sample)/timee
    print(FPR, QPS)
    # print('False positive items: {}; FPR: {}; Size of queries: {}'.format(FP_items, FPR, len(negative_sample)))

'''
Implement learned Bloom filter
'''
if __name__ == '__main__':
    main()
