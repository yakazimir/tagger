# -*- coding: utf-8 -*-

import sys 
from optparse import OptionParser,OptionGroup
from tagger import global_config

GENERAL_G = OptionGroup(global_config,"Tagger.__main__")

GENERAL_G.add_option(
    "--action",dest="action",default="train_tagger",
    help="The action to carry out [default='train_tagger']'"
)

GENERAL_G.add_option(
    "--dir",dest="dir",default=None,
    help="Place to store output [default=None]'"
)

global_config.add_option_group(GENERAL_G)

### this is the main execution point when calling the tagger module

if __name__ == "__main__":

    ## parses the command line arguments 
    config,_ = global_config.parse_args(sys.argv[1:])
