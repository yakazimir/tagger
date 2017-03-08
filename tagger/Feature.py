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

    
