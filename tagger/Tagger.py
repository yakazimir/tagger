# -*- coding: utf-8 -*-

import sys
import os
import traceback
from optparse         import OptionParser,OptionGroup
from tagger.BaseClass import TaggerSerializable
from tagger.Dataset   import setup_dataset
from tagger.Optimizer        import setup_optimizer

class TaggerBase(TaggerSerializable):
    
    """Base class for statistical taggers"""

    def train(self,config):
        """Train the tagger model

        :param config: the overall tagger configuration
        :rtype: None 
        """
        raise NotImplementedError 

    def test(self,config):
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
        dataset = setup_dataset(config,'train')
        validation_data = setup_dataset(config,"valid")
        self.optimizer.optimize(dataset,validation_data)

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
        optimizer = setup_optimizer(config)
        return cls(optimizer)

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
    ttype = TAGGERS.get(config.ttype,None)

    if not ttype:
        raise ValueError('Unknown tagger type: %s' % ttype)
    return ttype

## MAIN EXECUTION ENTRY POINT

def run_tagger(config):
    """Main function for running a tagger pipeline

    :param config: the configuration
    """
    desired_action = config.action 

    ## train a tagger model

    try: 
        if desired_action == 'train_tagger':
            
            ## find the type of tagger to use 
            tagger_class = Tagger(config)

            ## create a tagger instance 
            tagger = tagger_class.from_config(config)
            ## train it
            tagger.train(config)

        elif desired_action == 'test_tagger':
            raise NotImplementedError('TESTER: Implement me!!')
    
        else:
            raise NotImplementedError('Tagger action not implemented! %s' % desired_action)


    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        try:
            if config.dir:
                tagger_loc = os.path.join(config.dir,"tagger.p")
                tagger.dump(tagger_loc)
        except:
            pass 
        
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

    group.add_option(
        "--evaluate_train",dest="evaluate_train",default=False,
        help="Test model on training data [default=False]"
    )

    group.add_option(
        "--evaluate_test",dest="evaluate_test",default=False,
        help="Test model on testing data [default=False]"
    )

    group.add_option(
        "--evaluate_valid",dest="evaluate_valid",default=False,
        help="Test model on validation data [default=False]"
    )

    config.add_option_group(group)
