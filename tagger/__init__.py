

## PROJECT INFORMATION 

__author__ = "Kyle Richardson and Elena Mokeeva"
__license__ = "GPL2"
__url__ = ""
__keywords__ = [
    "NLP","POS","Machine Learning","Perceptron",
    "Online Learning",
]
__copyright__ = ""
__version__ = "0.1"

description = """
Tagger: a python library for text tagging
"""

USAGE = """usage: python -m tagger [options]"""

## creates a configuration from different sub modules
from optparse import OptionParser,OptionGroup
from tagger.Dataset   import params as data_params
from tagger.Learner   import params as learn_params
from tagger.Optimizer import params as opt_params

global_config = OptionParser(usage=USAGE,description=description)

## add individual options 
data_params  (global_config)
learn_params (global_config)
opt_params   (global_config)
