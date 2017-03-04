from optparse import OptionParser,OptionGroup
from BaseClass import TaggerSerializable


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

    def __init__(self,model):
        """Initializes an online optimizer 

        :param model: a model to use 
        :type model: subclass of LearnerBase
        """
        self.model = model

    def optimize(self,dataset):
        """Main method for optimizing or fitting model using online updates 

        -- ``Online`` here means that the updates to the model are made
        per example. 

        :param dataset: the data used to fit the data
        :type dataset: subclass of DatasetBase
        """        
        pass

    def test(self,dataset):
        """Test the model of some data

        :param dataset: the dataset to test the model on 
        :type dataset: subclass of DatasetBase 
        """
        raise NotImplementedError

### Factory method 
    
OPTIMIZERS = {
    "online" : OnlineOptimizer,
}

def Optimizer(otype):
    """Factory method for creating optimizer instance 

    :param otype: the optimizer type 
    """
    pass


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

    config.add_option_group(group)
