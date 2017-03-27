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
    "--log",dest="log",default='info',
    help="Set the debug level [default='info']"
)

LEVELS = {
    "info"    : logging.INFO,
    "debug"   : logging.DEBUG,
    "error"   : logging.ERROR,
    "warning" : logging.WARNING,
}

global_config.add_option_group(GENERAL_G)

module_logger = logging.getLogger("tagger.__main__")

def setup_wdir(config,sysarg,level):
    """Setup a working directory for storing experiment files/runs as
    well as the logging information.

    :param config: the main configuration 
    :param sysarg: cli input to the module 
    :param level: the logging level
    :rtype: None 
    """
    ## create the working directory
    create_wdir(config)
    create_run_script(sysarg,config)

    ## setting the logger 
    log_file  = os.path.join(config.dir,"experiment.log")
    logging.basicConfig(filename=log_file,level=level)

### this is the main execution point when calling the tagger module
if __name__ == "__main__":

    ## parses the command line arguments 
    config,_ = global_config.parse_args(sys.argv[1:])

    try:

        log_level = LEVELS.get(config.log,logging.INFO)
        
        ## setup up logger and experiment directory
        if config.dir:
            setup_wdir(config,sys.argv[1:],log_level)
        else:
            logging.basicConfig(level=log_level)

        ## tries to run a tagger
        run_tagger(config)
        
    except Exception,e:
        module_logger.error(e,exc_info=True)
        traceback.print_exc(file=sys.stdout)

    ## backup the configuration 
    finally:
        pass
