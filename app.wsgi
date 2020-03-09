#!/usr/local/bin/python3.6
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/trackerApi/")

from app import app as application
