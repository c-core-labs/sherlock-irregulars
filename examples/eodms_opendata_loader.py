# -*- coding: utf-8 -*-
"""
EODMS OpenData Api adapter
"""
import logging
import os
from os.path import join
import requests
from ogr import CreateGeometryFromWkt
from pystac import Link
from requests.auth import HTTPBasicAuth

from irregulars.base import STACAdapter
from irregulars.mappings import BaseStacMappings

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

EODMS_USER = os.environ.get('EODMS_USER')
EODMS_PASS = os.environ.get('EODMS_PASS')


class RadarSat1StacMappings(BaseStacMappings):
    """
    Mappings for Conversion of Radarsat1 dhus api.
    """
    ID = 'id'
    TITLE = 'identifier'
    DESCRIPTION = 'summary'
    COLLECTION = 'collection'
    LICENSE = 'license_title'
    GEOMETRY = 'footprint'
    DATETIME = 'endposition'
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
    PUBLISHED = 'ingestiondate'
    KEYWORD_ATTRIBUTES = ('subject', 'topic_category')
    URL_BASE = r'https://www.eodms-sgdot.nrcan-rncan.gc.ca/wes/Client/?entryPoint=resultDetails&resultId=3833067&collectionId=Radarsat1#'
    PROVIDER_NAME = 'Government of Canada'
    PROVIDER_DESCRIPTION = 'Canadian EODMS'
    PROVIDER_ROLES = ['licensor', 'producer', 'processor', 'host']
    OVERLOADED_TERMS = [ID, TITLE, DATETIME, COLLECTION, GEOMETRY, DESCRIPTION]
    ASSET_URL = 'href'
    ASSET_DESCRIPTION = 'rel'

    ROLE_DICT = {
        None: 'data',
        'icon': 'thumbnail',
        'alternative': 'overview'
    }
    TYPE_DICT = {
        None: 'zip',
        'icon': 'image/jpeg',
        'alternative': 'image/jpeg',
        'product': 'product'
    }

    @property
    def collection(self):
        """
        Collection Attribute
        """
        return 'radarsat1'
    # End collection property
# End RadarSat1StacMappings class


class RSAT1Adapter(STACAdapter):
    """
    Adapt Source Metadata to STAC
    """
    SOURCE_URL = r'https://data.eodms-sgdot.nrcan-rncan.gc.ca/api/dhus/v1/products' \
                 r'/Radarsat1/search?q=producttype:SGF&rows=100'

    mappings = RadarSat1StacMappings

    def fetch_results(self):
        """
        Fetch results from api
        """
        href = self.SOURCE_URL
        resp = requests.get(href, auth=HTTPBasicAuth(EODMS_USER, EODMS_PASS)).json()
        while href:
            href = resp.get('link')[2].get('href')
            for entry in resp.get('entry'):
                yield entry
            resp = requests.get(href, auth=HTTPBasicAuth(EODMS_USER, EODMS_PASS)).json()
            if not resp.get('entry'):
                break

    # End fetch_results method

    def process_results(self, json_result):
        """
        Process group of results
        """

        stac_item = self.create_stac_item(json_result)
        if not stac_item:
            return
        asset_sources = json_result.get('link')
        self._build_assets(stac_item, asset_sources, 'rel')

        stac_json = stac_item.to_dict()

        self.publish_to_server(stac_json)

    # End process_results method

    def interpret_geometry(self, original_entry):
        """
        Extract Native geospatial to geojson geometry object.
        """
        geometry = CreateGeometryFromWkt(
            original_entry.get(self.mappings.GEOMETRY))

        return geometry.ExportToJson(), geometry.GetEnvelope()

    # End _interpret_geometry method

    def create_asset(self, asset):
        """
        Overload to handle download link having no title
        """
        if not asset.get(self.mappings.ASSET_TITLE):

            asset[self.mappings.ASSET_TITLE] = 'Radarsat1 archived product'
        return super(RSAT1Adapter, self).create_asset(asset)
    # End create_asset method

    def create_stac_item(self, original_entry):
        """
        Overload to add additional metadata.
        """
        stac_item = super(RSAT1Adapter, self).create_stac_item(original_entry)
        stac_item.common_metadata.mission = 'radarsat1'
        stac_item.links = [
            Link('original', self.extract_source_link(original_entry),
                 title='Original EODMS reference')]
        return stac_item
    # End create_stac_item(self, original_entry): method

    def extract_source_link(self, original_entry):
        """
        Extract Link to metadata source
        """
        parsed_out_eomdms_id = None
        for link in original_entry.get('link'):
            if link.get('rel') == 'icon':
                parsed_out_eomdms_id = link.get('href').split('-')[-1]
        if parsed_out_eomdms_id:
            return join(self.mappings.URL_BASE.format(parsed_out_eomdms_id))
    # End _extract_source_link method
# End RSAT1Adapter class


if __name__ == '__main__':
    adapter = RSAT1Adapter()
    print(adapter.SOURCE_URL)
    adapter()
