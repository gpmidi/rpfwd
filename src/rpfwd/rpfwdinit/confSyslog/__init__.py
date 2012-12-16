''' Rsyslog config file generation tools
Created on Dec 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import logging, logging.config
log = logging.getLogger("rpfwd.prfwdinit.confSyslog.__init__")
# log.debug('initing')

from rpfwd.rpfwdinit.conf import ConfigBase

# Don't import SyslogInput - It's a helper only
from tcpInput import SyslogTCPInput
from udpInput import SyslogUDPInput

from syslogOutput import SyslogOutputs

class ConfSyslog(ConfigBase):
    """ """
    
    def __init__(self, config):
        ConfigBase.__init__(self = self, config = config)
        self.confs = [
                    SyslogOutputs(config = config,),
                    SyslogTCPInput(config = config,),
                    SyslogUDPInput(config = config,),
                    ]
    
    def createUpdateConfig(self):
        """ Create and/or update our conf.d file """
        log.debug("Going to update all syslog confs")
        for cfg in self.confs:
            cfg.createUpdateConfig()
        log.debug("Done updating confs")
                    
    def restartIfNeeded(self):
        """ Restart our daemon, if it's required. 
        TODO: If it's not already running, do nothing. 
        """
        log.debug("Going to restart all syslog confs, if needed")
        for cfg in self.confs:
            cfg.createUpdateConfig()
        log.debug("Done restarting syslog for all confs")
        
