"""Module provider for IBM Cloud"""
from __future__ import absolute_import
import json
import logging
import requests

from lexicon.providers.cloudflare import Provider as CloudflareProvider


LOGGER = logging.getLogger(__name__)

NAMESERVER_DOMAINS = ['cloud.ibm.com']


def provider_parser(subparser):
    """Return the parser for this provider"""
    subparser.add_argument(
        "--auth-token", help="IBM Cloud API key")
    subparser.add_argument(
        "--ibm-crn", help="IBM Cloud Internet Services CRN")


class Provider(CloudflareProvider):
    """Provider class for IBM Cloud"""
    def __init__(self, config):
        super(Provider, self).__init__(config)
        self.domain_id = None
        self.api_endpoint = 'https://api.cis.cloud.ibm.com/v1/{}'.format(
            self._get_provider_option('ibm_crn').replace('/', '%2F')
        )
        self.ibm_auth_token = self.ibm_get_iamtoken()

    def ibm_get_iamtoken(self):
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "accept": "application/json",
        }
        params = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": self._get_provider_option('auth_token'),
        }
        url = "https://iam.cloud.ibm.com/identity/token"
        resp = requests.post(url, params, headers=headers, timeout=30)

        return resp.json()["access_token"]

    def _request(self, action='GET', url='/', data=None, query_params=None):
        if data is None:
            data = {}
        if query_params is None:
            query_params = {}
        default_headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'x-auth-user-token': 'Bearer {0}'.format(self.ibm_auth_token)
        }
        if not url.startswith(self.api_endpoint):
            url = self.api_endpoint + url

        response = requests.request(action, url, params=query_params,
                                    data=json.dumps(data),
                                    headers=default_headers,
                                    timeout=30)

        # if the request fails for any reason, throw an error.
        response.raise_for_status()
        return response.json()
