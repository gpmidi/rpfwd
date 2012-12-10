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
    
#    def createUpdateConfig(self):
#        """ Create and/or update our conf.d file """
#     
#    def restartIfNeeded(self):
#        """ Restart our daemon, if it's required. """

