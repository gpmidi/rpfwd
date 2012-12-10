#!/usr/bin/python
""" Generate and enable all of our configs

"""
import logging, logging.config
log = logging.getLogger("rpfwd.rpfwdinit.__init__")
# log.debug('initing')

from optparse import OptionParser
import os, os.path, sys, stat

from rpfwd.config import getConfig

def main():
    """ Generate and enable all of our configs """
    parser = OptionParser(
                          usage = "%prog",
                          # version = "%prog v0.1",
                          prog = "rpfwdInit",
                          description = """Generate and enable all of our configuration files.                        
                          """,
                          )
    parser.add_option(
                      "-v",
                      "--verbose",
                      action = "append",
                      dest = "verboseCounter",
                      default = logging.WARN / 10,
                      help = "Increase logging verbosity. Can be used multiple times. ",
                      )
    parser.add_option(
                      "--config",
                      action = "store",
                      type = "string",
                      dest = "mainConfigLoc",
                      default = "/boot/rpfwd/rpfwd.ini",
                      help = "The location that the main config file can be found. [Default: %default]",
                      )
    parser.add_option(
                      "--staticFileLoc",
                      action = "store",
                      type = "string",
                      dest = "staticFileLoc",
                      # TODO: Move this somewhere where it makes more sense
                      default = "/usr/share/doc/rpfwd/",
                      help = "The location that the various helper files can be found. [Default: %default]",
                      )
    
    log.debug("Parsing args")
    (opts, args) = parser.parse_args()
    
    # Set logging threshold
    lLevel = opts.verboseCounter * 10
    log.setLevel(lLevel)
    
    # Validate the main ini
    if not os.access(opts.mainConfigLoc, os.R_OK | os.W_OK):
        log.error("Can't read and/or write the main config file: %r", opts.mainConfigLoc)
        sys.exit(1)
    
    # Validate the helper files
    if not os.access(opts.staticFileLoc, os.R_OK):
        log.error("Can't read the helper files location: %r", opts.staticFileLoc)
        sys.exit(1)
    
    cfg = getConfig(
                    location = opts.mainConfigLoc,
                    configspecLocation = os.path.join(opts.staticFileLoc, 'rpfwd.configspec.ini'),
                    )
    
    
    
    log.debug("Done")
