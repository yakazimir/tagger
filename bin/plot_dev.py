
import os
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":

    ## DO NOT MODIFY THIS 

    ## number of positions?
    N = 6
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars
    fig, ax = plt.subplots()

    ## MODIFY THIS:
    perceptron_accuracy = (.89,.90,.75,.65,.32,.11)
    aperceptron_accuracy = (.89,.90,.75,.65,.32,.11)

    train = {"ru": {}, "en": {}}
    dev = {"ru": {}, "en": {}}
    features = {}

    experiments = [os.path.join("../experiments", d) for d in os.listdir('../experiments')]
    for ex in experiments:
        if os.path.isdir(ex):
            with open(ex + "/train_info.txt", 'r') as f:
                text = f.readlines()
                train_d = text[1][23:]
                dev_d = text[2][17:]

                if "ru" in ex:
                    train["ru"][ex] = (float(train_d), float(text[0][22:]))
                    dev["ru"][ex] = (float(dev_d), float(text[0][22:]))

                if "dev_en" in ex:
                    train["en"][ex] = (float(train_d), float(text[0][22:]))
                    dev["en"][ex] = (float(dev_d), float(text[0][22:]))
    entop = sorted(dev["en"].items(), key=lambda z : z[-1][0], reverse=True)[:10]
    for (result,value) in entop:
        info = result[22:]
        combo = info.split("++")[0]
        #print(combo + str(value))
        features[combo] = [None,None]

    print(features)
        #print (dev["en"])
    feutures ={i:[None,None] for i in ["1","2", "3"]}

    features_l = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "1+2", "1+2+3", "1+2+3+4", "1+2+3+4+5+6", "1+2+3+4+5+6+7", "1+2+3+4+5+6+7+8", "1+2+3+4+5+6+7+8+9", "1+2+3+4+5+6+7+8+9+10+11"]
    feutures = {i: [None, None] for i in features}
    print(features)
    for combination in features:
        #print(combination)
        for infos in dev["en"]:
            #print (dev["en"][infos])
            #print(infos)
            if "+" + combination +"++perceptron" in infos:
                #print(features[combination] + infos)
                features[combination][0] = dev["en"][infos][0]
                #print(combination + infos)
                #print (features[combination])"""

            if combination + "++aperceptron" in infos:
                print(infos)
                features[combination][1] = dev["en"][infos][0]
                #print (features)"""
        if features[combination][0]!= features[combination][1]:
            print ("AAAAAAA")
            print features[combination]

    print(features)
    ax.set_xticklabels(('1+2+3', '1+2+3+4', '3+4+5', '5+6+7', '3+4+5','10+11'))

    ## DO NOT MODIFY THIS 
    rects2 = ax.bar(ind, perceptron_accuracy, width, color='y')
    rects1 = ax.bar(ind + width, aperceptron_accuracy, width, color='r')

    # DO NOT MODIFY THIS
    ax.set_ylabel('Accuracy')
    ax.set_xlabel('Features Used')
    ax.set_title('Importance of features')
    ax.set_xticks(ind + width)

    ax.legend((rects1[0],rects2[0]),('Perceptron',"APerceptron"))

    plt.show()
