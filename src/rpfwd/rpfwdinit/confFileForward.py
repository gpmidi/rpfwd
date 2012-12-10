'''
Created on Dec 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import logging, logging.config
log = logging.getLogger("rpfwd.prfwdinit.confFileForward")
# log.debug('initing')

import sys, os, os.path 
from rpfwd.rpfwdinit.conf import ConfigBase

class ConfFileForward(ConfigBase):
    """ Enable forwarding of log files """
    
    def __init__(self, config):
        ConfigBase.__init__(self = self, config = config)
        
        assert 'FileForward' in config

        self.ourCfg = config['FileForward']
        self.fwds = {}
        
        for forwarder in self.ourCfg.sections:
            self.fwds[forwarder] = FileForward(
                                               config = config,
                                               sectionTitle = forwarder,
                                               )
    
    def createUpdateConfig(self):
        """ Create and/or update our conf.d file """
        raise NotImplementedError
     
    def restartIfNeeded(self):
        """ Restart our daemon, if it's required. """
        raise NotImplementedError


class FileForward(ConfigBase):
    """ Enable forwarding of log files to a given target """
    
    def __init__(self, config, sectionTitle):
        ConfigBase.__init__(self = self, config = config)
        
        assert sectionTitle in self.config['FileForward']
        
        self.ourCfg = self.config['FileForward'][sectionTitle]
        self.name = sectionTitle
        
    def createUpdateConfig(self):
        """ Create and/or update our conf.d file """
        raise NotImplementedError
     
    def restartIfNeeded(self):
        """ Restart our daemon, if it's required. """
        raise NotImplementedError        
