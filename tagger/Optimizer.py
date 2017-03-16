import time
from optparse import OptionParser,OptionGroup
from BaseClass import TaggerSerializable
from Learner   import setup_learner

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

    def optimize(self,dataset,validation=None):
        """Main method for optimizing or fitting model using online updates 

        -- ``Online`` here means that the updates to the model are made
        per example. 

        :param dataset: the data used to fit the data
        :type dataset: subclass of DatasetBase
        :param validation: a validation dataset 
        :type validation: None or subclass of DatasetBase
        """
        ## start a new iteration 
        for epoch in self.iterations:
            
            ## start a counter 
            start_time = time.time()

            ## go through your data 
            for data_instance in dataset:
                
                self.logger.warning('Online learning loop not implemented, doing nothing!')
                #features = self.extractor.extract(data_instance)
                #self.model.update(features)

            ## log iteration information 
            self.logger.info('Finished iteration %d in %s seconds' %\
                                 (epoch,time.time()-start_time))

    def test(self,dataset):
        """Test the model of some data

        :param dataset: the dataset to test the model on 
        :type dataset: subclass of DatasetBase 
        """
        raise NotImplementedError('Optimizer test not implemented yet!')

    @classmethod
    def from_config(cls,config):
        """Setup an online optimizer instance 

        :param config: the main configuration 
        """
        learner = setup_learner(config)
        

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
        "--iters",dest="iters",default=10,
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

