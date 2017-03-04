# -*- coding: utf-8 -*-

import sys 
from optparse import OptionParser,OptionGroup
from tagger import description
from tagger.Dataset import params as data_params
from tagger.Learner import params as learn_params
from tagger.Optimizer import params as opt_params

## program usage

USAGE = """usage: python -m tagger [options]"""

## overall configuration 
    
CONFIG_P = OptionParser(usage=USAGE,description=description)

## add module configuration settings
data_params(CONFIG_P)
learn_params(CONFIG_P)
opt_params(CONFIG_P)

## general options

GENERAL_G = OptionGroup(CONFIG_P,"Tagger.__main__")

GENERAL_G.add_option(
    "--action",dest="action",default="train_tagger",
    help="The action to carry out [default='train_tagger']'"
)

CONFIG_P.add_option_group(GENERAL_G)

### this is the main execution point when calling the tagger module

if __name__ == "__main__":

    ## parses the command line arguments 
    config,_ = CONFIG_P.parse_args(sys.argv[1:])

    print config.action

    ## for how,
    #CONFIG_P.print_help()

