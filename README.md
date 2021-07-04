# COMP 480: An Exploratory Analysis of Fake News Detection on Adaptive Learned Bloom FIlters

## Introduction
#### We implemented four machine learning-driven bloom filters and examined the accuracy-resource tradeoffs. The following set of algorithms: bloom filters, learned bloom filters, sandwiched learned bloom filters, adaptive bloom filters, and disjoint adaptive bloom filters were compared and contrasted.1 More specifically, we wanted to focus on conducting further exploration into the reproducibility and extensibility of the previous work. Hence, we followed the process outlined in the paper as well as validated the results presented.

#### We chose two new datasets, beyond the ones used in the paper, for tackling the problem presented in the testing purposes. Under discussion with our mentor Zhaozhuo Xu, we settled on the theme of fake news detection. Hence, both datasets applied in this project are related to this category with the focus of one on mimicking the size constraints posed in the previous work and the other tackling large memory usage.

#### Initially, we focused on the reproducibility of previous results but we also examined the false positive rate vs. queries per second and the effects of hyper-parameters for learning on the aforementioned responses, across all datasets.

## Data Gathering
#### We used language processing libraries to tokenize the headlines and article bodies. We then apply the TF-IDF vectorizer to appropriately process input for the random forest. 

#### The pre-processing consisted of reducing the data to textual data, applying the Porter Stemmer algorithm, and then removing anystop words across aggregated NLP stop words. We vectorize the titles and text using TF-IDF vectorization and train the random forest classifier on the processed data. TF-IDF is a text vectorizer that combines the term frequency within documents to the inverse document frequency.

#### We wanted to generate a dataset that mimicked the size constraints imposed on the previous work model. We found that 20 leaf nodes and 40 decision trees resulted in the closest memory usage of 155 KB.

#### Another focus was to benchmark the minimized memory dataset against a non-parameterized random forest to distinguish the extent of the memory-to-accuracy tradeoff. A full random forest contains 100 decision trees with an unbounded number of leaf nodes. For comparison, this model resulted in a memory usage of 384 MB.

#### By applying the models to the entirety of the training and testing dataset, we can obtain score measurements that reflect the score measurements used in the paper. Now, we can pipeline the new data into the bloom filter algorithms proposed in the paper.

## Conclusion
#### The scope of this project was limited to experimental replication and application of new data. As discussed, we were able to find flaws in the wide-scale usability of this application towards different datasets. We achieved our goals but would definitely look forward to expanding the technical aspects of this project as well in the future.
#### Another direction that may be interesting to pursue is following up with the future works of detecting near matches for a fake news detection application using learned, distance sensitive bloom filters.
