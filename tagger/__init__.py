

## PROJECT INFORMATION 

__author__ = "Kyle Richardson and Elena Mokeeva"
__license__ = "GPL2"
__url__ = "https://github.com/yakazimir/tagger"
__keywords__ = [
    "NLP","POS","Machine Learning","Perceptron",
    "Online Learning","Tagging",
]
__copyright__ = ""
__version__ = "0.1"

description = """
Tagger: a python library for text tagging
"""

USAGE = """usage: python -m tagger [options] [--help]"""


## creates a configuration from different sub modules
from optparse import OptionParser,OptionGroup
from tagger.Dataset   import params as data_params
from tagger.Learner   import params as learn_params
from tagger.Optimizer import params as opt_params
from tagger.Tagger    import params as tag_params
from tagger.Feature   import params as feat_params

## global configuration parser
global_config = OptionParser(usage=USAGE,description=description)

## add individual options to config parser 
data_params  (global_config)
learn_params (global_config)
opt_params   (global_config)
tag_params   (global_config)
feat_params  (global_config)

## default configuration settings
default_config,_ = global_config.parse_args([])
