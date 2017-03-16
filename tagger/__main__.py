# -*- coding: utf-8 -*-

import traceback 
import sys
import os
import logging
from optparse import OptionGroup
from tagger import global_config
from tagger.Tagger import run_tagger
from tagger.util import *

GENERAL_G = OptionGroup(global_config,"Tagger.__main__")

GENERAL_G.add_option(
    "--action",dest="action",default="train_tagger",
    help="The action to carry out [default='train_tagger']"
)

GENERAL_G.add_option(
    "--dir",dest="dir",default=None,
    help="Place to store output [default=None]'"
)

GENERAL_G.add_option(
    "--override",dest="override",default=False,
    help="Override an exisiting working directory [default=False]"
)

GENERAL_G.add_option(
    "--backup",dest="backup",default=False,
    help="Backup models/information when possible [default=False]"
)

global_config.add_option_group(GENERAL_G)

### this is the main execution point when calling the tagger module

if __name__ == "__main__":
    
    ## parses the command line arguments 
    config,_ = global_config.parse_args(sys.argv[1:])

    try: 
        ## setup up logger and experiment directory
        if config.dir:
            log_file = os.path.join(config.dir,"experiment.log")
            logging.basicConfig(filename=log_file,level=logging.INFO)
            create_wdir(config)
        else:
            logging.basicConfig(level=logging.INFO)

        ## tries to run a tagger
        run_tagger(config)
        
    except Exception,e:
        traceback.print_exc(file=sys.stdout)
