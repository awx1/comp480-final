#!/bin/sh

python3 disjoint_Ada_BF.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --model_path ./rf_model.p --size_of_Ada_BF 150000  --num_group_min 8 --num_group_max 12  --c_min 1.6 --c_max 2.5
printf "Done with 1\n"
python3 disjoint_Ada_BF.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --model_path ./rf_model.p --size_of_Ada_BF 200000  --num_group_min 8 --num_group_max 12  --c_min 1.6 --c_max 2.5
printf "Done with 2\n"
python3 disjoint_Ada_BF.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --model_path ./rf_model.p --size_of_Ada_BF 250000  --num_group_min 8 --num_group_max 12  --c_min 1.6 --c_max 2.5
printf "Done with 3\n"
python3 disjoint_Ada_BF.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --model_path ./rf_model.p --size_of_Ada_BF 300000  --num_group_min 8 --num_group_max 12  --c_min 1.6 --c_max 2.5
printf "Done with 4\n"
python3 disjoint_Ada_BF.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --model_path ./rf_model.p --size_of_Ada_BF 350000  --num_group_min 8 --num_group_max 12  --c_min 1.6 --c_max 2.5
printf "Done with 5\n"
python3 disjoint_Ada_BF.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --model_path ./rf_model.p --size_of_Ada_BF 400000  --num_group_min 8 --num_group_max 12  --c_min 1.6 --c_max 2.5
printf "Done with 6\n"
python3 disjoint_Ada_BF.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --model_path ./rf_model.p --size_of_Ada_BF 450000  --num_group_min 8 --num_group_max 12  --c_min 1.6 --c_max 2.5
printf "Done with 7\n"
python3 disjoint_Ada_BF.py --data_path ./Datasets-fakenews/Fake_news_score_full_clean.csv --model_path ./rf_model.p --size_of_Ada_BF 500000  --num_group_min 8 --num_group_max 12  --c_min 1.6 --c_max 2.5
printf "Done with 8\n"


