''' Rsyslog config file generation tools
Created on Dec 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import logging, logging.config
log = logging.getLogger("rpfwd.prfwdinit.confSyslog.__init__")
# log.debug('initing')

from tcpInput import SyslogTCPInput
from udpInput import SyslogUDPInput

from syslogOutput import SyslogOutput
