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
from unittest import TestCase, mock

import os
import requests

from everysk.sdk.entities.portfolio.base import Portfolio
from everysk.core.datetime import Date, DateTime
from everysk.core.serialize import dumps
from everysk.core.object import BaseDict
from everysk.core.exceptions import HttpError, SDKError
from everysk.core.http import HttpSDKPOSTConnection

from everysk.sdk.base import BaseSDK, _mount_self_obj, _parser_out

###############################################################################
#   BaseSDK TestCase Implementation
###############################################################################
class TestBaseSDK(TestCase):

    class CustomObjectWithToDict:
        def __init__(self, value):
            self.value = value

        def to_dict(self, with_internals=False):
            return {'value': self.value} if not with_internals else {'value': self.value, 'internal': 'data'}

    def setUp(self):
        self.default_kwargs = {
            'class_name': 'BaseSDK',
            'method_name': 'setUp',  # This will be overridden in each test method.
            'self_obj': None,
            'params': {}
        }
        self.old_post = requests.post
        self.headers = {
            'Accept-Encoding': 'gzip, deflate;q=0.9',
            'Accept-Language': 'en-US, en;q=0.9, pt-BR;q=0.8, pt;q=0.7',
            'Cache-control': 'no-cache',
            'Connection': 'close',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Authorization': 'Bearer SID:TOKEN'
        }
        os.environ['EVERYSK_API_URL_SCHEME'] = 'https'
        os.environ['EVERYSK_API_URL_DOMAIN'] = 'test.com'
        os.environ['EVERYSK_API_SID'] = 'my_SID'
        os.environ['EVERYSK_API_TOKEN'] = 'my_TOKEN'
        response = mock.MagicMock()
        response.content = dumps({'my_SID': 'teste'})
        response.status_code = 200
        requests.post = mock.create_autospec(requests.post)
        requests.post.return_value = response

    def tearDown(self) -> None:
        requests.post = self.old_post

    def test_import_from_sdk_path(self):
        from everysk.sdk import Portfolio as root_Portfolio #pylint: disable=import-outside-toplevel

        self.assertEqual(root_Portfolio, Portfolio)

        with self.assertRaisesRegex(ImportError, "cannot import name 'Module' from 'everysk.sdk'"):
            from everysk.sdk import Module #pylint: disable=import-outside-toplevel

    def test_defaults_are_set(self):
        # Using the context manager to mock HttpSDKPOSTConnection
        http = BaseSDK.get_response(**self.default_kwargs)

        requests.post.assert_called_once_with(
            url='https://test.com/v1/sdk_function',
            headers=self.headers,
            verify=True,
            timeout=30,
            data=dumps(self.default_kwargs)
        )

    def test_automatic_class_name_assignment(self):
        # In this scenario, we are not passing 'class_name'.
        # Directly calling get_response from BaseSDK
        kwargs = {'method_name': 'test_automatic_class_name_assignment'}
        BaseSDK.get_response(**kwargs)

        expected_kwargs = {**self.default_kwargs, **kwargs, 'class_name': 'BaseSDK'}

        requests.post.assert_called_once_with(
            url='https://test.com/v1/sdk_function',
            headers=self.headers,
            verify=True,
            timeout=30,
            data=dumps(expected_kwargs)
        )

    def test_automatic_method_name_assignment(self):
        # In this scenario, we are not passing 'class_name'.
        # Directly calling get_response from BaseSDK
        kwargs = {'class_name': 'BaseSDK'}
        BaseSDK.get_response(**kwargs)

        expected_kwargs = {**self.default_kwargs, **kwargs, 'method_name': 'test_automatic_method_name_assignment'}

        requests.post.assert_called_once_with(
            url='https://test.com/v1/sdk_function',
            headers=self.headers,
            verify=True,
            timeout=30,
            data=dumps(expected_kwargs)
        )

    def test_get_response_raises_sdk_error_on_http_error(self):
        with mock.patch.object(HttpSDKPOSTConnection, 'get_response', side_effect=HttpError("Test HTTP Error")):
            with self.assertRaises(SDKError) as context:
                BaseSDK.get_response()
            self.assertEqual(str(context.exception), "Test HTTP Error")

    def test_get_response_with_sdk_error(self):
        with mock.patch.object(HttpSDKPOSTConnection, 'get_response', return_value={'error_module':'everysk.core.exceptions.SDKError', 'error_message':'SDK sample error'}):
            with self.assertRaisesRegex(SDKError, 'SDK sample error'):
                BaseSDK.get_response()

    def test_to_dict_returns_dict(self):
        class TestSDK(BaseSDK):
            def to_dict(self, with_internals: bool = True) -> dict:
                return super().to_dict(with_internals)

        test_sdk = TestSDK(
            test='test',
            date=Date(2021, 1, 1),
            datetime=DateTime(2021, 1, 1, 1, 1, 1),
            date_list=[Date(2021, 1, 1)],
            datetime_list=[DateTime(2021, 1, 1, 1, 1, 1)],
            dates_dict={'date': Date(2021, 1, 1), 'datetime': DateTime(2021, 1, 1, 1, 1, 1), 'date_list': [Date(2021, 1, 1)], 'datetime_list': [DateTime(2021, 1, 1, 1, 1, 1)]},
            tuple_list=[(Date(2021, 1, 1),)],
            date_tuple=(Date(2021, 1, 1),),
            date_set=set([Date(2021, 1, 1)]),
        )
        test_sdk.obj_list = [TestSDK(
            test='test',
            date=Date(2021, 1, 1),
            datetime=DateTime(2021, 1, 1, 1, 1, 1),
        )]
        self.assertDictEqual(test_sdk.to_dict(), {
            'test': 'test',
            'date': '20210101',
            'datetime': '20210101 01:01:01',
            'date_list': ['20210101'],
            'datetime_list': ['20210101 01:01:01'],
            'dates_dict': {'date': '20210101', 'datetime': '20210101 01:01:01', 'date_list': ['20210101'], 'datetime_list': ['20210101 01:01:01']},
            'tuple_list': [('20210101',)],
            'date_tuple': ('20210101',),
            'date_set': ['20210101'],
            'obj_list': [{
                'test': 'test',
                'date': '20210101',
                'datetime': '20210101 01:01:01',
            }]
        })

    def test_mount_self_obj_none(self):
        self.assertIsNone(_mount_self_obj(None))

    def test_mount_self_obj_with_private_attrs(self):
        class TestObject(BaseDict):
            def __init__(self):
                self._private = 1
                self.public = 2

        test_obj = TestObject()
        result = _mount_self_obj(test_obj)
        self.assertIn('_private', result)
        self.assertIn('public', result)
        self.assertEqual(result['_private'], 1)

    def test_mount_self_obj_with_serializable_object(self):
        class Serializable(BaseDict):
            def __init__(self):
                self.teste = 1
                self._klass = DateTime

        class TestObject(BaseDict):
            def __init__(self):
                self._private = Serializable()

        test_obj = TestObject()
        result = _mount_self_obj(test_obj)
        self.assertDictEqual(result, {'_private': {'teste': 1, '_klass': 'DateTime'}})

    def test_parser_out_with_primitive(self):
        self.assertEqual(_parser_out(42), 42)
        self.assertEqual(_parser_out("test"), "test")

    def test_parser_out_with_list(self):
        self.assertEqual(_parser_out([1, "a", [3, 4]]), [1, "a", [3, 4]])

    def test_parser_out_with_tuple(self):
        self.assertEqual(_parser_out((1, "b", (3, 4))), (1, "b", (3, 4)))

    def test_parser_out_with_set(self):
        self.assertEqual(_parser_out({1, 2, 3}), [1, 2, 3])  # Order might need to be considered

    def test_parser_out_with_dict(self):
        input_dict = {"a": 1, "b": {"c": 2}}
        self.assertDictEqual(_parser_out(input_dict), input_dict)

    def test_parser_out_custom_object_with_to_dict(self):
        obj = self.CustomObjectWithToDict('data')
        self.assertDictEqual(_parser_out(obj, False), {'value': 'data'})
        self.assertDictEqual(_parser_out(obj), {'value': 'data', 'internal': 'data'})

    def test_parser_out_custom_object_with_to_dict_in_list(self):
        obj_list = [self.CustomObjectWithToDict('data1'), self.CustomObjectWithToDict('data2')]
        expected_output = [{'value': 'data1'}, {'value': 'data2'}]
        self.assertListEqual(_parser_out(obj_list, False), expected_output)

    def test_parser_out_custom_object_with_strftime_or_null(self):
        self.assertEqual(_parser_out(DateTime(2020, 1, 1)), '20200101 00:00:00')

    def test_parser_out_with_undefined(self):
        self.assertEqual(_parser_out(Undefined), Undefined.default_parse_string)

    def test_parser_out_with_internals_flag(self):
        obj = self.CustomObjectWithToDict('data')
        self.assertDictEqual(_parser_out(obj, with_internals=False), {'value': 'data'})
        self.assertDictEqual(_parser_out(obj, with_internals=True), {'value': 'data', 'internal': 'data'})
