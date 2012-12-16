'''
Created on Dec 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import logging, logging.config
log = logging.getLogger("rpfwd.prfwdinit.confNetwork")
# log.debug('initing')

import sys, os, os.path 
from rpfwd.rpfwdinit.conf import ConfigBase

class ConfNetworking(ConfigBase):
    """ """
    
    def __init__(self, config):
        ConfigBase.__init__(self = self, config = config)
        
        assert 'Networking' in config

        self.ourCfg = config['Networking']
    
    def createUpdateConfig(self):
        """ Create and/or update our conf.d file """
        log.debug("Setting hostname to %r", self.ourCfg['hostname'])
        
        cfg = self.ourCfg['hostname']
        
        with open('/etc/hostname', 'w') as f:
            f.write(cfg)
        
        log.debug("Setting live hostname")
        # FIXME: Switch this to a way without a shell injection vuln
        rc = os.system("/bin/hostname '%s'" % self.ourCfg['hostname'])
        if rc != 0:
            log.error("Failed to set hostname to %r. Got $r. ", self.ourCfg['hostname'], rc)
                    
    def restartIfNeeded(self):
        """ Restart our daemon, if it's required. 
        TODO: If it's not already running, do nothing. 
        """
        log.debug("Nothing required for restartIfNeeded")
