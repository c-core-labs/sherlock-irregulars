# -*- coding: utf-8 -*-
"""
Base Stac Mapping Classes
"""
import logging
from datetime import datetime

__author__ = 'Gerard Noseworthy - LOOKNorth.'
__email__ = 'gerard.noseworthy@c-core.ca'

from utils import sanitize_keywords


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class BaseAssetMapping(object):
    """
    Enum Class for Mapping Assets
    """

    def __init__(self):
        """
        Initialize the BaseAssetMapping class
        """
        super(BaseAssetMapping, self).__init__()
    # End init built-in
# End BaseAssetMapping class


class BaseStacMappings(object):
    """
    Enum Class for mapping json results to STAC
    """
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    COLLECTION = None
    DATETIME = None
    DESCRIPTION = None
    KEYWORD_ATTRIBUTES = None
    GEOMETRY = None
    ID = None
    LICENSE = None
    PUBLISHED = None
    TITLE = None
    PROVIDER_NAME = None
    PROVIDER_DESCRIPTION = None
    PROVIDER_ROLES = []
    OVERLOADED_TERMS = [ID, TITLE, DATETIME, COLLECTION, GEOMETRY, DESCRIPTION]
    ASSET_URL = None
    ASSET_DESCRIPTION = None
    ASSET_TITLE = None
    ROLE_DICT = {}
    TYPE_DICT = {}

    def __init__(self, json_props):
        """
        Initialize the CanadaOpenDataStacMappings class
        """
        super(BaseStacMappings, self).__init__()

        self._props = json_props

    # End init built-in

    # End init built-in

    @property
    def all_source_attributes(self):
        """

        """
        return [self.ID, self.TITLE, self.DESCRIPTION, self.COLLECTION, self.LICENSE,
                self.GEOMETRY]
    # End all_source_attributes property

    @property
    def collection(self):
        """
        Collection Attribute
        """
        return self._props.get(self.COLLECTION)
    # End collection property

    @property
    def datetime(self):
        """
        Item Timestamp
        :rtype datetime
        """
        return datetime.strptime(self._props.get(self.DATETIME), self.DATETIME_FORMAT)
    # End datetime property

    @property
    def description(self):
        """
        Description Attribute
        """
        return self._props.get(self.DESCRIPTION)

    # End description property

    @property
    def geometry(self):
        """
        Json geometry
        :rtype dict
        """
        return self._props.get(self.GEOMETRY)

    # End geometry property

    @property
    def identifier(self):
        """
        ID attribute
        """
        return self._props.get(self.ID)
    # End identifier property

    @property
    def has_provider(self):
        """
        Check for appropriate provider attributes
        """
        return self.PROVIDER_NAME and self.PROVIDER_DESCRIPTION and self.PROVIDER_ROLES
    # End has_provider property

    @property
    def keywords(self):
        """
        Keywords
        rtyle: list
        """
        keywords = set()
        for kw_att in self.KEYWORD_ATTRIBUTES:
            kws = self._props.get(kw_att)
            if not kws:
                continue
            keywords.update(sanitize_keywords(kws))
        return list(keywords)

    # End keywords property

    @property
    def license(self):
        """
        Liscence Attribute
        """
        return self._props.get(self.LICENSE, 'proprietary')
    # End license property

    @property
    def publish_date(self):
        """
        Publication Datetime
        :rtype datetime
        """
        return datetime.strptime(self._props.get(self.PUBLISHED), self.DATETIME_FORMAT)
    # End publish_date property

    @property
    def title(self):
        """
        Title Attribute
        """
        return self._props.get(self.TITLE)
    # End title property
# End BaseStacMappings class


class CanadaOpenDataStacMappings(BaseStacMappings):
    """
    Canaddian Geospatial Data portal mappings
    """
    ID = 'id'
    TITLE = 'title'
    DESCRIPTION = 'notes'
    COLLECTION = 'collection'
    LICENSE = 'license_title'
    GEOMETRY = 'spatial'
    DATETIME = 'time_period_coverage_start'
    PUBLISHED = 'date_published'
    KEYWORD_ATTRIBUTES = ('subject', 'topic_category')
    URL_BASE = r'https://open.canada.ca/data/en/dataset/'

    OVERLOADED_TERMS = [ID, TITLE, DATETIME, COLLECTION, GEOMETRY, DESCRIPTION, PUBLISHED]

    ROLE_DICT = {
        'web_service': 'data',
        'dataset': 'data',
        'guide': 'metadata'
    }

    @property
    def english_keywords(self):
        """
        # Keyywords attribute needs special handling for
        """
        keywords_tag = 'keywords'
        keywords_language = 'en'
        return self._props.get(keywords_tag, {}).get(keywords_language)
    # End english_keywords property

    @property
    def keywords(self):
        """
        Keywords
        rtyle: list
        """
        keywords = set()
        for kw_att in self.KEYWORD_ATTRIBUTES:
            kws = self._props.get(kw_att)
            if not kws:
                continue
            keywords.update(sanitize_keywords(kws))
        keywords.update(self.english_keywords)
        return list(keywords)

    # End keywords property
    @property
    def source_link(self):
        """
        Create Source Link
        """
        return
    # End source_link property
# End CanadaOpenDataStacMappings class


if __name__ == '__main__':
    pass
