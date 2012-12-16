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

class MissingKeyError(ValueError):
    """ A key is missing """
    
class MissingPrivateKey(MissingKeyError):
    """ Missing a private key """
    
class MissingPublicKey(MissingKeyError):
    """ Missing a public key """

class ConfGPG(ConfigBase):
    """ Enable forwarding of log files """
    
    def __init__(self, config):
        ConfigBase.__init__(self = self, config = config)
        # TODO: Make sure a user can't trigger this
        assert 'GPG' in config
        
        self.gpg = None
        self.keyPriv = None
        self.keyPub = None

        self.ourCfg = config['GPG']
        self.updateCfgWithDefaults()  
        
    def updateCfgWithDefaults(self):
        """ Make sure the config file has all of our options. If any are 
        missing, set to default and save. 
        """
        write = False
        if not 'keydir' in self.ourCfg:
            self.ourCfg['keydir'] = '/var/lib/rpfwd/'
            write = True       
        if not 'keysize' in self.ourCfg:
            self.ourCfg['keysize'] = 4096
            write = True       
        if not 'keytype' in self.ourCfg:
            self.ourCfg['keytype'] = 'RSA'
            write = True       
        if not 'keypasswd' in self.ourCfg:
            self.ourCfg['keypasswd'] = self.getRandomPW(length = 32)
            write = True
        if not 'keyid' in self.ourCfg:
            self.ourCfg['keyid'] = None
            write = True
        if not 'sendpubkey' in self.ourCfg:
            self.ourCfg['sendpubkey'] = None
            write = True
        if write:
            log.debug("Going to save config file as changes were made - Added missing fields. ")
            self.config.write()
               
    def getGPG(self):
        """ Returns a gnupg.GPG object that is ready for use. """
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
        
        if self.gpg:
            return self.gpg
        self.gpg = gnupg.GPG(gnupghome = self.ourCfg['keydir'])
        log.debug("Created new GPG object: %r", self.gpg)
        
    def createUpdateConfig(self):
        """ Create and/or update our config file(s).
        In reality, we're making sure we have a GPG key that we can use.
        """
        log.debug("Updating config for %r", self)
        
        # Create a key if needed; fetch it otherwise
        pub, priv = self.getKey()
            
    def _findKey(self, keyid):
        """ Return a gpg key with the spesified keyid. Return None if none is found. """
        gpg = self.getGPG()
        
        pub = None
        priv = None
        for key in gpg.list_keys(secret = True):
            if key['fingerprint'] == keyid:
                priv = key
        for key in gpg.list_keys(secret = False):
            if key['fingerprint'] == keyid:
                pub = key
                
        if pub or priv:
            return (pub, priv)
        return None
    
    def getKey(self):
        """ Returns a tuple containing a pair of dicts which have our keys properties in them. Create a new one if one does not already exist. """
        if self.ourCfg['keyid']:
            # Have a key already listed. Validate we can access it. 
            found = self._findKey(keyid = self.ourCfg['keyid'])
            # Ugly, but it'll give the user exact feedback about the key
            if found:
                if found[0] and found[1]:
                    log.debug("Have both a pub and priv key")
                    return found
                elif found[0] and not found[1]:
                    log.error("Have a public key but not a private key")
                    raise MissingPrivateKey("Found a public key %r, but no private key")
                elif not found[0] and found[1]:
                    log.error("Have a public key but not a private key")
                    raise MissingPublicKey("Found a private key %r, but no public key")
                else:
                    log.error("Didn't find a public and private key for keyid %r", self.ourCfg['keyid'])
                    raise MissingKeyError("Didn't find a public and private key for keyid %r" % self.ourCfg['keyid'])
            else:
                log.error("Didn't find a public and private key for keyid %r", self.ourCfg['keyid'])
                raise MissingKeyError("Didn't find a public and private key for keyid %r" % self.ourCfg['keyid'])
        else:
            # No key, create one
            self.genKey()
            return (self.keyPub, self.keyPriv)
        
    def genKey(self):
        """ Create a new key pair for use by rpfwd """
        gpg = self.getGPG()
        
        log.debug("Going to create a new key")
        input_data = gpg.gen_key_input(
                                       key_type = self.ourCfg['keytype'],
                                       key_length = self.ourCfg['keysize'],
                                       name_real = "RPi Forwarder",
                                       name_comment = "",
                                       name_email = 'root@%s' % socket.getfqdn(),
                                       expire_date = 0,
                                       passphrase = self.ourCfg['keypasswd'],
                                       )
        newKey = gpg.gen_key(input_data)
        log.debug("Key created: %r Fingerprint: %r", newKey, newKey.fingerprint)
        # Find our key
        for key in gpg.list_keys(secret = True):
            if key['fingerprint'] == newKey.fingerprint:
                self.keyPriv = key
        for key in gpg.list_keys(secret = False):
            if key['fingerprint'] == newKey.fingerprint:
                self.keyPub = key
        assert self.keyPriv['keyid'] == self.keyPub['keyid']
        
        # Save our key
        if self.ourCfg['keyid']:
            log.debug("Already have a keyid set to %r. Not changing it to %r. ", self.ourCfg['keyid'], self.keyPub['keyid'])
        else:
            log.debug("Saving our new keyid of %r", self.keyPub['keyid'])
            self.ourCfg['keyid'] = self.keyPub['keyid']
            self.config.write()
            
        return self.keyPub['keyid']
        
     
    def restartIfNeeded(self):
        """ Restart our daemon, if it's required. """
        log.debug("No restarted required for %r", self)
