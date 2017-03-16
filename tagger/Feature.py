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
        extractor = cls.({})
        extractor.logger.warning('No features!')
        return extractor 
    
## SETTINGS

def params(config):
    """Loads dataset settings into a configuration

    :param config: the configuration
    :rtype: None  
    """
    group = OptionGroup(config,"tagger.Feature","Feature Extractor Settings")

    group.add_option(
        "--extractor",dest="extractor",default="",
        help="The type of feature extractor to use [default='']"
    )
    
    config.add_option_group(group)
