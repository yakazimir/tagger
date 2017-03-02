import logging 
import gzip 
import traceback

class TaggerClass(object):

    class TaggerError(Exception):
        """An exception class for TaggerClass runtime errors"""

        def __init__(self,msg,error,logger=None):
            """

            :param msg: the error message 
            :param error: the raises error 
            :param logger: 
            """
            pass

    @classmethod
    def from_config(cls,config):
        """Load a class instance from configuration 

        :param config: the tagger configuration object 
        :returns: TaggerClass instance 
        """
        raise NotImplementedError

    @classmethod
    def load(cls,path):
        """Load a pickled instance of class

        :param path: the path to the pickled class 
        :type path: basestring 
        :returns: a class instance 
        """
        pass

    def dump(self):
        """Make a pickled backup of the class instance 
        
        :rtype: None 
        """
        pass
    
    @property
    def logger(self):
        """A logger for tagger class instance 

        :returns: logger instance 
        """
        pass
