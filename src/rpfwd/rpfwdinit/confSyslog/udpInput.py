'''
Created on Dec 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import logging, logging.config
log = logging.getLogger("rpfwd.prfwdinit.confSyslog.udpInput")
# log.debug('initing')

from syslogInput import SyslogInput

class SyslogUDPInput(SyslogInput):
    """ """
    
    def __init__(self, config):
        """ """
        SyslogInput.__init__(self = self, config = config)
        
        assert 'SyslogLogging' in config
        assert 'SyslogUDPInput' in config['SyslogLogging']

        self.ourCfg = config['SyslogLogging']['SyslogUDPInput']
        self.rsyslogNeedsRestart = False
        
    def createUpdateConfig(self):
        """ Create and/or update our conf.d file """
        self.rsyslogNeedsRestart = True
        
        if self.ourCfg['enabled']:
            cfg = """# Provides UDP syslog reception
# DO NOT EDIT BY HAND - MAINTAINED BY rpfwdInit.py
$ModLoad imudp.so
$InputUDPServerBindRuleset %(ruleset)s
$InputUDPServerRun %(port)s
            """ % self.ourCfg
        else:
            cfg = """# Provides UDP syslog reception
# DO NOT EDIT BY HAND - MAINTAINED BY rpfwdInit.py
# Disabled
#$ModLoad imudp.so
#$InputUDPServerBindRuleset %(ruleset)s
#$InputUDPServerRun %(port)s
            """ % self.ourCfg
        
        with open('/etc/rsyslog.d/20-SyslogUDPInput.conf', 'w') as f:
            f.write(cfg)
        
        
        
