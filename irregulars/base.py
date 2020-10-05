# -*- coding: utf-8 -*-
"""
<<DESCRIPTION OF SCRIPT>>
"""
import logging


__author__ = 'Gerard Noseworthy - LOOKNorth.'
__email__ = 'gerard.noseworthy@c-core.ca'

import requests
from pystac import Item, Asset, Provider
from irregulars.mappings import BaseStacMappings
from irregulars.utils import sanitize_keywords
from config import PUBLISH_URL


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class STACAdapter(object):
    """
    Adapt Source Metadata to STAC
    """

    mappings = BaseStacMappings

    def __init__(self, *args):
        """
        Initialize the STACAdapter class
        """
        super(STACAdapter, self).__init__()
        self.failed = 0
        self.completed = 0
    # End init built-in

    def __call__(self):
        """
        Make Class Callable
        """
        for entry in self.fetch_results():
            self.process_results(entry)

        log.info('processing complete with {0} sucessful and {1} failed entries').format(
            self.completed, self.failed)

    # End call built-in

    @property
    def provider(self):
        """
        Attributes for Data provider
        """
        if not self.mappings.has_provider:
            return
        return Provider(self.mappings.PROVIDER_NAME, self.mappings.PROVIDER_DESCRIPTION,
                        self.mappings.PROVIDER_ROLES)
    # End provider property

    def fetch_results(self):
        """
        Acquire results from remote source
        """
        raise NotImplementedError()

    def process_results(self, json_results):
        """
        Transform results to STAC
        """
        raise NotImplementedError()

    def _build_assets(self, stac_entry, asset_sources, asset_name_attribute):
        """
        Build Assets from source urls
        """
        assets = {}
        for asset in asset_sources:
            asset_name = asset.get(asset_name_attribute, 'product')
            stac_entry.add_asset(asset_name, self.create_asset(asset))
        # return stac_entry
        return assets
    # End _build_assets method

    def create_asset(self, asset):
        """

        """
        desc = asset.get(self.mappings.ASSET_DESCRIPTION)
        return Asset(asset.get(self.mappings.ASSET_URL),
                     title=asset.get(self.mappings.ASSET_TITLE),
                     description=desc,
                     media_type=self.mappings.TYPE_DICT.get(desc),
                     roles=[self.mappings.ROLE_DICT.get(desc)],
                     )
    # End create_asset method

    def create_stac_item(self, original_entry):
        """
        Generate Stac Entry from individual input.
        """
        entry = self.mappings(original_entry)
        if not entry.geometry:
            self.failed += 1
            return

        props = self.extract_properties(original_entry, self.mappings.OVERLOADED_TERMS)

        license = entry.license

        reqs = self.extract_required_attributes(entry)
        if not reqs:
            return
        (timestamp, id_, title, description, collection) = reqs

        if timestamp.year < 1970:
            timestamp = timestamp.replace(year=1970)

        keywords = self.extract_keywords(original_entry)
        if keywords:
            props['keywords'] = keywords

        extent, geometry = self.interpret_geometry(original_entry)

        pystac_entry = Item(id_, geometry, extent,
                            timestamp, props,
                            collection=collection)

        pystac_entry.common_metadata.title = title
        pystac_entry.common_metadata.license = license

        pystac_entry.common_metadata.description = description
        pystac_entry.common_metadata.provider = self.provider
        return pystac_entry

    def extract_properties(self, original_entry, overloads):
        """
        Extract metadata properties to props based on attribut mapping.
        """
        accessory_props = {}
        for k, v in original_entry.items():
            if k in overloads:
                continue
            if v and isinstance(v, str):
                accessory_props[k] = v
        return accessory_props
    # End _extract_properties method

    def extract_required_attributes(self, entry):
        id_ = entry.identifier
        try:
            coverage_date = entry.datetime
        except TypeError:
            log.warning("{0} failed to load due to datetime".format(id_))
            self.failed += 1
            return
        title = entry.title
        collection = entry.collection
        desc = entry.title

        return coverage_date, id_, title, desc, collection

    def extract_keywords(self, original_entry):
        keywords = set()
        for kw_att in self.mappings.KEYWORD_ATTRIBUTES:
            kws = original_entry.get(kw_att)
            if not kws:
                continue
            keywords.update(sanitize_keywords(kws))
        return list(keywords)
    # End create_stac_item method

    def interpret_geometry(self, original_entry):
        """
        Extract Native geospatial to geojson geometry object.
        """
        extent = original_entry.get('extent')
        geometry = original_entry.get('geometry')

        return extent, geometry

    # End _interpret_geometry method

    def publish_to_server(self, data):
        """
        Dispatch created stac item
        """
        resp = requests.put(PUBLISH_URL,
                            data=data)
        status = resp.status_code
        if status == 400:
            self.completed += 1
        else:
            self.failed +=1
    # End store_result method
# End STACAdapter class
