''' Generate the rsyslog conf.d file for TCP-based reception. 
Created on Dec 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import logging, logging.config
log = logging.getLogger("rpfwd.prfwdinit.confSyslog.tcpInput")
# log.debug('initing')

from syslogInput import SyslogInput
        
class SyslogTCPInput(SyslogInput):
    """  
    """
    
    def __init__(self, config):
        """ """
        assert 'SyslogLogging' in config
        assert 'SyslogTCPInput' in config['SyslogLogging']
        self.config = config
        self.ourCfg = config['SyslogLogging']['SyslogTCPInput']
        self.rsyslogNeedsRestart = False
        
    def createUpdateConfig(self):
        """ Create and/or update our conf.d file """
        self.rsyslogNeedsRestart = True
        
        if self.ourCfg['enabled']:
            cfg = """# Provides TCP syslog reception
# DO NOT EDIT BY HAND - MAINTAINED BY rpfwdInit.py
$ModLoad imtcp.so
$InputTCPServerBindRuleset %(ruleset)s
$InputTCPServerRun %(port)s
            """ % self.ourCfg
        else:
            cfg = """# Provides TCP syslog reception
# DO NOT EDIT BY HAND - MAINTAINED BY rpfwdInit.py
# Disabled
#$ModLoad imtcp.so
#$InputTCPServerBindRuleset %(ruleset)s
#$InputTCPServerRun %(port)s
            """ % self.ourCfg
        
        with open('/etc/rsyslog.d/70-SyslogTCPInput.conf', 'w') as f:
            f.write(cfg)
        
    
        
