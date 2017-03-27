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
        feature_map = find_name_features(dataset)
        return cls(feature_map)

    @property
    def num_features(self):
        """Information about the number of features 

        :rtype: ine
        """
        return len(self.feature_map)

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

    if ("MALE","F",first_letter) in feature_map :
        labels["MALE"][mf1] = 1.0

    if ("FEMALE","F",first_letter) in feature_map:
        labels["FEMALE"][ff1] = 1.0


    last_letter = raw_name[-1]
    mf2 = feature_map.get(("MALE","L",last_letter), None)
    ff2 = feature_map.get(("FEMALE","L",last_letter), None)
    if ("MALE","L",last_letter) in feature_map:
        labels["MALE"][mf2] = 1.0

    if ("FEMALE", "L", last_letter) in feature_map:
        labels["FEMALE"][ff2] = 1.0

    vowels = set(["a", "e", "i", "o", "u"])
    num_vowels = len([c for c in raw_name if c in vowels])
    mf3 = feature_map.get(("MALE","Vow",num_vowels), None)
    ff3 = feature_map.get(("FEMALE", "Vow", num_vowels), None)

    if ("MALE","Vow",num_vowels) in feature_map:
        labels["MALE"][mf3] = num_vowels

    if ("FEMALE", "Vow", num_vowels) in feature_map:
        labels["FEMALE"][ff3] = num_vowels


    last_three_letters = raw_name[-3:]
    mf4 = feature_map.get(("MALE", "End", last_three_letters), None)
    ff4 = feature_map.get(("FEMALE", "End", last_three_letters), None)

    if ("MALE", "End", last_three_letters) in feature_map:
        labels["MALE"][mf4] = 1.0

    if ("FEMALE", "End", last_three_letters) in feature_map:
        labels["FEMALE"][ff4] = 1.0


    mf5 = feature_map.get(("MALE", "NM", raw_name), None)
    ff5 = feature_map.get(("FEMALE", "NM", raw_name), None)

    if ("MALE", "NM", raw_name) in feature_map:
        labels["MALE"][mf5] = 1.0

    if ("FEMALE", "NM", raw_name) in feature_map:
        labels["FEMALE"][ff5] = 1.0


    letters = {c: raw_name.count(c) for c in raw_name}

    for (letter_type,count) in letters.iteritems():


        mf6 = feature_map.get(("MALE", "LT", letter_type), None)
        ff6 = feature_map.get(("FEMALE", "LT", letter_type), None)

        if ("MALE", "L", letter_type) in feature_map:
            labels["MALE"][mf6] = float(count)

        if ("FEMALE", "LT", letter_type) in feature_map:
            labels["FEMALE"][ff6] = float(count)



def find_name_features(dataset):
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
    vowels = set(["a","e","i","o","u"])

    
    for (text,label) in dataset:

        ## feature template 1 : FIRST LETTER FEATURE
        first_letter = text[0]
        identifier = (label,"F",first_letter)

        if identifier not in features:
            features[identifier] = len(features)

        ## features template 2 : LAST LETTER FEATURE
        last_letter = text[-1]
        identifier = (label,"L",last_letter)

        if identifier not in features:
            features[identifier] = len(features)


        ## feature template 3:
        num_vowels = len([c for c in text if c in vowels])

        """if num_vowels <= 0:
            v_identifier = ("NV",)
        if num_vowels >= 1:
            v_identifier = (">=1",)
        if num_vowels >= 5:
            v_identifier = (">=5,",)

        if v_identifier not in features: 
            features[v_identifier] = len(features)"""
        tv_identifier = (label,"Vow",num_vowels)
        if tv_identifier not in features:
            features[tv_identifier] = len(features)

        ## feature template 4:
        last_three_letters = text[-3:]
        tl_identifier = (label,"End", last_three_letters)
        if tl_identifier not in features:
            features[tl_identifier] = len(features)

        ## feature template 5:
        nm_identifier = (label,"NM", text)
        if nm_identifier not in features:
            features[nm_identifier] = len(features)

        ## feature template 6:
        letters =  {c: text.count(c) for c in text}
        for (letter_type, count) in letters.iteritems():
            lt_identifier = (label,"LT",letter_type)
            if lt_identifier not in features:
                features[lt_identifier] = len(features)

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
        "--templates",dest="templates",default="",
        help="The type of templates to use [default='']"
    )

    config.add_option_group(group)
