import time
from copy import deepcopy
from optparse import OptionParser,OptionGroup
from tagger.BaseClass import TaggerSerializable
from tagger.Learner   import setup_learner
from tagger.Feature   import setup_extractor
from tagger.Dataset   import setup_dataset
from tagger.util import *


class OptimizerBase(TaggerSerializable):
    """Base class for optimization procedure"""
    
    def optimize(self,dataset):
        """Main method for optimizing or fitting model

        :param dataset: the data used to fit the data
        :type dataset: subclass of DatasetBase
        """
        raise NotImplementedError

    def test(self,dataset):
        """Test the model of some data

        :param dataset: the dataset to test the model on 
        :type dataset: subclass of DatasetBase 
        """
        raise NotImplementedError

class OnlineOptimizer(OptimizerBase):
    """Online optimization procedure"""

    def __init__(self,model,extractor,iterations=10):
        """Initializes an online optimizer 

        :param model: a model to use 
        :type model: subclass of LearnerBase
        :param extractor: the feature extractor 
        """
        self.model = model
        self.extractor = extractor
        self.iterations = iterations

    def optimize(self,dataset,validation=None,wdir=None):

        """Main method for optimizing or fitting model using online updates 

        -- ``Online`` here means that the updates to the model are made
        per example. 

        :param dataset: the data used to fit the data
        :type dataset: subclass of DatasetBase
        :param validation: a validation dataset 
        :type validation: None or subclass of DatasetBase
        """
        last_update = 0
        last_iteration = None
        last_accuracy = 0.
        best_model = None

        ## start a new iteration 
        for epoch in range(self.iterations):
            
            ## start a counter 
            start_time = time.time()

            ## go through your data 
            for data_instance in dataset:
                raw,gold = data_instance

                ## input -> (Male, {features}), (Female,{features})
                features = self.extractor.extract(data_instance)

                ## features -> scores
                prediction = self.model.score(features)

                ## make the update based on prediction and correct answer
                self.model.update(features,prediction,gold)

            ## log iteration information 
            self.logger.info('Finished iteration %d in %s seconds' %\
                                 (epoch,time.time()-start_time))

            self.model.after_iteration()

            ## end of the iteration j
            if validation:
                dev_average = self.test(validation)
                self.logger.info('Accuracy of development set after %d iterations: %f' % (epoch,dev_average))

                if dev_average > last_accuracy:
                    last_update = epoch
                    last_accuracy = dev_average

                    best_model = deepcopy(self.model.weights)
                elif (epoch - last_update) >= 10:
                    last_iteration = epoch
                    self.logger.info('Stopped early: current=%f, last prev. best=%f' % (dev_average,last_accuracy))
                    break

        ## test of the training data
        ##########



        if best_model:
            self.model.weights = best_model
        if not last_iteration: last_iteration = epoch


        self.model.after_experiment()
        average = self.test(dataset)
        self.logger.info('Accuracy on training: %f' % average)

        #test model again on validation with averaged vector
        new_validation_average = self.test(validation)
        self.logger.info('Final accuracy on validation: %f' % new_validation_average)

        if wdir:
            print_train_info(average,last_accuracy,wdir,last_iteration,new_validation_average)

    def test_dataset(self,dataset):
        pass

    def test(self,dataset):
        """Test the model of some data

        :param dataset: the dataset to test the model on 
        :type dataset: subclass of DatasetBase 
        """

        correct = 0.0
        incorrect = 0.0
        for data_instance in dataset:
            raw, gold = data_instance
            features = self.extractor.extract(data_instance)
            prediction = self.model.score(features)

            if prediction == gold:
                correct += 1.0

            else:
                incorrect += 1.0

        return correct / (correct + incorrect)


    @classmethod
    def from_config(cls,config):
        """Setup an online optimizer instance 

        :param config: the main configuration 
        """
        train = setup_dataset(config,'train')
        extractor = setup_extractor(config,train)
        learner = setup_learner(config,extractor.feature_map)

        return cls(learner,extractor,config.iters)

class BatchOptimizer(OptimizerBase):
    """Class for batch training"""
    pass

### Factory method
    
OPTIMIZERS = {
    "online" : OnlineOptimizer,
}

def Optimizer(otype):
    """Factory method for creating optimizer instance 

    :param otype: the optimizer type 
    :raises: ValueError 
    """
    if otype not in OPTIMIZERS:
        raise ValueError('Unknown optimizer type: %s' % otype)
    return OPTIMIZERS[otype]

def setup_optimizer(config):
    """Setups up an optimizer from configuration

    :param config: the main configuration
    """
    optimizer_class = Optimizer(config.optimizer)

    ## setup the optimizer given settings 
    optimizer = optimizer_class.from_config(config)
    return optimizer
    

#### SETTINGS

def params(config):
    """Loads dataset settings into a configuration

    :param config: the configuration
    :rtype: None  
    """
    group = OptionGroup(config,"tagger.Optimizer","Optimization settings")
    
    group.add_option(
        "--iters",dest="iters",default=10,type=int,
        help="The number of iterations [default='10']"
    )

    group.add_option(
    "--optimizer",dest="optimizer",default="online",
    help="The type of optimization to use [default='online']'"
    )

    group.add_option(
    "--learn_rate",dest="learn_rate",default=0.01,
    help="The learning rate [default=0.01]'"
    )
    
    config.add_option_group(group)

