###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

###############################################################################
#   Imports
###############################################################################
import unittest
from unittest import mock

from everysk.config import settings
from everysk.core.datetime import DateTime
from everysk.core.exceptions import SDKValueError
from everysk.core.http import HttpSDKPOSTConnection

from everysk.sdk.entities.worker_template.base import WorkerTemplate
from everysk.sdk.entities.query import Query

###############################################################################
#   Report TestCase Implementation
###############################################################################
class WorkerTemplateTestCase(unittest.TestCase):

    def setUp(self):
        self.sample_data = {
            'created_on': DateTime(2023, 9, 9, 9, 9, 9, 9),
            'updated_on': DateTime(2023, 9, 9, 9, 9, 9, 9),
            'version': 'v1',
            'id': 'wrkt_xyz',
            'sort_index': 1,
            'category': 'portfolio',
            'form_outputs': {
                'OUTPUT_ONE': [
                    {
                        'key': 'value',
                    }
                ]
            },
            'script_entry_point': 'main',
            'tags': [],
            'type': 'BASIC',
            'script_visible_source': "def main(args):\n    print('test')\n    return",
            'form_functions': {},
            'ports': [
                {
                    'key': 'value',

                }
            ],
            'name': 'Worker Teste',
            'script_source': "def main(args):\n    print('test')\n    return",
            'icon': 'retriever',
            'script_runtime': 'python',
            'description': '#Worker Sample',
            'form_inputs': [
                {
                    'key': 'value'
                }

            ],
            'visible': True,
            'default_output': 'OUTPUT_ONE',
        }
        self.worker_template = WorkerTemplate(**self.sample_data)
        self.headers = HttpSDKPOSTConnection().get_headers()
        self.api_url = HttpSDKPOSTConnection().get_url()

    def test_get_id_prefix(self):
        self.assertEqual(WorkerTemplate.get_id_prefix(), settings.WORKER_TEMPLATE_ID_PREFIX)

    def test_validate(self):
        expected_data = '{"class_name": "WorkerTemplate", "method_name": "validate", "self_obj": {"created_on": {"__datetime__": "2023-09-09T09:09:09.000009+00:00"}, "updated_on": {"__datetime__": "2023-09-09T09:09:09.000009+00:00"}, "version": "v1", "id": "wrkt_xyz", "sort_index": 1, "category": "portfolio", "form_outputs": {"OUTPUT_ONE": [{"key": "value"}]}, "script_entry_point": "main", "tags": [], "type": "BASIC", "script_visible_source": "def main(args):\\n    print(\'test\')\\n    return", "form_functions": {}, "ports": [{"key": "value"}], "name": "Worker Teste", "script_source": "def main(args):\\n    print(\'test\')\\n    return", "icon": "retriever", "script_runtime": "python", "description": "#Worker Sample", "form_inputs": [{"key": "value"}], "visible": true, "default_output": "OUTPUT_ONE", "path_name": null, "__class_path__": "everysk.sdk.entities.worker_template.base.WorkerTemplate"}, "params": {}}'
        worker_template: WorkerTemplate = self.worker_template.copy()

        with mock.patch('requests.post') as mock_post:
            mock_post.return_value.content = '{}'
            mock_post.return_value.status_code = 200
            worker_template.validate()

        mock_post.assert_called_with(
            url=self.api_url,
            headers=self.headers,
            verify=settings.HTTP_DEFAULT_SSL_VERIFY,
            timeout=settings.EVERYSK_SDK_HTTP_DEFAULT_TIMEOUT,
            data=expected_data
        )

    ###############################################################################
    #   Check Query Test Case Implementation
    ###############################################################################
    def test_check_query_returns_valid(self):
        worker_template: WorkerTemplate = self.worker_template
        result = worker_template._check_query(query='test_query') # pylint: disable=protected-access

        self.assertEqual(result, True)

    def test_check_entity_to_query_raises_sdk_error(self):
        with self.assertRaises(SDKValueError) as context:
            worker_template: WorkerTemplate = self.worker_template
            worker_template['tags'] = ['tag1', 'tag2']
            worker_template._check_entity_to_query() # pylint: disable=protected-access

        self.assertEqual(str(context.exception), "Can't filter by Name and Tags at the same time")

    ###############################################################################
    #   Mount Query Test Case Implementation
    ###############################################################################
    def test_mount_query_with_name(self):
        expected_query = Query(**{'_klass': WorkerTemplate, 'filters': [('name', '<', 'worker testf'), ('name', '>=', 'worker teste')], 'order': [], 'projection': None, 'distinct_on': [], 'limit': 1, 'offset': None, 'page_size': None, 'page_token': None})
        worker_template: WorkerTemplate = self.worker_template
        result = worker_template.to_query(limit=1)

        self.assertEqual(result, expected_query)

    def test_mount_query_with_tags(self):
        expected_query = Query(**{'_klass': WorkerTemplate, 'filters': [('tags', '=', 'tag1'), ('tags', '=', 'tag2')], 'order': [], 'projection': None, 'distinct_on': [], 'limit': 1, 'offset': None, 'page_size': None, 'page_token': None})
        worker_template: WorkerTemplate = self.worker_template
        worker_template['name'] = None
        worker_template['tags'] = ['tag1', 'tag2']
        result = worker_template.to_query(limit=1)

        self.assertEqual(result, expected_query)
