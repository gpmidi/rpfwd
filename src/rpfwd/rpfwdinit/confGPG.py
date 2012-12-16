'''
Created on Dec 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import logging, logging.config
log = logging.getLogger("rpfwd.prfwdinit.confGPG")
# log.debug('initing')

import sys, os, os.path 
from rpfwd.rpfwdinit.conf import ConfigBase
import socket
import stat
import subprocess
import re 
import gnupg

class ConfGPG(ConfigBase):
    """ Enable forwarding of log files """
    
    def __init__(self, config):
        ConfigBase.__init__(self = self, config = config)
        # TODO: Make sure a user can't trigger this
        assert 'GPG' in config

        self.ourCfg = config['GPG']
    
    def createUpdateConfig(self):
        """ Create and/or update our conf.d file """
        log.debug("Updating config for %r", self)
        assert 'keydir' in self.ourCfg
        
        if not os.path.exists(self.ourCfg['keydir']):
            log.debug("Key directory %r doesn't exist. Creating it. ", self.ourCfg['keydir'])
            os.mkdir(self.ourCfg['keydir'])
            os.chmod(
                     self.ourCfg['keydir'],
                     # 0700
                     stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR,
                     )
        
        assert os.access(self.ourCfg['keydir'], os.R_OK | os.W_OK | os.X_OK)
        
        if os.path.exists(self.getPrivateKeyLoc()) and os.path.exists(self.getPublicKeyLoc()):
            log.debug("Private and public key locations exists.")            
        else:
            log.debug("No existing key. Creating a new one. ")
            self.genKey()
        
        
    def genKey(self):
        gpgBatchContents = """%echo Generating a key for rpfwd
Key-Type: %(keytype)s
Key-Length: %(keysize)d
Name-Real: RPi Forwarder
Name-Comment: Log Forwarder Key
Name-Email: root@%(hostname)s
Expire-Date: 0
Passphrase: %(keypasswd)s
%pubring %(pubkeyloc)s
%secring %(privkeyloc)s
%commit
%echo Completed
          """ % dict(# Could use configobj directly - Not doing so to make config more transparent
                   keysize = self.ourCfg['keysize'],
                   keytype = self.ourCfg['keytype'],
                   keypasswd = self.ourCfg['keypasswd'],
                   hostname = socket.getfqdn,
                   privkeyloc = self.getPrivateKeyLoc(),
                   pubkeyloc = self.getPublicKeyLoc(),
                   )
        # Needed to avoid gpg asking any questions
        log.debug("Writing out gpg config")
        with open(self.getNewKeyConfigLoc(), 'w') as f:
            f.write(gpgBatchContents)
            
        try:
            cmdWithArgs = [
                           '/usr/bin/gpg',
                           '--batch',
                           '--gen-key',
                           self.getNewKeyConfigLoc(),
                           ]
            results = self.runCmd(cmdWithArgs, cwd = '/tmp/')
            found = re.findall(r'^\sCompleted\s*$*', results, re.DOTALL | re.MULTILINE)
            if len(found) != 1:
                log.error("Failed to create a new key. Got output %r. ", results)
                raise RuntimeError("Failed to create a new key. Got output %r. " % results)
            
        finally:
            os.remove(self.getNewKeyConfigLoc())
        
    def runCmd(self, cmdWithArgs, cwd = '/tmp/'):
        p = subprocess.Popen(
                             cmdWithArgs,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.STDOUT,
                             cwd = cwd,
                             )
        log.debug("Started command (PID: %d)(Cmd/Args: %r)(CWD: %r)", p.pid, cmdWithArgs, cwd)
        while(True):
            ret = p.poll()  # returns None while subprocess is running
            line = p.stdout.readline()
            log.debug("Read line: %r", line)
            yield line
            if(ret is not None):
                break
        try:
            remain = p.stdout.read()
            log.debug("Read remaining: %r", line)
            yield remain
        except:
            pass
        log.debug("Command ended with a return code of %d", ret)
        if ret != 0:
            raise RuntimeError("Command failed with a return code of %r. Cmd: %r" % (ret, cmdWithArgs))
    
    def getNewKeyConfigLoc(self):
        return os.path.join(self.ourCfg['keydir'], 'main.gen.cfg')
          
    def getPrivateKeyLoc(self):
        return os.path.join(self.ourCfg['keydir'], 'main.priv')
    
    def getPublicKeyLoc(self):
        return os.path.join(self.ourCfg['keydir'], 'main.pub')
     
    def restartIfNeeded(self):
        """ Restart our daemon, if it's required. """
        log.debug("No restarted required for %r", self)
