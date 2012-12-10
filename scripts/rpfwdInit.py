#!/usr/bin/python
""" A script to init a Raspbian-based Raspberry Pi based on 
settings in /boot/rpfwd/rpfwd.ini and other files in /boot/rpfwd/. 

"""
import logging, logging.config
log = logging.getLogger("rpfwd.scripts.rpfwdInit")
logging.basicConfig(
                    level = logging.INFO,
                    # format = '%(asctime)s %(levelname)s %(message)s',
                    )
log.debug('initing')

from rpfwd.rpfwdinit import main
log.debug("Imported main function")

if __name__ == "__main__":
    log.debug("Going to start main")
    main()
    log.debug("Done")
    
    
