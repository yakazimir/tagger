
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":

    ## DO NOT MODIFY THIS 
    N = 5
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars
    fig, ax = plt.subplots()

    ## MODIFY THIS:
    accuracy = (.89,.90,.75,.65,.32)
    ax.set_xticklabels(('1+2+3', '1+2+3+4', '3+4+5', '5+6+7', '3+4+5'))

    ## DO NOT MODIFY THIS 
    rects2 = ax.bar(ind + width, accuracy, width, color='y')

    # DO NOT MODIFY THIS
    ax.set_ylabel('Accuracy')
    ax.set_xlabel('Features Used')
    ax.set_title('Importance of features')
    ax.set_xticks(ind + width)
    
    plt.show()
