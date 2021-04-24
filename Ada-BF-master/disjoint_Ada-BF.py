import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from Bloom_filter import BloomFilter
import os


def R_size(count_key, count_nonkey, R0):
    R = [0]*len(count_key)
    R[0] = max(R0,1)
    for k in range(1, len(count_key)):
        R[k] = max(int(count_key[k] * (np.log(count_nonkey[0]/count_nonkey[k])/np.log(0.618) + R[0]/count_key[0])), 1)
    return R


def Find_Optimal_Parameters(c_min, c_max, num_group_min, num_group_max, R_sum, train_negative, positive_sample, query_name):
    c_set = np.arange(c_min, c_max+10**(-6), 0.1)
    FP_opt = train_negative.shape[0]

    for num_group in range(num_group_min, num_group_max+1):
        for c in c_set:
            ### Determine the thresholds
            thresholds = np.zeros(num_group + 1)
            thresholds[0] = -0.1
            thresholds[-1] = 1.1
            num_negative = train_negative.shape[0]
            tau = sum(c ** np.arange(0, num_group, 1))
            num_piece = int(num_negative / tau)
            score = np.sort(np.array(list(train_negative['score'])))

            for i in range(1, num_group):
                if thresholds[-i] > 0:
                    score_1 = score[score < thresholds[-i]]
                    if int(num_piece * c ** (i - 1)) <= len(score_1):
                        thresholds[-(i + 1)] = score_1[-int(num_piece * c ** (i - 1))]
                    else:
                        thresholds[-(i + 1)] = 0
                else:
                    thresholds[-(i + 1)] = 1

            count_nonkey = np.zeros(num_group)
            for j in range(num_group):
                count_nonkey[j] = sum((score >= thresholds[j]) & (score < thresholds[j + 1]))

            num_group_1 = sum(count_nonkey > 0)
            count_nonkey = count_nonkey[count_nonkey > 0]
            thresholds = thresholds[-(num_group_1 + 1):]

            ### Count the keys of each group
            query = positive_sample[query_name]
            score = positive_sample['score']

            count_key = np.zeros(num_group_1)
            query_group = []
            bloom_filter = []
            for j in range(num_group_1):
                count_key[j] = sum((score >= thresholds[j]) & (score < thresholds[j + 1]))
                query_group.append(query[(score >= thresholds[j]) & (score < thresholds[j + 1])])

            ### Search the Bloom filters' size
            R = np.zeros(num_group_1 - 1)
            R[:] = 0.5 * R_sum
            non_empty_ix = min(np.where(count_key > 0)[0])
            if non_empty_ix > 0:
                R[0:non_empty_ix] = 0
            kk = 1
            while abs(sum(R) - R_sum) > 200:
                if (sum(R) > R_sum):
                    R[non_empty_ix] = R[non_empty_ix] - int((0.5 * R_sum) * (0.5) ** kk + 1)
                else:
                    R[non_empty_ix] = R[non_empty_ix] + int((0.5 * R_sum) * (0.5) ** kk + 1)
                R[non_empty_ix:] = R_size(count_key[non_empty_ix:-1], count_nonkey[non_empty_ix:-1], R[non_empty_ix])
                if int((0.5 * R_sum) * (0.5) ** kk + 1) == 1:
                    break
                kk += 1

            Bloom_Filters = []
            for j in range(int(num_group_1 - 1)):
                if j < non_empty_ix:
                    Bloom_Filters.append([0])
                else:
                    Bloom_Filters.append(BloomFilter(count_key[j], R[j]))
                    Bloom_Filters[j].insert(query_group[j])

            ### Test querys
            ML_positive = train_negative.loc[(train_negative['score'] >= thresholds[-2]), query_name]
            query_negative = train_negative.loc[(train_negative['score'] < thresholds[-2]), query_name]
            score_negative = train_negative.loc[(train_negative['score'] < thresholds[-2]), 'score']

            test_result = np.zeros(len(query_negative))
            ss = 0
            for score_s, query_s in zip(score_negative, query_negative):
                ix = min(np.where(score_s < thresholds)[0]) - 1
                if ix >= non_empty_ix:
                    test_result[ss] = Bloom_Filters[ix].test(query_s)
                else:
                    test_result[ss] = 0
                ss += 1
            FP_items = sum(test_result) + len(ML_positive)
            print('False positive items: %d, Number of groups: %d, c = %f' %(FP_items, num_group, round(c, 2)))
            if FP_opt > FP_items:
                FP_opt = FP_items
                Bloom_Filters_opt = Bloom_Filters
                thresholds_opt = thresholds
                non_empty_ix_opt = non_empty_ix

    return Bloom_Filters_opt, thresholds_opt, non_empty_ix_opt



'''
Implement disjoint Ada-BF
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', action="store", dest="data_path", type=str, required=True,
                        help="path of the dataset")
    parser.add_argument('--model_path', action="store", dest="model_path", type=str, required=True,
                        help="path of the model")
    parser.add_argument('--num_group_min', action="store", dest="min_group", type=int, required=True,
                        help="Minimum number of groups")
    parser.add_argument('--num_group_max', action="store", dest="max_group", type=int, required=True,
                        help="Maximum number of groups")
    parser.add_argument('--size_of_Ada_BF', action="store", dest="M_budget", type=int, required=True,
                        help="memory budget")
    parser.add_argument('--c_min', action="store", dest="c_min", type=float, required=True,
                        help="minimum ratio of the keys")
    parser.add_argument('--c_max', action="store", dest="c_max", type=float, required=True,
                        help="maximum ratio of the keys")



    results = parser.parse_args()
    DATA_PATH = results.data_path
    num_group_min = results.min_group
    num_group_max = results.max_group
    model_size = os.path.getsize(results.model_path)
    R_sum = results.M_budget - model_size * 8
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
        plt.style.use('seaborn-deep')

        x = data.loc[data['label']==1,'score']
        y = data.loc[data['label']==0,'score']
        bins = np.linspace(0, 1, 25)

        plt.hist([x, y], bins, log=True, label=['Keys', 'non-Keys'])
        plt.legend(loc='upper right')
        plt.savefig('./Malware_Score_Dist-disjoint.png')
        plt.show()

        '''Stage 1: Find the hyper-parameters'''
        Bloom_Filters_opt, thresholds_opt, non_empty_ix_opt = Find_Optimal_Parameters(c_min, c_max, num_group_min, num_group_max, R_sum, train_negative, positive_sample, 'md5')
        
        '''Stage 2: Run disjoint Ada-BF on all the samples'''
        ### Test queries
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
        plt.style.use('seaborn-deep')

        x = data.loc[data['label']==1,'score']
        y = data.loc[data['label']==-1,'score']
        bins = np.linspace(0, 1, 25)

        plt.hist([x, y], bins, log=True, label=['Keys', 'non-Keys'])
        plt.legend(loc='upper right')
        plt.savefig('./URL_Score_Dist-disjoint.png')
        plt.show()

        '''Stage 1: Find the hyper-parameters'''
        Bloom_Filters_opt, thresholds_opt, non_empty_ix_opt = Find_Optimal_Parameters(c_min, c_max, num_group_min, num_group_max, R_sum, train_negative, positive_sample, 'url')

        '''Stage 2: Run disjoint Ada-BF on all the samples'''
        ### Test queries
        ML_positive = negative_sample.loc[(negative_sample['score'] >= thresholds_opt[-2]), 'url']
        query_negative = negative_sample.loc[(negative_sample['score'] < thresholds_opt[-2]), 'url']
    else:
        print("Should not reach this case")

    score_negative = negative_sample.loc[(negative_sample['score'] < thresholds_opt[-2]), 'score']
    test_result = np.zeros(len(query_negative))
    ss = 0
    for score_s, query_s in zip(score_negative, query_negative):
        ix = min(np.where(score_s < thresholds_opt)[0]) - 1
        if ix >= non_empty_ix_opt:
            test_result[ss] = Bloom_Filters_opt[ix].test(query_s)
        else:
            test_result[ss] = 0
        ss += 1
    FP_items = sum(test_result) + len(ML_positive)
    FPR = FP_items/len(query_negative)
    print('False positive items: {}; FPR: {}; Size of quries: {}'.format(FP_items, FPR, len(query_negative)))
