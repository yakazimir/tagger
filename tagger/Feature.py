## put classes here related to feature extraction

class FeatureExtractorBase(object):
    pass



## SETTINGS


def params(config):
    """Loads dataset settings into a configuration

    :param config: the configuration
    :rtype: None  
    """
    group = OptionGroup(config,"tagger.Feature","Feature Extractor Settings")
    config.add_option_group(group)
