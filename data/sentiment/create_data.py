# -*- coding: utf-8 -*-

import os
import codecs
import math
import random
import re

here = curr_path = os.path.abspath(os.path.dirname(__file__))
origin_data = os.path.join(here, 'restaurantData.txt')

if __name__ == "__main__":
    n_recommend = set()
    p_recommend = set()
    total_data = []
    ## male names
    with codecs.open(origin_data, encoding='utf-8') as origin:
        for line in origin:
            line = line.strip()
            info = line.split("***")[0].strip()
            text = line.split("***")[1].strip()
            if "-1-" in info:
                total_data.append((text,"positiv"))

            if "-0-" in info:
                total_data.append((text, "negativ"))

    total_size = len(total_data)
    print(total_data)

    ## break into train/test/validation
    indices = range(0, total_size)
    random.seed(42)
    random.shuffle(indices)

    num_train = int(total_size * 0.7)
    num_test = int(total_size * .15)

    train_indices = [indices[i] for i in range(0, num_train)]
    test_indices = [indices[i] for i in range(num_train, num_train + num_test)]
    valid_indices = [indices[i] for i in range(num_train + num_test, num_train + num_test + num_test)]

    # train
    train_data = os.path.join(here, "train.txt")
    valid_data = os.path.join(here, "valid.txt")
    test_data = os.path.join(here, "test.txt")
    train_stats = {"n": 0, "p": 0}

    ## print the training data
    with codecs.open(train_data, 'w', encoding='utf-8') as train:
        for tindex in train_indices:
            data_point = total_data[tindex]
            print >> train, "%s\t%s" % (data_point[0], data_point[1])
            if data_point[1] == "negativ":
                train_stats["n"] += 1
            else:
                train_stats["p"] += 1

    vtotal = 0.0
    vcorrect = 0.0

    ## print the validation data
    with codecs.open(valid_data, 'w', encoding='utf-8') as valid:
        for tindex in valid_indices:
            data_point = total_data[tindex]
            label = data_point[1]
            ninput = data_point[0]
            print >> valid, "%s\t%s" % (data_point[0], data_point[1])




    with codecs.open(test_data,'w',encoding='utf-8') as test:
        for tindex in test_indices:
            data_point = total_data[tindex]
            label = data_point[1]
            ninput = data_point[0]
            print >>test,"%s\t%s" % (data_point[0],data_point[1])

