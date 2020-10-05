# -*- coding: utf-8 -*-
"""
Utilites
"""
import logging


__author__ = 'Gerard Noseworthy - LOOKNorth.'
__email__ = 'gerard.noseworthy@c-core.ca'

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def sanitize_keywords(keywords):
    """
    Reduce kewords to lowercase and space seperated.
    """
    if isinstance(keywords, str):
        keywords = keywords.split(';')

    if not isinstance(keywords, list):
        raise (TypeError("Keyword Attribute needs to be list"))

    return [k.replace('_', ' ').lower() for k in keywords]
# End sanitize_keywords function

if __name__ == '__main__':
    pass
