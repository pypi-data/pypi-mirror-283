###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
# Classes that handle HTTP Connections.

# Url: https://requests.readthedocs.io/en/latest/
#      https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers
#      https://developer.mozilla.org/en-US/docs/Glossary/Quality_values
#
import random
import time

import requests
from everysk.core.exceptions import HttpError, InvalidArgumentError
from everysk.core.object import BaseObject
from everysk.core.serialize import dumps, loads
from everysk.core.fields import BoolField, DictField, IntField, StrField
from everysk.core.log import Logger
from everysk.config import settings


log = Logger(name='everysk-lib-core-http-log')


class HttpConnectionConfig(BaseObject):
    # Activate/deactivate the use of the verify flag on HTTP requests.
    # By default this is defined in settings.HTTP_REQUESTS_VERIFY
    # but could be defined in the class configuration too.
    ssl_verify = BoolField(default=True)

    # Limit for retries
    retry_limit = IntField(default=5)

    # Times that randrange will use to do the next retry
    retry_end_seconds = IntField(default=30)
    retry_start_seconds = IntField(default=5)

    def get_ssl_verify(self) -> bool:
        return self.ssl_verify if settings.HTTP_REQUESTS_VERIFY is Undefined else settings.HTTP_REQUESTS_VERIFY


class HttpConnection(BaseObject):
    """
    Base class to use for HTTP connections, has two attributes:
        - timeout: It's in and represent seconds, defaults to 30.
        - url: It's string and will be the destination.
    """
    class Config(HttpConnectionConfig):
        pass

    ## Private attributes
    _retry_count = IntField(default=1) # Used to control how many times this connection was retry

    ## Public attributes
    config: Config # To autocomplete correctly
    headers = DictField(default=None)
    timeout = IntField(default=settings.HTTP_DEFAULT_TIMEOUT)
    url = StrField(default=None)

    def _clean_response(self, response: requests.models.Response) -> requests.models.Response:
        """
        Checks status_code for response, if status_code is different than 200 throws an exception.

        Args:
            response (requests.models.Response): Http response from server.

        Raises:
            HttpError: If something goes wrong raise exception with status_code and content.
        """
        if getattr(response, 'status_code', settings.HTTP_SUCCESS_STATUS_CODES[0]) not in settings.HTTP_SUCCESS_STATUS_CODES:
            raise HttpError(status_code=response.status_code, msg=response.content)

        return response

    def get_headers(self) -> dict:
        """
        Headers needed to send HTTP methods.
        Below are the most common Headers used by browsers,
        we use them to look less like a Bot and more like a valid access.
        """
        headers = settings.HTTP_DEFAULT_HEADERS.copy()
        if self.headers is not None:
            headers.update(self.headers)

        return headers

    def get_url(self) -> str:
        """
        Generate the correct url to fetch data from vendor on POST/GET requests.
        """
        return self.url

    def message_error_check(self, message: str) -> bool: # pylint: disable=unused-argument
        """
        If this method returns True, the connection will be tried again.

        Args:
            message (str): The error message that occurred on the connection.
        """
        return False

    def _get_response_from_url(self) -> requests.models.Response:
        """
        This will be implemented on child classes to really do the connection.
        """
        return None

    def get_response(self) -> requests.models.Response:
        """
        Try to fetch data from self.get_url and calling self._get_response_from_url for the complete response.
        On HttpError, if self.message_error_check is True we will try connect again for a few more times.
        """
        try:
            response = self._clean_response(self._get_response_from_url())
            # After a success we set the value to 1 again
            self._retry_count = 1
        except Exception as error: # pylint: disable=broad-exception-caught
            # Sometimes it can happen that the server is busy, if this happen the error message must be tested
            # and must return true to enable recursion and we will try again the connection.
            if self.message_error_check(str(error).lower()) and self._retry_count < self.config.retry_limit:
                self._retry_count += 1
                # As we have several processes, we use a random number to avoid collision between them.
                time.sleep(random.randint(self.config.retry_start_seconds, self.config.retry_end_seconds))
                response = self.get_response()
            else:
                raise error

        return response


class HttpGETConnection(HttpConnection):
    """ Class that implements a interface for HTTP GET connections """
    params = DictField()
    user = StrField()
    password = StrField()

    def get_params(self) -> dict:
        """
        This method is used to make the correct params to pass on GET request.
        These params will be added to the URL with & separating then.
        """
        return self.params

    def _get_response_from_url(self) -> requests.models.Response:
        """
        Try to fetch data from url using GET request.
        Note that any dictionary key whose value is None will not be added to the URL's query string.
        """
        params = {
            'url': self.get_url(),
            'headers': self.get_headers(),
            'params': self.get_params(),
            'verify': self.config.get_ssl_verify(),
            'timeout': self.timeout
        }
        if self.user:
            params['auth'] = (self.user, self.password)

        if settings.HTTP_LOG_RESPONSE:
            dct = params.copy()
            # To remove the password in the logs
            if 'auth' in params:
                dct['auth'] = (params['auth'][0], '***********')

            log.debug('HTTP GET request: %s', dct)

        response = requests.get(**params)

        if settings.HTTP_LOG_RESPONSE:
            dct = {
                'status_code': response.status_code,
                'time': response.elapsed.total_seconds(),
                'headers': response.headers,
                'content': response.content
            }
            log.debug('HTTP GET response: %s', dct)

        return response


class HttpPOSTConnection(HttpConnection):
    """
    Class that implements a interface for HTTP POST connections.
    If self.is_json is True the POST method will be a JSON POST,
    otherwise will be a Form POST Data.
    """
    is_json = BoolField(default=True)
    payload = DictField()

    def get_headers(self) -> dict:
        """ Headers needed to send HTTP Post methods. """
        headers = super().get_headers()
        if self.is_json:
            headers['Content-Type'] = 'application/json; charset=utf-8'
        else:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'

        return headers

    def get_payload(self) -> dict:
        """ Make the correct payload body to pass on POST request. """
        return self.payload

    def _get_response_from_url(self) -> requests.models.Response:
        """ Try to get/set data on url using POST request. """
        params = {
            'url': self.get_url(),
            'headers': self.get_headers(),
            'verify': self.config.get_ssl_verify(),
            'timeout': self.timeout
        }
        if self.is_json:
            params['json'] = self.get_payload()
        else:
            params['data'] = self.get_payload()

        if settings.HTTP_LOG_RESPONSE:
            log.debug('HTTP POST request: %s', params)

        response = requests.post(**params)

        if settings.HTTP_LOG_RESPONSE:
            dct = {
                'status_code': response.status_code,
                'time': response.elapsed.total_seconds(),
                'headers': response.headers,
                'content': response.content
            }
            log.debug('HTTP POST response: %s', dct)

        return response


class HttpPOSTCompressedConnection(HttpPOSTConnection):

    def get_payload(self) -> dict:
        """ Make the correct payload body to pass on POST request. """
        return dumps(self.payload)

    def get_response(self) -> dict:
        """
        Try to fetch data from self.get_url and calling self._get_response_from_url for the complete response.
        On HttpError, if self.message_error_check is True we will try connect again more 5 times.
        Decompress the response.content
        """
        response = super().get_response()
        return loads(response.content)


class HttpSDKPOSTConnection(HttpPOSTCompressedConnection):

    is_json = BoolField(default=False, readonly=True)

    class_name = StrField()
    method_name = StrField()
    self_obj = DictField()
    params = DictField()

    def get_url(self) -> str:
        return f'{settings.EVERYSK_API_URL}/{settings.EVERYSK_SDK_VERSION}/{settings.EVERYSK_SDK_ROUTE}'

    def get_payload(self) -> dict:
        """ Make the correct payload body to pass on POST request. """
        self.payload = {
            'class_name': self.class_name,
            'method_name': self.method_name,
            'self_obj': self.self_obj,
            'params': self.params
        }
        return super().get_payload()

    def get_headers(self) -> dict:
        """ Headers needed to send HTTP Post methods. """
        headers = super().get_headers()
        everysk_api_sid = settings.EVERYSK_API_SID
        everysk_api_token = settings.EVERYSK_API_TOKEN

        if not everysk_api_sid:
            raise InvalidArgumentError('Invalid API SID')
        if not everysk_api_token:
            raise InvalidArgumentError('Invalid API TOKEN')

        headers['Authorization'] = f'Bearer {everysk_api_sid}:{everysk_api_token}'

        return headers
