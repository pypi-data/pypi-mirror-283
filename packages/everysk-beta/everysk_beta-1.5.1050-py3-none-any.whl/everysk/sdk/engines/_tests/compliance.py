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
from unittest import TestCase, mock

from everysk.sdk.engines.compliance import Compliance

from everysk.core.http import HttpSDKPOSTConnection

from everysk.config import settings

###############################################################################
#   Compliance Test Case Implementation
###############################################################################
class ComplianceTestCase(TestCase):

    def setUp(self) -> None:
        self.headers = HttpSDKPOSTConnection().get_headers()
        self.api_url = HttpSDKPOSTConnection().get_url()
        return super().setUp()

    ###############################################################################
    #   Check Method Test Case Implementation
    ###############################################################################
    def test_check_method_returns_expected_response(self):
        expected_data = '{"class_name": "Compliance", "method_name": "check", "self_obj": null, "params": {"rules": [{"rule": "rule1"}, {"rule": "rule2"}], "datastore": [{"data": "data1"}, {"data": "data2"}], "metadata": null}}'
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value.content = '{}'
            mock_post.return_value.status_code = 200
            Compliance.check(rules=[{'rule': 'rule1'}, {'rule': 'rule2'}], datastore=[{'data': 'data1'}, {'data': 'data2'}])

        mock_post.assert_called_with(
            url=self.api_url,
            headers=self.headers,
            verify=settings.HTTP_DEFAULT_SSL_VERIFY,
            timeout=settings.EVERYSK_SDK_HTTP_DEFAULT_TIMEOUT,
            data=expected_data
        )
