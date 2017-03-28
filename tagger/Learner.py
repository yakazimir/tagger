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

    def update(self,features,prediction,gold):
        """Performs the perceptron update rule 

        :param features: the feature representation
        :param prediction: what the model currently thinks is correct
        :param gold: the actually correct answer
        :rtype: None
        """
        if prediction == gold:
            return

        ## if not, go through feature and subtract one from "bad" features
        totalfeatures = set()

        ## what are all the features for all labels?
        for fmap in features.values():
            for featureid in fmap.keys():
                totalfeatures.add(featureid)

        # now the update
        for feature_num in totalfeatures:
            self.weights[feature_num] +=\
                features[gold].get(feature_num,0.0) - features[prediction].get(feature_num,0.0)


    def score(self,features):
        """Score a set of candidates 

        :param features: the input features
        :returns: label name with highest score
        """
        label_scores = {label:0.0 for label in features.keys()}

        for (label,label_features) in features.iteritems():
            for (feature_id,feature_count) in label_features.iteritems():
                label_scores[label] += feature_count*self.weights[feature_id]

        return max(label_scores, key=label_scores.get)

    @classmethod
    def from_features(cls,feature_map):
        """Loads a model from an existing list of features

        :param feature_map: the feature list 
        :returns: a PerceptronInstance 
        """
        ## initialize all weights to zero
        weights = {i:0.0 for i in feature_map.values()}
        model = cls(weights)
        return model
    
### baseline learners

class MajorityLearner(LinearLearner):
    """A majority learner class"""

    def __init__(self,weights):
        self.weights = {} ## we dont need this, but for design purposes well keep it
        self.labels_seen = {}

    def update(self,features,prediction,gold):
        """Perform online update during training 

        :param features: the target features
        :param prediction: what the system thinks
        :param gold: the actual real world value
        """
        if gold not in self.labels_seen:
            self.labels_seen[gold] = 0.0
        self.labels_seen[gold] += 1.0

    def score(self,features):
        """Score an input feature representation 

        :param features: the features to score 
        """
        if not self.labels_seen:
            return False
        return max(self.labels_seen, key=self.labels_seen.get)


    @classmethod
    def from_features(cls,feature_map):
        """Loads a model from an existing list of features

        :param feature_map: the feature list
        :returns: a PerceptronInstance
        """
        ## initialize all weights to zero
        weights = {}
        model = cls(weights)
        return model


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
    "perceptron" : PerceptronLearner,
    "majority"   : MajorityLearner,
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

def setup_learner(config,features):
    """Returns a learner instance from config
    
    :param config: the main configuration 
    :param features: the map of features
    :raises: ValueError
    """
    ltype = Learner(config.learner)
    return ltype.from_features(features)
    
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
