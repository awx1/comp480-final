import sys
import subprocess
import matplotlib.pyplot as plt
import os

def runForData(dataPathName):
    Ada_BF_out = subprocess.check_output([sys.executable, "./Ada_BF.py", "--data_path", dataPathName, "--size_of_Ada_BF", "200000",  "--num_group_min", "8",  "--num_group_max", "12",  "--c_min", "1.6",  "--c_max", "2.5"])
    FPR, QPS = (Ada_BF_out.decode("utf-8")).split(' ')
    FPR = float(FPR)
    QPS = float(QPS)
    print(FPR, QPS)

    BF_out = subprocess.check_output([sys.executable, "./Bloom_filter.py", "--data_path", dataPathName, "--size_of_BF", "200000"])
    # print(BF_out)
    FPR1, QPS1 = (BF_out.decode("utf-8")).split(' ')
    FPR1 = float(FPR1)
    QPS1 = float(QPS1)
    print(FPR1, QPS1)

    learned_BF_out = subprocess.check_output([sys.executable, "./learned_Bloom_Filter.py", "--data_path", dataPathName, "--size_of_LBF", "200000",  "--threshold_min", "0.5",   "--threshold_max", "0.95"])
    # print(learned_BF_out)
    FPR2, QPS2 = (learned_BF_out.decode("utf-8")).split(' ')
    FPR2 = float(FPR2)
    QPS2 = float(QPS2)
    print(FPR2, QPS2)

    # disJoint_out = subprocess.check_output([sys.executable, "/Users/aabouzeid/Desktop/Junior_year/Spring2021/COMP480/FinalProject/comp480-final/Ada-BF-master/disjoint_Ada_BF.py", "--data_path", "./Datasets/URL_data.csv", "--model_path", "./rf_model.p", "--size_of_Ada_BF", "200000",  "--num_group_min", "8", "--num_group_max", "12",  "--c_min", "1.6",  "--c_max", "2.5"])
    # print(disJoint_out)
    # FPR3, QPS3 = (learned_BF_out.decode("utf-8")).split(' ')
    # FPR3 = float(FPR3)
    # QPS3 = float(QPS3)
    # print(FPR3, QPS3)

    listJx = [QPS, QPS1, QPS2]
    ListlistPx = [FPR, FPR1, FPR2]
    


#Main code
runForData("./Datasets/URL_data.csv")
runForData("./Datasets/Malware_data.csv")
runForData("./Datasets-fakenews/Fake_news_score_clean.csv")
runForData("./Datasets-fakenews/Fake_news_score_full_clean.csv")

