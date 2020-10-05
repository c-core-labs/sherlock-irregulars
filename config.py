# -*- coding: utf-8 -*-
"""
Config Information
"""
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


load_dotenv()

PUBLISH_URL = os.environ.get('PUBLISH_URL')
PUBLISH_USERNAME = os.environ.get('PUBLISH_USER_NAME')
PUBLISH_PASSWORD = os.environ.get('PUBLISH_PASSWORD')

