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

    @classmethod
    def init_features(cls,config,dataset):
        """Create class instance and init features from dataset

        :param config: the configuration 
        :param dataset: the dataset to extract features from
        """
        #### IMPLEMENT HERE
        #feature_map = find_name_features(dataset)
        #return cls(feature_map)

        ## TEMPORARY
        extractor = cls({})
        extractor.logger.warning('No features!')
        return extractor

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

def find_name_features(dataset):
    """Find the different features in train data

    :param dataset: the training dataset
    :rtype: dict
    :returns: a map of features with values
    """
    features = {}
    
    for (text,label) in dataset:

        ## feature template 1

        ## features template 2

        ## 
        pass

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
