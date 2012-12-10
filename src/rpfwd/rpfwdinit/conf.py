'''
Created on Dec 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import logging, logging.config
log = logging.getLogger("rpfwd.prfwdinit.conf")
# log.debug('initing')

import sys, os, os.path 

class ConfigBase(object):
    def __init__(self, config):
        self.config = config
    
    def createUpdateConfig(self):
        """ Create and/or update our conf.d file """
        raise NotImplementedError, "Need to define createUpdateConfig"
    
    def restartIfNeeded(self):
        """ Restart our daemon, if it's required. 
        TODO: If it's not already running, do nothing. 
        """
        raise NotImplementedError, "Need to define restartIfNeeded"
    
    
