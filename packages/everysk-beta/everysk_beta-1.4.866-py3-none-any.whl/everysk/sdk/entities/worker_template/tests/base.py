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
from everysk.config import settings

# from everysk.core.datetime import DateTime, ZoneInfo

from everysk.sdk.entities.worker_template.base import WorkerTemplate

from everysk.sdk.base import _mount_self_obj

###############################################################################
#   Report TestCase Implementation
###############################################################################
class WorkerTemplateTestCase(unittest.TestCase):

    def setUp(self):
        self.sample_data = {
            'created_on': None,
            'updated_on': None,
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

    def test_get_id_prefix(self):
        self.assertEqual(WorkerTemplate.get_id_prefix(), settings.WORKER_TEMPLATE_ID_PREFIX)

    def test_validate(self):
        worker_template: WorkerTemplate = self.worker_template.copy()
        with unittest.mock.patch('everysk.sdk.base.HttpSDKPOSTConnection') as mock_http_connection:
            mock_http_connection.return_value.get_response.return_value = True
            result = worker_template.validate()

        mock_http_connection.assert_called_once_with(class_name='WorkerTemplate', params={}, method_name='validate', self_obj=_mount_self_obj(worker_template))
        mock_http_connection.return_value.get_response.assert_called_once_with()
        self.assertTrue(result)
