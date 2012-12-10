'''
Created on Dec 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import logging, logging.config
log = logging.getLogger("rpfwd.prfwdinit.confSyslog.syslogInput")
# log.debug('initing')

import sys, os, os.path 
from rpfwd.rpfwdinit.conf import ConfigBase

class SyslogInput(ConfigBase):
    """ Use self.rsyslogNeedsRestart to determine if we need
    to restart the rsyslog daemon or not.
    """
    
    def restartIfNeeded(self):
        """ Restart our daemon, if it's required. 
        TODO: If it's not already running, do nothing. 
        """
        if self.rsyslogNeedsRestart:
            log.debug("Going to restart rsyslogd")
            rc = os.system("/usr/bin/service rsyslog restart")
            if rc != 0:
                os.error("Failed to restart the rsyslog daemon. Got a return code of %r", rc)
        else:
            log.debug("Not going to restart rsyslogd")
