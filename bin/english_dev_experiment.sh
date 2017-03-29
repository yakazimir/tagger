experiment_number=0

for language in en ru;
do
    for features in 1 2 3 4 5 6 7 8 9 10 11 1+2 1+2+3 1+2+3+4 1+2+3+4+5+6 1+2+3+4+5+6+7 1+2+3+4+5+6+7+8 1+2+3+4+5+6+7+8+9 1+2+3+4+5+6+7+8+9+10+11;
        do
        for shuffle_setting in "--shuffle=false" "--shuffle=true";
        do
            for learner in perceptron aperceptron;
                do
                wdir=experiments/dev_$language+$features+$shuffle_settings+$learner
                if [ $language == "ru" ]; then
                 loc=data/names/ru
                 fi

                if [ $language == "en" ]; then
                 loc=data/names/en
                 fi
                ./run.sh --loc $loc --dir $wdir --iters 1000000000 --learner $learner --override=true --templates $features --language $language
                echo "finished experiment: " $experiment_number
                experiment_number=$((experiment_number + 1))
            done
        done
    done
done


