'''
Created on Dec 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import logging, logging.config
log = logging.getLogger("rpfwd.prfwdinit.confGPG")
# log.debug('initing')

import sys, os, os.path 
from rpfwd.rpfwdinit.conf import ConfigBase

class ConfGPG(ConfigBase):
    """ Enable forwarding of log files """
    
    def __init__(self, config):
        ConfigBase.__init__(self = self, config = config)
        
        assert 'GPG' in config

        self.ourCfg = config['GPG']
    
#    def createUpdateConfig(self):
#        """ Create and/or update our conf.d file """
#     
#    def restartIfNeeded(self):
#        """ Restart our daemon, if it's required. """

