###############################################################################
#
# (C) Copyright 2024 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

###############################################################################
#   Imports
###############################################################################
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning # pylint: disable=import-error
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) # pylint: disable=no-member

###############################################################################
#   HTTPClient Implementation
###############################################################################
class HTTPClient(object):
    def __init__(self, timeout=3600, verify_ssl_certs=True, allow_redirects=False) -> None:
        self.timeout = timeout
        self.allow_redirects = allow_redirects
        self.verify_ssl_certs = verify_ssl_certs

    def request(self, method, url, headers, params=None, payload=None):
        raise NotImplementedError(
            'HTTPClient subclasses must implement `request`'
        )

###############################################################################
#   Requests Client Implementation
###############################################################################
class RequestsClient(HTTPClient):
    def request(self, method, url, headers, params=None, payload=None):

        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            json=payload,
            timeout=self.timeout,
            verify=self.verify_ssl_certs,
            allow_redirects=self.allow_redirects
        )
        return (response.status_code, response.content)

def new_default_http_client(*args, **kwargs):
    return RequestsClient(*args, **kwargs)
