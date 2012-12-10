'''
Created on Dec 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
'''
import logging, logging.config
log = logging.getLogger("rpfwd.config")
# log.debug('initing')

import os, os.path, sys, stat


from configobj import ConfigObj

def getConfig(
              location = "/boot/rpfwd/rpfwd.ini",
              configspecLocation = "/usr/share/doc/rpfwd/rpfwd.configspec.ini",
              ):
    """ Return a copy of the config """
    log.debug("Creating config spec object from %r", configspecLocation)
    configspec = ConfigObj(
                           configspecLocation,
                           list_values = False,
                           )
    
    config = ConfigObj(location, configspec = configspec)
    
    return config
