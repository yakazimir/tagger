# -*- coding: utf-8 -*-

import os
import codecs
import math
import random


here = curr_path = os.path.abspath(os.path.dirname(__file__))
males   = os.path.join(here,'males_wikipedia.txt')
females = os.path.join(here,'females_wikipedia.txt')

if __name__ == "__main__":
    mnames = set()
    fnames = set()

    with codecs.open(males,encoding='utf-8') as male_names:
        for m in male_names:
            mnames.add(m.strip())

    with codecs.open(females,encoding='utf-8') as female_names:
        for f in female_names:
            fnames.add(f.strip())

    ## bring together the data
    total_data = [(m,"MALE") for m in mnames]+[(f,"FEMALE") for f in fnames]
    total_size = len(total_data)

    ## break into train/test/validation
    indices = range(0,total_size)
    random.seed(42)
    random.shuffle(indices)

    num_train = int(total_size*0.7)
    num_test = int(total_size*.15)

    train_indices = [indices[i] for i in range(0,num_train)]
    test_indices = [indices[i] for i in range(num_train,num_train+num_test)]
    valid_indices = [indices[i] for i in range(num_train+num_test,num_train+num_test+num_test)]


    ## make the data
    ##################

    # train
    train_data = os.path.join(here,"train.txt")
    valid_data = os.path.join(here,"valid.txt")
    test_data = os.path.join(here,"test.txt")
    train_stats = {"m":0,"f":0}

    ## print the training data 
    with codecs.open(train_data,'w',encoding='utf-8') as train:
        for tindex in train_indices:
            data_point = total_data[tindex]
            print >>train,"%s\t%s" % (data_point[0],data_point[1])
            if data_point[1] == "MALE": train_stats["m"] += 1
            else: train_stats["f"] += 1

    vtotal = 0.0
    vcorrect = 0.0
    
    ## print the validation data
    with codecs.open(valid_data,'w',encoding='utf-8') as valid:
        for tindex in valid_indices:
            data_point = total_data[tindex]
            label = data_point[1]
            ninput = data_point[0]
            print >>valid,"%s\t%s" % (data_point[0],data_point[1])

            # if label == "MALE": vcorrect += 1.0
            # vtotal += 1.0

            if ninput[-1] == u'а':
                if label == "FEMALE":
                    vcorrect += 1.0
            else:
                if label == "MALE":
                    vcorrect += 1.0

            vtotal += 1.0

    ### majority baseline on validation 
    print vcorrect/vtotal

    ttotal = 0.0
    tcorrect = 0.0

    with codecs.open(test_data,'w',encoding='utf-8') as test:
        for tindex in test_indices:
            data_point = total_data[tindex]
            label = data_point[1]
            ninput = data_point[0]
            print >>test,"%s\t%s" % (data_point[0],data_point[1])

            if ninput[-1] == u'а':
                if label == "FEMALE":
                    tcorrect += 1.0
            else:
                if label == "MALE":
                    tcorrect += 1.0

            ttotal += 1.0

    print tcorrect/ttotal
            
            
