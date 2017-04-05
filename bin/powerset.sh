#!/bin/bash

my_list=(1,2,3,4,5,6,7,8,9,10,11)
combination=()
experiment_number = 0
number = 0
# Prepare the indicator, set to all zeros.
binary=()
for (( i=0; i<=11; i++ )) ; do
    binary[i]=0
done

while (( ! binary[11] )) ; do
    combination=()
    # Print the subset.
    #printf '{ '
    for (( j=1; j<11; j++ )) ; do
        (( i=j+1 ))
        (( binary[j] )) && combination="$combination+$j";
    done
    number=$((number + 1))
    echo "number: " $number
    for language in en ru;
        do
        for learner in perceptron aperceptron;
            do
                wdir=experiments/dev_$language+$combination+$learner
                if [ $language == "ru" ]; then
                 loc=data/names/ru
                 #echo "ru"
                 fi

                if [ $language == "en" ]; then
                 loc=data/names/en
                 #echo "en"
                 fi

                if [ "$combination" != "" ] ; then
                    echo $combination
                    #./run.sh --loc $loc --dir $wdir --iters 100 --learner $learner --override=true --templates "$combination" --language $language
                    echo "finished experiment: " $experiment_number
                    experiment_number=$((experiment_number + 1))
                fi
        done
    done
    #printf '\n'

    # Increment the indicator.
    for (( i=0; binary[i]==1; i++ )) ; do
        binary[i]=0
    done
    binary[i]=1
done