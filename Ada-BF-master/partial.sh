#!/bin/sh

python3 Bloom_filter.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_BF 150000  
python3 Bloom_filter.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_BF 200000
python3 Bloom_filter.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_BF 250000
python3 Bloom_filter.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_BF 300000
python3 Bloom_filter.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_BF 350000
python3 Bloom_filter.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_BF 400000
python3 Bloom_filter.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_BF 450000
python3 Bloom_filter.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_BF 500000

python3 learned_Bloom_filter.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_LBF 150000  --threshold_min 0.5   --threshold_max 0.95

python3 learned_Bloom_filter.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_LBF 200000  --threshold_min 0.5   --threshold_max 0.95

python3 learned_Bloom_filter.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_LBF 250000  --threshold_min 0.5   --threshold_max 0.95

python3 learned_Bloom_filter.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_LBF 300000  --threshold_min 0.5   --threshold_max 0.95

python3 learned_Bloom_filter.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_LBF 350000  --threshold_min 0.5   --threshold_max 0.95

python3 learned_Bloom_filter.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_LBF 400000 --threshold_min 0.5   --threshold_max 0.95

python3 learned_Bloom_filter.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_LBF 450000  --threshold_min 0.5   --threshold_max 0.95

python3 learned_Bloom_filter.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_LBF 500000  --threshold_min 0.5   --threshold_max 0.95

python3 Ada_BF.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_Ada_BF 150000  --num_group_min 8 --num_group_max 12  --c_min 1.6 --c_max 2.5

python3 Ada_BF.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_Ada_BF 200000  --num_group_min 8 --num_group_max 12  --c_min 1.6 --c_max 2.5

python3 Ada_BF.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_Ada_BF 250000  --num_group_min 8 --num_group_max 12  --c_min 1.6 --c_max 2.5

python3 Ada_BF.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_Ada_BF 300000  --num_group_min 8 --num_group_max 12  --c_min 1.6 --c_max 2.5

python3 Ada_BF.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_Ada_BF 350000  --num_group_min 8 --num_group_max 12  --c_min 1.6 --c_max 2.5

python3 Ada_BF.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_Ada_BF 400000  --num_group_min 8 --num_group_max 12  --c_min 1.6 --c_max 2.5

python3 Ada_BF.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_Ada_BF 450000  --num_group_min 8 --num_group_max 12  --c_min 1.6 --c_max 2.5

python3 Ada_BF.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --size_of_Ada_BF 500000  --num_group_min 8 --num_group_max 12  --c_min 1.6 --c_max 2.5


