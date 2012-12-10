'''
Created on Dec 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import logging, logging.config
log = logging.getLogger("rpfwd.prfwdinit.confSyslog.syslogOutput")
# log.debug('initing')

import sys, os, os.path 
from rpfwd.rpfwdinit.conf import ConfigBase

class SyslogOutput(ConfigBase):
    """ """
    def __init__(self, config, sectionTitle):
        """ """
        ConfigBase.__init__(self = self, config = config)
        
        assert 'SyslogLogging' in config
        assert sectionTitle in config['SyslogLogging']
        
        self.ourCfg = config['SyslogLogging'][sectionTitle]
        self.name = sectionTitle
        
    def getConfigLine(self):
        """ Generate our output line for our conf.d """
        # Desc comment
        comment = "# %s\n" % self.name
        if self.ourCfg['proto'] == 'TCP':
            return comment + "*.* @@%s:%s\n\n" % (
                                    self.ourCfg['target'],
                                    self.ourCfg['port'],
                                    )
        elif self.ourCfg['proto'] == 'UDP':
            return comment + "*.* @%s:%s\n\n" % (
                                   self.ourCfg['target'],
                                   self.ourCfg['port'],
                                   )
        else:
            raise ValueError, "Got an unknown protocol: %r" % self.ourCfg['proto']
        
                
class SyslogOutputs(object):
    """ All syslog based forwarding outputs """
    
    def __init__(self, config):
        """ """
        ConfigBase.__init__(self = self, config = config)

        assert 'SyslogLogging' in config

        self.rsyslogNeedsRestart = False
        self.outputs = {}
        
        for section in config['SyslogLogging'].sections:
            self.outputs[section] = SyslogOutput(
                                                 config = self.config,
                                                 sectionTitle = section,
                                                 )
        
    def createUpdateConfig(self):
        """ Create and/or update our conf.d file """
        log.debug("Going to update all syslog output configs")
        self.rsyslogNeedsRestart = True
        ret = """# Provides Syslog forwarding
# DO NOT EDIT BY HAND - MAINTAINED BY rpfwdInit.py

"""
        for name, section in self.outputs.keys():
            ret += section.getConfigLine()
                    
        with open('/etc/rsyslog.d/70-SyslogOutput.conf', 'w') as f:
            f.write(ret)
            
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
        
        
