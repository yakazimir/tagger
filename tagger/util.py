import os
import sys
import codecs

## put all utility functions here

__all__ = [
    "build_text_data",    
]

def __find_path(ddir,dtype):
    """Return the data path

    :param ddir: the data directory
    :param dtype: the type of data
    :raises: ValueError
    """
    path = os.path.join(ddir,dtype+".txt")
    if not path:
        raise ValueError('Cannot find data!')
    return path

def build_text_data(config,dtype):
    """Builds the text data 


    :param config: the main configuration 
    :param dtype: the type of data 
    :rtype: tuple 
    :returns: a tuple of a text list and label list
    """
    path = __find_path(config.loc,dtype)
    encoding = 'utf-8' if not config.encoding else config.encoding
    text = []; labels = [] 

    with codecs.open(path,encoding=encoding) as my_data:
        for line in my_data:
            line = line.strip()
            name,label = line.split('\t')
            text.append(name.strip())
            labels.append(label)

    return (text,labels)



if __name__ == "__main__":
    pass
