# -*- coding: utf-8 -*-

from optparse import OptionParser,OptionGroup
from BaseClass import TaggerSerializable

## put classes here related to feature extraction

class FeatureExtractor(TaggerSerializable):
    
    """Base class for implementing feature extractors"""
    
    def extract(self,data_instance):
        """Extract features for a given data instance 

        :param data_instance: the example to extract data for 
        """
        raise NotImplementedError


    @property
    def num_features(self):
        """Information about the number of features 

        :rtype: ine
        """
        raise NotImplementedError

    @classmethod
    def init_features(cls,config,dataset):
        """Create class instance and init features from dataset

        :param config: the configuration 
        :param dataset: the dataset to extract features from
        """
        raise NotImplementedError

    @classmethod
    def from_config(cls,config):
        """Set up the feature extractor, find basic features

        :param config: the main configuration 
        """
        raise ValueError('Config init not supported for FeatureExtractors!')

class NameFeatureExtractor(FeatureExtractor):
    """Feature extractor for getting name features and name classification"""

    def __init__(self,feature_map):
        """Ceates a NameFeatureExtractor instance

        :param features: Feature map for mapping features types to identifiers
        """
        self.feature_map = feature_map

    def extract(self,data_instance):
        """Add later"""
        labels = {"MALE": {}, "FEMALE": {}}

        extract_name_features_training(data_instance,labels,self.feature_map)
        return labels


    @classmethod
    def init_features(cls,config,dataset):
        """Create class instance and init features from dataset

        :param config: the configuration 
        :param dataset: the dataset to extract features from
        """
        #### IMPLEMENT HERE
        feature_map = find_name_features(dataset,config.templates,config.language)
        return cls(feature_map)

    @property
    def num_features(self):
        """Information about the number of features 

        :rtype: ine
        """
        return len(self.feature_map)

class RussianHeuristicExtractor():
    def extract(self):
        """ """
        labels = {"MALE": 1, "FEMALE": 0}
        return labels

    @classmethod
    def init_features(cls, config, dataset):
        """Create class instance and init features from dataset

        :param config: the configuration
        :param dataset: the dataset to extract features from
        """
        #### IMPLEMENT HERE
        for (text, label) in dataset:
            if text[-1] == u"а":
                labels["FEMALE"]+=
        return cls(feature_map)

## types

EXTRACTORS = {
    "names" : NameFeatureExtractor,
}

def Extractor(etype):
    """The class of extractor to use 

    :param etype: the extractor type 
    """
    e = EXTRACTORS.get(etype,None)
    if not e:
        raise ValueError('Unknown extractor: %s' % e)
    return e
    
def setup_extractor(config,dataset):
    """Setup the feature extractor 

    :param config: the main configuration 
    :param dataset: the dataset to use to extract features
    """
    eclass = Extractor(config.extractor)
    return eclass.init_features(config,dataset)

## EXTRACTOR SPECIFIC FUNCTIONS

def extract_name_features_training(name_input,labels,feature_map):
    """Extract features for names used for training or predicting

    :param name_input: the name which you want to extract features for
    :param labels: the two outputs
    """
    raw_name,_ = name_input
    first_letter = raw_name[0]

    mf1 =  feature_map.get(("MALE","F",first_letter),None)
    ff1 = feature_map.get(("FEMALE","F",first_letter),None)

    if mf1:
        labels["MALE"][mf1] = 1.0

    if ff1:
        labels["FEMALE"][ff1] = 1.0


    last_letter = raw_name[-1]

    mf2 = feature_map.get(("MALE","L",last_letter), None)
    ff2 = feature_map.get(("FEMALE","L",last_letter), None)
    if mf2:
        labels["MALE"][mf2] = 1.0

    if ff2:
        labels["FEMALE"][ff2] = 1.0

    vowels = set(["a", "e", "i", "o", "u"])
    num_vowels = len([c for c in raw_name if c in vowels])

    mf3 = feature_map.get(("MALE","Vow",num_vowels), None)
    ff3 = feature_map.get(("FEMALE", "Vow", num_vowels), None)

    if mf3:
        labels["MALE"][mf3] = num_vowels

    if ff3:
        labels["FEMALE"][ff3] = num_vowels


    last_three_letters = raw_name[-3:]

    mf4 = feature_map.get(("MALE", "End", last_three_letters), None)
    ff4 = feature_map.get(("FEMALE", "End", last_three_letters), None)

    if mf4:
        labels["MALE"][mf4] = 1.0

    if ff4:
        labels["FEMALE"][ff4] = 1.0

    mf5 = feature_map.get(("MALE", "NM", raw_name), None)
    ff5 = feature_map.get(("FEMALE", "NM", raw_name), None)

    if mf5:
        labels["MALE"][mf5] = 1.0

    if ff5:
        labels["FEMALE"][ff5] = 1.0


    letters = {c: raw_name.count(c) for c in raw_name}

    for (letter_type,count) in letters.iteritems():


        mf6 = feature_map.get(("MALE", "LT", letter_type), None)
        ff6 = feature_map.get(("FEMALE", "LT", letter_type), None)

        if mf6:
                labels["MALE"][mf6] = float(count)

        if ff6:
                labels["FEMALE"][ff6] = float(count)

    fl = raw_name[0]+raw_name[-1]

    mf7 = feature_map.get(("MALE", "FL", fl), None)
    ff7 = feature_map.get(("FEMALE", "FL", fl), None)

    if mf7:
       labels["MALE"][mf7] = 1.0

    if ff7:
        labels["FEMALE"][ff7] = 1.0

    comb = str(num_vowels) + last_letter

    mf8 = feature_map.get(("MALE", "LV", comb), None)
    ff8 = feature_map.get(("FEMALE", "LV", comb), None)

    if mf8:
        labels["MALE"][mf8] = 1.0

    if ff8:
        labels["FEMALE"][ff8] = 1.0

    num = len(raw_name)
    mf9 = feature_map.get(("MALE", "Nu", num), None)
    ff9 = feature_map.get(("FEMALE", "Nu", num), None)

    if mf9:
        labels["MALE"][mf9] = 1.0

    if ff9:
        labels["FEMALE"][ff9] = 1.0

    if num > 6:
        k_n = ">6"
    if num <= 6:
       k_n = "<=6"
    elif num <= 3:
        k_n = "<=3"

    mf10 = feature_map.get(("MALE", "Bn", k_n), None)
    ff10 = feature_map.get(("FEMALE", "Bn", k_n), None)

    if mf10:
        labels["MALE"][mf10] = 1.0

    if ff10:
        labels["FEMALE"][ff10] = 1.0

    if num_vowels > 3:
        v_n = ">3"
    if num_vowels <= 3:
       v_n = "<=3"
    elif num_vowels <= 1:
        v_n = "<=1"

    mf11 = feature_map.get(("MALE", "Vn", v_n), None)
    ff11 = feature_map.get(("FEMALE", "Vn", v_n), None)

    if mf11:
        labels["MALE"][mf11] = 1.0

    if ff11:
        labels["FEMALE"][ff11] = 1.0





def find_name_features(dataset,templates,language):
    """Find the different features in train data

    name input: Melanie 
    features: 

         first letter = 'm'        ("F",'m'),("F",'z')...
         last letter  = 'e'        ("L","e").... 
         last two letters = 'ie'
         .... 

    features = {

    ("F",'m') => 0 
    ("F",'z') => 1
    .....

    ("L","e") => j

    .. => n
    }
        

    :param dataset: the training dataset
    :rtype: dict
    :returns: a map of features with values
    """
    features = {}
    if language == "en":
        vowels = set(["a","e","i","o","u"])
    else:
        vowels = set([u"а", u"е", u"и", u"о", u"у"])
    templates = [int(t) for t in templates.split("+")]
    
    for (text,label) in dataset:

        first_letter = text[0]
        if 1 in templates:
            identifier = (label,"F",first_letter)

            if identifier not in features:
                features[identifier] = len(features)

        ## features template 2 : LAST LETTER FEATURE
        last_letter = text[-1]
        if 2 in templates:
            identifier = (label,"L",last_letter)

            if identifier not in features:
                features[identifier] = len(features)


        ## feature template 3:
        num_vowels = len([c for c in text if c in vowels])
        if 3 in templates:
            tv_identifier = (label,"Vow",num_vowels)
            if tv_identifier not in features:
                features[tv_identifier] = len(features)

        ## feature template 4:
        last_three_letters = text[-3:]
        if 4 in templates:
            tl_identifier = (label,"End", last_three_letters)
            if tl_identifier not in features:
                features[tl_identifier] = len(features)

        ## feature template 5:
        if 5 in templates:
            nm_identifier = (label,"NM", text)
            if nm_identifier not in features:
                    features[nm_identifier] = len(features)

        ## feature template 6:
        letters =  {c: text.count(c) for c in text}
        if 6 in templates:
            for (letter_type, count) in letters.iteritems():
                lt_identifier = (label,"LT",letter_type)
                if lt_identifier not in features:
                    features[lt_identifier] = len(features)

        ## feature template 7:
        fandl = text[0] + text[-1]
        if 7 in templates:
            fl_identifier = (label, "FL", fandl)
            if fl_identifier not in features:
                features[fl_identifier] = len(features)

        ## feature template 8:
        volwlast = str(num_vowels) + last_letter
        if 8 in templates:
            lastv_identifier = (label, "LV", volwlast)
            if lastv_identifier not in features:
                features[lastv_identifier] = len(features)

        ## feature template 9:
        number = len(text)
        if 9 in templates:
            nu_identifier = (label, "Nu", number)
            if nu_identifier not in features:
                features[nu_identifier] = len(features)

        ##
        if 10 in templates:
            if number >6:
                b_n_identifier = (label, "Bn", ">6")
            if number <= 6:
                b_n_identifier = (label, "Bn", "<=6")
            elif number <= 3:
                b_n_identifier = (label, "Bn", "<=3")

            if b_n_identifier not in features:
                features[b_n_identifier] = len(features)

        if 11 in templates:
            if num_vowels >3:
                v_n_identifier = (label, "Vn", ">3")
            if num_vowels <= 3:
                v_n_identifier = (label, "Vn", "<=3")
            elif num_vowels <= 1:
                v_n_identifier = (label, "Vn", "<=1")

            if v_n_identifier not in features:
                features[v_n_identifier] = len(features)
    return features
        


def extract_name_features(instance):
    pass
    
## SETTINGS

def params(config):
    """Loads dataset settings into a configuration

    :param config: the configuration
    :rtype: None  
    """
    group = OptionGroup(config,"tagger.Feature","Feature Extractor Settings")

    group.add_option(
        "--extractor",dest="extractor",default="names",
        help="The type of feature extractor to use [default='']"
    )

    group.add_option(
        "--templates",dest="templates",default="1+2+3+4+5",
        help="The type of templates to use [default='']"
    )
    group.add_option(
        "--language", dest="language", default="en",
        help="The language to use [default='en']"
    )

    config.add_option_group(group)
