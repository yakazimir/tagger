# -*- coding: utf-8 -*-

import sys 
from optparse import OptionParser
from tagger import description


## program usage 
USAGE = """usage: python -m tagger [options]"""

## module components

GROUPS = {
    "tagger.Dataset"   : "Managing datasets",
    "tagger.Learner"   : "Handles Learning Models",
    "tagger.Optimizer" : "Handles Optimization Procedures",
    "tagger.Feature"   : "Handles Feature Representations",
    "tagger.Tagger"    : "Hander tagger implementations",
    "General"          : "General tagger settings",
}


CONFIG_P = OptionParser(usage=USAGE,description=description)

## general options

CONFIG_P.add_option(
    "--action",dest="action",default="train_tagger",
    help="The action to carry out [default='train_tagger']'"
)

CONFIG_P.add_option(
    "--encoding",dest="encoding",default="utf-8",
    help="The main encoding [default='utf-8']'"
)

CONFIG_P.add_option(
    "--lower",dest="lower",default=True,
    help="Lowercase text when possible [default=True]'"
)

### this is the main execution point when calling the tagger module

if __name__ == "__main__":

    ## parses the command line arguments 
    config,_ = CONFIG_P.parse_args(sys.argv[1:])

    print config.action

    ## for how,
    #CONFIG_P.print_help()

