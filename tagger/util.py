import os
import sys
import codecs
import logging
import subprocess
from shutil import rmtree

## put all utility functions here

__all__ = [
    "build_text_data",
    "create_wdir",
    "create_run_script",
    "print_train_info",
]

util_logger = logging.getLogger("tagger.util")
    
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
        for k,line in enumerate(my_data):
            line = line.strip()

            try: 
                name,label = line.split('\t')
                text.append(name.strip())
                labels.append(label)
            except:
                raise ValueError('Encountered error at line %d: %s' % (k,line))

    return (text,labels)

def create_wdir(config):
    """Create a working directory

    :param config: the main configuration 
    """
    path = config.dir

    if not path:
        raise ValueError('Must specify a working path!')
        
    if os.path.isdir(path) and not config.override:
        raise ValueError(
            'directory already exists, use --override option: %s'
            % path)
    elif os.path.isdir(path): 
        rmtree(path)
    os.makedirs(path)

def create_run_script(argv,config):
    """Generate a run script for repeating experiment 
    
    :param argv: the cli input 
    :param config: the main configuration
    :rtype: None 
    """
    from tagger import lib_loc

    run_path = os.path.join(config.dir,"run.sh")
    with open(run_path,'w') as run_script:
        print >>run_script, "cd %s\n./run.sh %s --override=true" % (lib_loc,' '.join(argv))

    ## give permissions to run script
    subprocess.call(['chmod', '755', run_path])


def print_train_info(train_accuracy,dev_accuracy,wdir,last):
    """Print information about the training after it is done


    :param train_accuracy: how well did the model do on training data
    :param dev_accuracy: how well on development set
    :param wdir: the experiment directory path
    :param last: the last number of iterations made before end or stopping
    """
    info_file_path = os.path.join(wdir,"train_info.txt")

    with open(info_file_path,'w') as info:
        print >>info, "NUMBER OF ITERATIONS: %d" % last
        print >>info, "ACCURACY ON TRAIN SET: %f" % train_accuracy
        print >>info, "ACCURACY ON DEV: %f" % dev_accuracy



if __name__ == "__main__":
    pass
