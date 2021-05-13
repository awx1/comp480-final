import sys
import subprocess
import matplotlib.pyplot as plt
import os

def runForData(dataPathName, modelPathName, gmin, gmax, cmin, cmax):
    print(dataPathName, gmin, gmax, cmin, cmax)

    Ada_BF_out = subprocess.check_output([sys.executable, "./Ada_BF.py", "--data_path", dataPathName, "--size_of_Ada_BF", "200000",  "--num_group_min", gmin,  "--num_group_max", gmax,  "--c_min", cmin,  "--c_max", cmax])
    FPR, QPS = (Ada_BF_out.decode("utf-8")).split(' ')
    FPR = float(FPR)
    QPS = float(QPS)
    print("Ada_Bf FPR & QPS:", FPR, QPS)


    disJoint_out = subprocess.check_output([sys.executable, "./disjoint_Ada_BF.py", "--data_path", dataPathName, "--model_path", modelPathName, "--size_of_Ada_BF", "200000",  "--num_group_min", gmin, "--num_group_max", gmax,  "--c_min", cmin,  "--c_max", cmax])
    print(disJoint_out)
    FPR3, QPS3 = (disJoint_out.decode("utf-8")).split(' ')
    FPR3 = float(FPR3)
    QPS3 = float(QPS3)
    print("DisJoint Ada_Bf FPR & QPS:", FPR3, QPS3)

    

#Main code
runForData("./Datasets/URL_data.csv", "./URL_Random_Forest_Model_n_10_leaf_20.pickle", str(8), str(12), str(1.6), str(2.5))
runForData("./Datasets-fakenews/Fake_news_score_clean.csv", "./rf_model.p", str(8), str(12), str(1.6), str(2.5))
runForData("./Datasets-fakenews/Fake_news_score_full_clean.csv", "./rf_model.p", str(8), str(12), str(1.6), str(2.5))

runForData("./Datasets/URL_data.csv", "./URL_Random_Forest_Model_n_10_leaf_20.pickle", str(4), str(20), str(1.0), str(3.0))
runForData("./Datasets-fakenews/Fake_news_score_clean.csv", "./rf_model.p", str(4), str(20), str(1.0), str(3.0))
runForData("./Datasets-fakenews/Fake_news_score_full_clean.csv", "./rf_model.p", str(4), str(20), str(1.0), str(3.0))



