import sys
import subprocess
import matplotlib.pyplot as plt
import os

def runAda(dataPathName, size):
    Ada_BF_out = subprocess.check_output([sys.executable, "./Ada_BF.py", "--data_path", dataPathName, "--size_of_Ada_BF", size,  "--num_group_min", "8",  "--num_group_max", "12",  "--c_min", "1.6",  "--c_max", "2.5"])
    FPR, QPS = (Ada_BF_out.decode("utf-8")).split(' ')
    FPR = float(FPR)
    QPS = float(QPS)
    return (FPR, QPS)

def runBF(dataPathName, size):
    BF_out = subprocess.check_output([sys.executable, "./Bloom_filter.py", "--data_path", dataPathName, "--size_of_BF", size])
    # print(BF_out)
    FPR1, QPS1 = (BF_out.decode("utf-8")).split(' ')
    FPR1 = float(FPR1)
    QPS1 = float(QPS1)
    return (FPR1, QPS1)

def runLearned(dataPathName, size):
    learned_BF_out = subprocess.check_output([sys.executable, "./learned_Bloom_Filter.py", "--data_path", dataPathName, "--size_of_LBF", size,  "--threshold_min", "0.5",   "--threshold_max", "0.95"])
    # print(learned_BF_out)
    FPR2, QPS2 = (learned_BF_out.decode("utf-8")).split(' ')
    FPR2 = float(FPR2)
    QPS2 = float(QPS2)
    return (FPR2, QPS2)

def runDis(dataPathName, size):
    disJoint_out = subprocess.check_output([sys.executable, "./disjoint_Ada_BF.py", "--data_path", dataPathName, "--model_path", "./rf_model.p", "--size_of_Ada_BF", size,  "--num_group_min", "8", "--num_group_max", "12",  "--c_min", "1.6",  "--c_max", "2.5"])
    # print(learned_BF_out)
    FPR2, QPS2 = (disJoint_out.decode("utf-8")).split(' ')
    FPR2 = float(FPR2)
    QPS2 = float(QPS2)
    return (FPR2, QPS2)


datasets = ["./Datasets/URL_data.csv", "./Datasets/Malware_data.csv", "./Datasets-fakenews/Fake_news_score_clean.csv", "./Datasets-fakenews/Fake_news_score_full_clean.csv"]
# datasets = ["./Datasets/URL_data.csv"]
ranges = [range(200000, 550000, 50000), range(100000, 350000, 50000), range(150000, 500000, 50000), range(150000, 500000, 50000)]

for idx, sett in enumerate(datasets):
    plt.figure(figsize=(20,12))
    # #Ada
    listJx = []
    ListlistPx = []
    for size in ranges[idx]:
        tupp = runAda(sett, str(size))
        listJx.append(size)
        ListlistPx.append(tupp[0])
    plt.plot(listJx, ListlistPx, linestyle = "solid", marker = "x")

    #BF
    listJx = []
    ListlistPx = []
    for size in ranges[idx]:
        tupp = runBF(sett, str(size))
        listJx.append(size)
        ListlistPx.append(tupp[0])
    plt.plot(listJx, ListlistPx, linestyle = "solid", marker = "x")

    #BFLearned
    listJx = []
    ListlistPx = []
    for size in ranges[idx]:
        tupp = runLearned(sett, str(size))
        listJx.append(size)
        ListlistPx.append(tupp[0])
    plt.plot(listJx, ListlistPx, linestyle = "solid", marker = "x")

    #DisJoint
    listJx = []
    ListlistPx = []
    for size in ranges[idx]:
        tupp = runDis(sett, str(size))
        listJx.append(size)
        ListlistPx.append(tupp[0])
    plt.plot(listJx, ListlistPx, linestyle = "solid", marker = "x")

    plt.legend(["Ada-BF", "BloomFilter", "Learned BloomFilter", "DisJoint Ada-BF"])
    plt.title("False Positive Rate vs Bitmap Size")
    plt.xlabel("Bitmap Size")
    plt.ylabel("False Positive Rate")
    plt.show
    plt.savefig(os.path.dirname(os.path.realpath(__file__))+sett[2:-4])
    plt.clf()


    


# #Main code
# runForData("./Datasets/URL_data.csv")
# runForData("./Datasets/Malware_data.csv")
# runForData("./Datasets-fakenews/Fake_news_score_clean.csv")
# runForData("./Datasets-fakenews/Fake_news_score_full_clean.csv")

# plt.legend(["URL_data", "Malware_data", "Fake_news_score_clean", "Fake_news_score_full_clean"])
# plt.title("False Positive Rate vs Query per second")
# plt.xlabel("Query per second")
# plt.ylabel("False Positive Rate")
# plt.show
# plt.savefig(os.path.dirname(os.path.realpath(__file__))+"/Plot1")
# plt.clf()