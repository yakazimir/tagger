import os

if __name__ == "__main__":
    train = {"ru":{},"en":{}}
    dev = {"ru":{},"en":{}}

    experiments = [os.path.join("../experiments",d) for d in os.listdir('../experiments')]
    # os.path.isdir(x)
    for ex in experiments:
        if os.path.isdir(ex):
            with open(ex+"/train_info.txt", 'r') as f:
                text = f.readlines()
                train_d = text[1][23:]

                if "ru" in ex:
                    print(float(text[0][22:]))
                    train["ru"][ex] = (float(train_d),float(text[0][22:]))
                    dev_d = text[2][17:]
                    dev["ru"][ex] = (float(dev_d),float(text[0][22:]))

                if "dev_en" in ex:
                    train["en"][ex] = (float(train_d),float(text[0][22:]))
                    dev_d = text[2][17:]
                    dev["en"][ex] = (float(dev_d),float(text[0][22:]))

    rumaximum_t = max(train["ru"], key=train["ru"].get)
    print("BEST ACCURACY ON TRAIN SET (ru): " +rumaximum_t + " " +str(train["ru"][rumaximum_t]))

    rumaximum_d = max(dev["ru"], key=dev["ru"].get)
    print("BEST ACCURACY ON DEV SET (ru): "+rumaximum_d + " " + str(dev["ru"][rumaximum_d]))


    enmaximum_t = max(train["en"], key=train["en"].get)
    print(enmaximum_t + " " + str(train["en"][enmaximum_t]))

    enmaximum_d = max(dev["en"], key=dev["en"].get)
    print(enmaximum_d + " " + str(dev["en"][enmaximum_d]))
