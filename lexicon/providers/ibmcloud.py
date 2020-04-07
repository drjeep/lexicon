"""Module provider for IBM Cloud"""
from __future__ import absolute_import
import json
import logging

import requests
from lexicon.providers.base import Provider as BaseProvider


LOGGER = logging.getLogger(__name__)

NAMESERVER_DOMAINS = ['cloud.ibm.com']


def provider_parser(subparser):
    """Return the parser for this provider"""
    subparser.add_argument(
        "--auth-token", help="specify api key for authentication")


class Provider(BaseProvider):
    """Provider class for IBM Cloud"""
    def __init__(self, config):
        super(Provider, self).__init__(config)
        self.domain_id = None
        self.api_endpoint = 'https://api.cis.cloud.ibm.com'

    def _authenticate(self):
        # self.domain_id = result['zone_id']
        pass

    # Create record. If record already exists with the same content, do nothing.
    def _create_record(self, rtype, name, content):
        return True

    # List all records. Return an empty list if no records found.
    # type, name and content are used to filter records.
    # If possible filter during the query, otherwise filter after response is received.
    def _list_records(self, rtype=None, name=None, content=None):
        return []

    # Create or update a record.
    def _update_record(self, identifier, rtype=None, name=None, content=None):
        return True

    # Delete an existing record. If record does not exist, do nothing.
    def _delete_record(self, identifier=None, rtype=None, name=None, content=None):
        return True

    # Helpers
    def _request(self, action='GET', url='', data=None, query_params=None):
        pass
