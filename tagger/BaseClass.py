import logging 
import gzip
import pickle
import traceback

class TaggerBase(object):

    """Tagger base class"""
    
    class TaggerError(Exception):
        """An exception class for TaggerClass runtime errors"""

        def __init__(self,msg,error,logger=None):
            """

            :param msg: the error message 
            :param error: the raises error 
            :param logger: an optional instance logger
            """
            pass

    @classmethod
    def from_config(cls,config):
        """Load a class instance from configuration 

        :param config: the tagger configuration object 
        :returns: TaggerClass instance 
        """
        raise NotImplementedError('Configuration setup not implemented!')


class TaggerLoggable(TaggerBase):
    
    """A tagger class that has a logger instance"""
    
    @property
    def logger(self):
        """A logger for tagger class instance 

        :returns: logger instance 
        """
        level = '.'.join([__name__,type(self).__name__])
        return logging.getLogger(level)

class TaggerSerializable(TaggerLoggable):
    
    """A tagger class that allows for serialization via pickle"""

    @classmethod
    def load(cls,path):
        """Load a pickled instance of class

        :param path: the path to the pickled class 
        :type path: basestring 
        :returns: a class instance 
        """
        out_path = path if ".gz" in path else path+".gz"
        
        with gzip.open(out_path,'rb') as my_instance:
            return pickle.load(my_instance)

    def dump(self,path):
        """Make a pickled backup of the class instance 

        :param path: the path to put pickled item 
        :rtype: None 
        """
        self.logger.info('Pickling the instance...')
        out_path = path if ".gz" in path else path+".gz"

        with gzip.open(out_path,'wb') as my_pickle:
            pickle.dump(self,out_path)
