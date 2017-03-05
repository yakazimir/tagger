# -*- coding: utf-8 -*-

from optparse import OptionParser,OptionGroup
from tagger.BaseClass import TaggerSerializable
from Optimizer import setup_optimizer

class TaggerBase(TaggerSerializable):
    
    """Base class for statistical taggers"""

    def train(self,config):
        """Train the tagger model

        :param config: the overall tagger configuration
        :rtype: None 
        """
        raise NotImplementedError 

    def test(self,configr):
        """Test the tagger model 

        :param config: the overall tagger configuration
        """
        raise NotImplementedError
    

class SimpleTagger(TaggerBase):
    
    """Greedy tagger implementations"""

    def __init__(self,optimizer):
        """Creates a simple tagger instance 


        :param optimizer: the optimizer to use 
        """
        self.optimizer = optimizer

    def train(self,config):
        """Train the greedy tagger model

        :param config: the overall tagger configuration
        :rtype: None 
        """
        # dataset = 
        #self.optimizer.optimize()

    def test(self,config):
        """Test the tagger model 

        :param config: the overall tagger configuration
        """
        pass

    @classmethod
    def from_config(cls,config):
        """Setup a simple tagger from a configuration 

        :param config: the main configuration 
        """
        pass

class SequenceTagger(TaggerBase):
    pass


## factory method

TAGGERS = {
    "SimpleTagger" : SimpleTagger,
}


def Tagger(config):
    """Returns a tagger according to configuration 

    :param config: the tagger configuration 
    :raises: ValueError
    """
    ttype = config.ttype

    if ttype not in TAGGERS:
        raise ValueError('Unknown tagger type: %s' % ttype)
    return TAGGERS[ttype]

## MAIN EXECUTION ENTRY POINT

def run_tagger(config):
    """Main function for running a tagger pipeline

    :param config: the configuration
    """
    desired_action = config.action 

    ## train a tagger model
    if desired_action != 'train_tagger':

        ## find the type of tagger to use 
        tagger_class = Tagger(config)

        ## create a tagger instance 
        tagger = tagger_class.from_config(config)

    else:
        raise NotImplementedError('Tagger action not implemented! %s' % desired_action)

### SETTINGS


def params(config):
    """Loads dataset settings into a configuration

    :param config: the configuration
    :rtype: None  
    """
    group = OptionGroup(config,"tagger.Tagger","Tagger Settings")
    
    group.add_option(
        "--ttype",dest="ttype",default='SimpleTagger',
        help="The type of tagger to use [default='SimpleTagger']"
    )
    
    config.add_option_group(group)
