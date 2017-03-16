# -*- coding: utf-8 -*-

import sys
from BaseClass import TaggerSerializable
from optparse import OptionParser,OptionGroup

__all__ = ["PerceptronLearner"]

class LearnerBase(TaggerSerializable):
    """Base class for learners"""
    pass

### LINEAR MODELS

class LinearLearner(LearnerBase):
    """Linear linear implementation"""

    def update(self,features):
        """Perform online update during training 

        :param features: the target features 
        """
        raise NotImplementedError

    def score(self,features):
        """Score an input feature representation 

        :param features 
        """
        raise NotImplementedError

    @classmethod
    def from_features(cls,feature_map):
        """Loads a model from an existing list of features

        :param feature_map: the feature list 
        :returns: a PerceptronInstance 
        """
        raise NotImplementedError 
        
    @classmethod
    def from_config(cls,config):
        """Load a learning model from configuration

        :param config: the configuration
        :returns: a PerceptronLearner instance
        """
        raise ValueError('Use from_features, config init not supported')


class PerceptronLearner(LinearLearner):
    
    """Implementation of the perceptron learner"""

    def __init__(self,weights):
        """Create a perceptron learner instance 

        :param weights: weights associated with features
        """
        self.weights     = weights

    def update(self,features):
        """Performs the perceptron update rule 

        :param features: the feature representation
        :rtype: None 
        """
        raise NotImplementedError

    def score(self,features):
        """Score a set of candidates 

        :param features: the input features 
        """
        pass

    @classmethod
    def from_features(cls,feature_map):
        """Loads a model from an existing list of features

        :param feature_map: the feature list 
        :returns: a PerceptronInstance 
        """
        ## initialize all weights to zero
        weights = {i:0.0 for i in feature_map.values()}
        return cls(weights)
    
### baseline learners

class MajorityLearner(LinearLearner):
    """A majority learner class"""

    def update(self,features):
        """Perform online update during training 

        :param features: the target features 
        """
        raise NotImplementedError

    def score(self,features):
        """Score an input feature representation 

        :param features: the features to score 
        """
        raise NotImplementedError

class HeuristicLearner(LinearLearner):
    """A Learner that uses a single or few heuristic to learn"""

    def update(self,features):
        """Perform online update during training 

        :param features: the target features 
        """
        raise NotImplementedError

    def score(self,features):
        """Score an input feature representation 

        :param features 
        """
        raise NotImplementedError

### Factory method

LEARNERS = {
    "perceptron" : PerceptronLearner
}

def Learner(ltype):
    """Factory method for giving back a learner 

    :param ltype: the type of learner desired 
    :raises: ValueError
    """
    lclass = LEARNERS.get(ltype,None)
    if not lclass:
        raise ValueError('Learner type not known: %s' % lclass)
    return lclass

def setup_learner(config):
    """Returns a learner instance from config
    
    :param config: the main configuration 
    :raises: ValueError
    """
    ltype = Learner(config.learner)
    return ltype.from_config(config)
    
    
## SETTINGS

def params(config):
    """Loads dataset settings into a configuration

    :param config: the configuration
    :rtype: None  
    """
    group = OptionGroup(config,"tagger.Learner","Learner and Model settings")
    
    group.add_option(
        "--learner",dest="learner",default="perceptron",
        help="The type of learner [default='perceptron']"
    )

    config.add_option_group(group)
