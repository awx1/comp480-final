import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from Bloom_filter import hashfunc
import time
import sys

class Ada_BloomFilter():
    def __init__(self, n, hash_len, k_max):
        self.n = n
        self.hash_len = int(hash_len)
        self.h = []
        for i in range(int(k_max)):
            self.h.append(hashfunc(self.hash_len))
        self.table = np.zeros(self.hash_len, dtype=int)
    def insert(self, key, k):
        for j in range(int(k)):
            t = self.h[j](key)
            self.table[t] = 1
    def test(self, key, k):
        test_result = 0
        match = 0
        for j in range(int(k)):
            t = self.h[j](key)
            match += 1*(self.table[t] == 1)
        if match == k:
            test_result = 1
        return test_result


def R_size(count_key, count_nonkey, R0):
    R = [0]*len(count_key)
    R[0] = R0
    for k in range(1, len(count_key)):
        R[k] = max(int(count_key[k] * (np.log(count_nonkey[0]/count_nonkey[k])/np.log(0.618) + R[0]/count_key[0])), 1)
    return R


def Find_Optimal_Parameters(c_min, c_max, num_group_min, num_group_max, R_sum, train_negative, positive_sample, query_name):
    c_set = np.arange(c_min, c_max+10**(-6), 0.1)
    FP_opt = train_negative.shape[0]

    k_min = 0
    for k_max in range(num_group_min, num_group_max+1):
        for c in c_set:
            tau = sum(c ** np.arange(0, k_max - k_min + 1, 1))
            n = positive_sample.shape[0]
            hash_len = R_sum
            bloom_filter = Ada_BloomFilter(n, hash_len, k_max)
            thresholds = np.zeros(k_max - k_min + 1)
            thresholds[-1] = 1.1
            num_negative = sum(train_negative['score'] <= thresholds[-1])
            num_piece = int(num_negative / tau) + 1
            score = train_negative.loc[(train_negative['score'] <= thresholds[-1]), 'score']
            score = np.sort(score)
            for k in range(k_min, k_max):
                i = k - k_min
                score_1 = score[score < thresholds[-(i + 1)]]
                if int(num_piece * c ** i) < len(score_1):
                    thresholds[-(i + 2)] = score_1[-int(num_piece * c ** i)]

            query = positive_sample[query_name]
            score = positive_sample['score']

            for score_s, query_s in zip(score, query):
                ix = min(np.where(score_s < thresholds)[0])
                k = k_max - ix
                bloom_filter.insert(query_s, k)
            ML_positive = train_negative.loc[(train_negative['score'] >= thresholds[-2]), query_name]
            query_negative = train_negative.loc[(train_negative['score'] < thresholds[-2]), query_name]
            score_negative = train_negative.loc[(train_negative['score'] < thresholds[-2]), 'score']

            test_result = np.zeros(len(query_negative))
            ss = 0
            for score_s, query_s in zip(score_negative, query_negative):
                ix = min(np.where(score_s < thresholds)[0])
                # thres = thresholds[ix]
                k = k_max - ix
                test_result[ss] = bloom_filter.test(query_s, k)
                ss += 1
            FP_items = sum(test_result) + len(ML_positive)
            # print('False positive items: %d, Number of groups: %d, c = %f' %(FP_items, k_max, round(c, 2)))

            if FP_opt > FP_items:
                FP_opt = FP_items
                bloom_filter_opt = bloom_filter
                thresholds_opt = thresholds
                k_max_opt = k_max

    # print('Optimal FPs: %f, Optimal c: %f, Optimal num_group: %d' % (FP_opt, c_opt, num_group_opt))
    return bloom_filter_opt, thresholds_opt, k_max_opt


def main(arg):
    # print(sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', action="store", dest="data_path", type=str, required=True,
                        help="path of the dataset")
    parser.add_argument('--num_group_min', action="store", dest="min_group", type=int, required=True,
                        help="Minimum number of groups")
    parser.add_argument('--num_group_max', action="store", dest="max_group", type=int, required=True,
                        help="Maximum number of groups")
    parser.add_argument('--size_of_Ada_BF', action="store", dest="R_sum", type=int, required=True,
                        help="size of the Ada-BF")
    parser.add_argument('--c_min', action="store", dest="c_min", type=float, required=True,
                        help="minimum ratio of the keys")
    parser.add_argument('--c_max', action="store", dest="c_max", type=float, required=True,
                        help="maximum ratio of the keys")



    results = parser.parse_args()
    DATA_PATH = results.data_path
    num_group_min = results.min_group
    num_group_max = results.max_group
    R_sum = results.R_sum
    c_min = results.c_min
    c_max = results.c_max


    '''
    Load the data and select training data
    '''
    dataset_name = DATA_PATH.split("/")[-1]
    data = pd.read_csv(DATA_PATH)

    if (dataset_name == "Malware_data.csv"):
        '''
        Load the data and select training data
        '''
        negative_sample = data.loc[(data['label']==0)]
        positive_sample = data.loc[(data['label']==1)]
        train_negative = negative_sample.sample(frac = 0.3)

        '''
        Plot the distribution of scores
        '''
        # plt.style.use('seaborn-deep')

        # x = data.loc[data['label']==1,'score']
        # y = data.loc[data['label']==0,'score']
        # bins = np.linspace(0, 1, 25)

        # plt.hist([x, y], bins, log=True, label=['Keys', 'non-Keys'])
        # plt.legend(loc='upper right')
        # plt.savefig('./Malware_Score_Dist.png')
        # plt.show()

        '''Stage 1: Find the hyper-parameters (spare 30% samples to find the parameters)'''
        start = time.time()
        bloom_filter_opt, thresholds_opt, k_max_opt = Find_Optimal_Parameters(c_min, c_max, num_group_min, num_group_max, R_sum, train_negative, positive_sample, 'md5')
        end = time.time()

        
        '''Stage 2: Run Ada-BF on all the samples'''
        ### Test Queries
        ML_positive = negative_sample.loc[(negative_sample['score'] >= thresholds_opt[-2]), 'md5']
        query_negative = negative_sample.loc[(negative_sample['score'] < thresholds_opt[-2]), 'md5']
    elif (dataset_name == "URL_data.csv"):
        '''
        Load the data and select training data
        '''
        negative_sample = data.loc[(data['label']==-1)]
        positive_sample = data.loc[(data['label']==1)]
        train_negative = negative_sample.sample(frac = 0.3)

        '''
        Plot the distribution of scores
        '''
        # plt.style.use('seaborn-deep')

        # x = data.loc[data['label']==1,'score']
        # y = data.loc[data['label']==-1,'score']
        # bins = np.linspace(0, 1, 25)

        # plt.hist([x, y], bins, log=True, label=['Keys', 'non-Keys'])
        # plt.legend(loc='upper right')
        # plt.savefig('./URL_Score_Dist.png')
        # plt.show()

        '''Stage 1: Find the hyper-parameters (spare 30% samples to find the parameters)'''
        start = time.time()
        bloom_filter_opt, thresholds_opt, k_max_opt = Find_Optimal_Parameters(c_min, c_max, num_group_min, num_group_max, R_sum, train_negative, positive_sample, 'url')
        end = time.time()

        
        '''Stage 2: Run Ada-BF on all the samples'''
        ### Test Queries
        ML_positive = negative_sample.loc[(negative_sample['score'] >= thresholds_opt[-2]), 'url']
        query_negative = negative_sample.loc[(negative_sample['score'] < thresholds_opt[-2]), 'url']
    elif (dataset_name == "Fake_news_score_clean.csv"):
        '''
        Load the data and select training data
        '''
        negative_sample = data.loc[(data['label']==0)]
        positive_sample = data.loc[(data['label']==1)]
        train_negative = negative_sample.sample(frac = 0.3)

        '''
        Plot the distribution of scores
        '''
        # plt.style.use('seaborn-deep')

        # x = data.loc[data['label']==1,'score']
        # y = data.loc[data['label']==0,'score']
        # bins = np.linspace(0, 1, 25)

        # plt.hist([x, y], bins, log=True, label=['Keys', 'non-Keys'])
        # plt.legend(loc='upper right')
        # plt.savefig('./FakeNews_Score_Dist.png')
        # plt.show()

        '''Stage 1: Find the hyper-parameters (spare 30% samples to find the parameters)'''
        start = time.time()
        bloom_filter_opt, thresholds_opt, k_max_opt = Find_Optimal_Parameters(c_min, c_max, num_group_min, num_group_max, R_sum, train_negative, positive_sample, 'title')
        end = time.time()

        
        '''Stage 2: Run Ada-BF on all the samples'''
        ### Test Queries
        ML_positive = negative_sample.loc[(negative_sample['score'] >= thresholds_opt[-2]), 'title']
        query_negative = negative_sample.loc[(negative_sample['score'] < thresholds_opt[-2]), 'title']
    
    elif (dataset_name == "Fake_news_score_full_clean.csv"):
        '''
        Load the data and select training data
        '''
        negative_sample = data.loc[(data['label']==0)]
        positive_sample = data.loc[(data['label']==1)]
        train_negative = negative_sample.sample(frac = 0.3)

        '''
        Plot the distribution of scores
        '''
        # plt.style.use('seaborn-deep')

        # x = data.loc[data['label']==1,'score']
        # y = data.loc[data['label']==0,'score']
        # bins = np.linspace(0, 1, 25)

        # plt.hist([x, y], bins, log=True, label=['Keys', 'non-Keys'])
        # plt.legend(loc='upper right')
        # plt.savefig('./FakeNews_Score_Dist.png')
        # plt.show()

        '''Stage 1: Find the hyper-parameters (spare 30% samples to find the parameters)'''
        start = time.time()
        bloom_filter_opt, thresholds_opt, k_max_opt = Find_Optimal_Parameters(c_min, c_max, num_group_min, num_group_max, R_sum, train_negative, positive_sample, 'title')
        end = time.time()
        
        '''Stage 2: Run Ada-BF on all the samples'''
        ### Test Queries
        ML_positive = negative_sample.loc[(negative_sample['score'] >= thresholds_opt[-2]), 'title']
        query_negative = negative_sample.loc[(negative_sample['score'] < thresholds_opt[-2]), 'title']
        
    else:
        print("Should not reach this case")

    score_negative = negative_sample.loc[(negative_sample['score'] < thresholds_opt[-2]), 'score']
    test_result = np.zeros(len(query_negative))
    ss = 0
    total = 0
    for score_s, query_s in zip(score_negative, query_negative):
        ix = min(np.where(score_s < thresholds_opt)[0])
        # thres = thresholds[ix]
        k = k_max_opt - ix
        start2 = time.time()
        test_result[ss] = bloom_filter_opt.test(query_s, k)
        end2 = time.time()
        ss += 1
        total += end2 - start2
    FP_items = sum(test_result) + len(ML_positive)
    FPR = FP_items/len(negative_sample)
    QPS = len(query_negative)/total
    
    # print('False positive items: {}; FPR: {}; Size of queries: {}; Query per second: {}'.format(FP_items, FPR, len(query_negative), QPS))
    print(FPR, QPS)
    return (FPR, QPS)
'''
Implement Ada-BF
'''
if __name__ == '__main__':
    main(sys.argv)
