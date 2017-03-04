## put objects and functions related to datasets
import random
from optparse import OptionParser,OptionGroup
from BaseClass import TaggerSerializable

class DatasetBase(TaggerSerializable):

    """Dataset base class"""
    
    def __iter__(self):
        ## implement an iterator 
        raise NotImplementedError

    def __len__(self):
        ## return the size of dataset
        raise NotImplementedError

    def __getitem__(self,index):
        raise NotImplementedError 

class TextData(DatasetBase):

    """A class for representing text data

    >>> t = TextData(["first text","second text"],["label1","label2"]) 
    >>> t[0]
    ("first text","label1") 
    >>> t[1] 
    ("second text","label2") 
    >>> len(t) 
    2
    >>> for instance in t: print t
    ("first text","label1") 
    ("second text","label2") 

    """

    def __init__(self,text,labels,shuffle=False):
        """Creates a text data instance 

        :param text: the text part of the data 
        :param labels: the labels associated with text 
        :param shuffle: shuffle the dataset 
        """
        self.text = text
        self.labels = labels
        self._size = len(text)
        
    def __iter__(self):
        ## implements an iterator 
        random.seed(10)
        indices = range(self._size)
        if self.shuffle: random.shuffle(indices)
        for number in indices:
            yield (self.text[number],self.labels[number])

    def __len__(self):
        ## implements the len(self) method
        return self._size

    @property
    def size(self):
        """Returns the size of the dataset

        :rtype: int 
        """
        return self._size

    def __getitem__(self,index):
        ## implements self[index] 
        return (self.text[index],self.labels[index])

#### SETTINGS

def params(config):
    """Loads dataset settings into a configuration

    :param config: the configuration
    :rtype: None  
    """
    group = OptionGroup(config,"tagger.Dataset","Dataset settings")
    
    group.add_option(
        "--loc",dest="loc",default="",
        help="The location of data [default='']"
    )

    group.add_option(
        "--encoding",dest="encoding",default="utf-8",
        help="The main encoding [default='utf-8']'"
    )

    group.add_option(
        "--lower",dest="lower",default=True,
        help="Lowercase text when possible [default=True]'"
    )

    config.add_option_group(group)
