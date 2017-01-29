## put all functions here related to learning

__all__ = ["PerceptronLearner"]


class LearnerBase(object):
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

class PerceptronLearner(LinearLearner):
    """Implementation of the perceptron learner"""

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

### Factory method

LEARNERS = {
    "perceptron" : PerceptronLearner
}

def Learner(ltype):
    """Factory method for giving back a learner 

    :param ltype: the type of learner desired 
    """
    pass
