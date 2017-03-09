# -*- coding: utf-8 -*-

import random
from optparse import OptionParser,OptionGroup
from BaseClass import TaggerSerializable
from tagger.util import *

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
    >>> nt = TextData([],["label1"])
    TaggerError
    Traceback (most recent call last)
    ...
    TaggerError: TAGGER RUNTIME ERROR: Mismatched text/label data!

    """

    def __init__(self,text,labels,shuffle=False):
        """Creates a text data instance 

        :param text: the text part of the data 
        :param labels: the labels associated with text 
        :param shuffle: shuffle the dataset 
        """
        self.text    = text
        self.labels  = labels
        self.shuffle = shuffle
        self._size   = len(text)

        ## check that datasets are the same size
        if len(text) != len(labels):
            raise TextData.TaggerError('Mismatched text/label data!',self.logger)
        
    def __iter__(self):
        ## implements an iterator

        ## set a seed for randomization so you can reproduce the shuffle
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

    @classmethod
    def from_config(cls,config,dtype='train'):
        """Build data from a configuration and text file. 
        
        -- the config.loc should give a pointer to 
        where the data is.

        Below is an example invocation: 

        >>> from tagger.Dataset import TextData
        >>> from tagger import default_config as config 
        >>> config.loc = 'data/names/ru'
        >>> tagger = TextData.from_config(config,'train') 
        >>> tagger.size 
        225
        >>> d[0]
        (u'\u041f\u0440\u043e\u043a\u043e\u043f\u0438\u0439', u'MALE')
        >>> print d[0][0]
        Прокопий

        :param config: the main configuration 
        :param dtype: the type of data to load (e.g., train/test/..)
        :returns: A TextData instance
        """
        text,labels = build_text_data(config,dtype)
        return cls(text,labels,config.shuffle)

    def __getitem__(self,index):
        ## implements self[index] 
        return (self.text[index],self.labels[index])

DATA = {
    "textdata" : TextData,
}
    
def Dataset(dctype):
    """Factor method for selecting dataset class
    
    :param dtype: the type of dataset class needed
    """
    ctype = DATA.get(dctype,None)
    if not ctype:
        raise ValueError('Unknown type of data: %s' % ctype)
    return ctype

def setup_dataset(config,dtype):
    """Returns a loaded dataset according to config and data type

    :param config: the main configuration 
    :param dtype: the type of data 
    """
    ctype = Dataset(config.dclass)
    return ctype.from_config(config,dtype)
        
    
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

    group.add_option(
        "--shuffle",dest="shuffle",default=False,
        help="Shuffle dataset when iterating [default=False]"
    )

    group.add_option(
        "--dclass",dest="dclass",default='textdata',
        help="The type of data [default=False]"
    )
    
    config.add_option_group(group)
