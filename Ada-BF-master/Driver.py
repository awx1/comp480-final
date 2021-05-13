import sys
import subprocess
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

cols = ['b', 'g', 'r', 'k']
markers = ["o", "^", "s", "x"]

# ["o", "^", "s"]

def runForData(dataPathName, col):
    Ada_BF_out = subprocess.check_output([sys.executable, "./Ada_BF.py", "--data_path", dataPathName, "--size_of_Ada_BF", "200000",  "--num_group_min", "8",  "--num_group_max", "12",  "--c_min", "1.6",  "--c_max", "2.5"])
    FPR, QPS = (Ada_BF_out.decode("utf-8")).split(' ')
    FPR = float(FPR)
    QPS = float(QPS)
    print(dataPathName, "./Ada_BF.py", FPR, QPS)

    BF_out = subprocess.check_output([sys.executable, "./Bloom_filter.py", "--data_path", dataPathName, "--size_of_BF", "200000"])
    # print(BF_out)
    FPR1, QPS1 = (BF_out.decode("utf-8")).split(' ')
    FPR1 = float(FPR1)
    QPS1 = float(QPS1)
    print(dataPathName, "./Bloom_filter.py", FPR1, QPS1)

    learned_BF_out = subprocess.check_output([sys.executable, "./learned_Bloom_Filter.py", "--data_path", dataPathName, "--size_of_LBF", "200000",  "--threshold_min", "0.5",   "--threshold_max", "0.95"])
    # print(learned_BF_out)
    FPR2, QPS2 = (learned_BF_out.decode("utf-8")).split(' ')
    FPR2 = float(FPR2)
    QPS2 = float(QPS2)
    print(dataPathName, "./learned_Bloom_Filter.py", FPR2, QPS2)

    disJoint_out = subprocess.check_output([sys.executable, "./disjoint_Ada_BF.py", "--data_path", "./Datasets/URL_data.csv", "--model_path", "./rf_model.p", "--size_of_Ada_BF", "200000",  "--num_group_min", "8", "--num_group_max", "12",  "--c_min", "1.6",  "--c_max", "2.5"])
    FPR3, QPS3 = (learned_BF_out.decode("utf-8")).split(' ')
    FPR3 = float(FPR3)
    QPS3 = float(QPS3)
    print(dataPathName, "./disjoint_Ada_BF.py", FPR3, QPS3)

    listJx = [QPS, QPS1, QPS2, QPS3]
    ListlistPx = [FPR, FPR1, FPR2, FPR3]
    for idx in range(len(listJx)):
        plt.scatter(listJx[idx], ListlistPx[idx], color = col, marker = markers[idx]) 
    


#Main code
plt.figure(figsize=(20,12))
runForData("./Datasets/URL_data.csv", 'b')
runForData("./Datasets/Malware_data.csv", 'g')
runForData("./Datasets-fakenews/Fake_news_score_clean.csv", 'r')
runForData("./Datasets-fakenews/Fake_news_score_full_clean.csv", 'k')

# legend
label_column = ["Ada_BF", "BF", "LBF"] # ["Ada_BF", "BF", "LBF", "Disjoint Ada_BF"]
label_row = ["URL_data", "Malware_data", "Fake_news_score_clean", "Fake_news_score_full_clean"]
rows = [mpatches.Patch(color='b'), mpatches.Patch(color='g'), mpatches.Patch(color='r'), mpatches.Patch(color='k')]
columns = [plt.plot([], [], "o", markerfacecolor='w', markeredgecolor='k')[0], 
    plt.plot([], [], "^", markerfacecolor='w', markeredgecolor='k')[0], 
    plt.plot([], [], "s", markerfacecolor='w', markeredgecolor='k')[0],
    plt.plot([], [], "x", markerfacecolor='w', markeredgecolor='k')[0]] # ,plt.plot([], [], "x", markerfacecolor='w', markeredgecolor='k')[0]

plt.legend(rows + columns, label_row + label_column)

plt.title("False Positive Rate vs Query per second")
plt.xlabel("Query per second")
plt.ylabel("False Positive Rate")
plt.show
plt.savefig(os.path.dirname(os.path.realpath(__file__))+"/Plot1")
plt.clf()