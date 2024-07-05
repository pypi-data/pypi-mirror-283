###############################################################################
#
# (C) Copyright 2024 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
__all__ = ['dumps', 'loads']
import json
import pickle
from typing import Any

from everysk.config import settings
from everysk.core.datetime import DateTime, Date
from everysk.core.undefined import UndefinedType


class JSONEncoder(json.JSONEncoder):

    def __init__(self, **kwargs) -> None:
        # Set specific params
        self.date_format = kwargs.pop('date_format', None) or settings.SERIALIZE_DATE_FORMAT
        self.datetime_format = kwargs.pop('datetime_format', None) or settings.SERIALIZE_DATETIME_FORMAT
        self.use_undefined = kwargs.pop('use_undefined', False) or settings.SERIALIZE_USE_UNDEFINED

        # Set all default params
        super().__init__(**kwargs)

    def undefined_to_dict(self, obj) -> dict[str, None] | None: # pylint: disable=unused-argument
        """
        Convert an Undefined object to a string or None.
        If `self.use_undefined` is set to True, it returns the default parse string of the Undefined object.

        Args:
            obj (UndefinedType): The Undefined object to convert to a string.
        """
        if self.use_undefined:
            return {settings.SERIALIZE_UNDEFINED_KEY: None}

        return None

    def convert_date(self, obj: Date) -> dict[str, str] | str:
        """
        Convert a Date object to a dict or string.
        If `self.date_format` is set the result will be a string in this format
        otherwise the result will be a dict with the Date as isoformat.

        Args:
            obj (Date): The Date object to convert to a string or dict.
        """
        if self.date_format:
            return obj.strftime(self.date_format)

        return {settings.SERIALIZE_DATE_KEY: obj.isoformat()}

    def convert_datetime(self, obj: DateTime) -> dict[str, str] | str:
        """
        Convert a DateTime object to a dict or string.
        If `self.datetime_format` is set the result will be a string in this format
        otherwise the result will be a dict with the DateTime as isoformat.

        Args:
            obj (DateTime): The DateTime object to convert to a string.
        """
        if self.datetime_format:
            return obj.strftime(self.datetime_format)

        return {settings.SERIALIZE_DATETIME_KEY: obj.isoformat()}

    def default(self, obj: Any) -> dict | None: # pylint: disable=arguments-renamed
        """
        Convert an object to a JSON serializable format.

        Args:
            obj (Any): The object to convert to a JSON serializable format.
        """
        if Date.is_date(obj):
            return self.convert_date(obj)

        if DateTime.is_datetime(obj):
            return self.convert_datetime(obj)

        if obj is Undefined:
            return self.undefined_to_dict(obj)

        return super().default(obj)


class JSONDecoder(json.JSONDecoder):

    def __init__(self, **kwargs) -> None:
        # Set specific params
        self.date_format = kwargs.pop('date_format', None) or settings.SERIALIZE_DATE_FORMAT
        self.datetime_format = kwargs.pop('datetime_format', None) or settings.SERIALIZE_DATETIME_FORMAT
        self.use_undefined = kwargs.pop('use_undefined', False) or settings.SERIALIZE_USE_UNDEFINED
        if 'object_hook' not in kwargs or kwargs['object_hook'] is None:
            kwargs['object_hook'] = self.custom_object_hook

        # Set all default params
        super().__init__(**kwargs)

    def str_to_date(self, obj: str) -> Date:
        """
        Convert a string to a Date object.
        If `self.date_format` is set, it uses the specified date format to convert the string to a Date object.

        Args:
            obj (str): The string to convert to a Date object.
        """
        if self.date_format:
            return Date.strptime(obj, self.date_format)

        return Date.fromisoformat(obj)

    def str_to_datetime(self, obj: str) -> DateTime:
        """
        Convert a string to a DateTime object.
        If `self.datetime_format` is set, it uses the specified datetime format to convert the string to a DateTime object.

        Args:
            obj (str): The string to convert to a DateTime object.
        """
        if self.datetime_format:
            return DateTime.strptime(obj, self.datetime_format)

        return DateTime.fromisoformat(obj)

    def str_to_undefined(self, obj: str) -> UndefinedType | None: # pylint: disable=unused-argument
        """
        Convert a string to Undefined object, if `self.use_undefined` is set to True, otherwise return None.

        Args:
            obj (str): The string to convert to a Undefined object.
        """
        if self.use_undefined:
            return Undefined

        return None

    def custom_object_hook(self, obj: dict) -> UndefinedType | None | Date | DateTime:
        """
        We change the default object hook to handle custom object hooks for date, datetime and Undefined objects.

        Args:
            obj (dict): A dictionary object to convert to check and convert.
        """
        if settings.SERIALIZE_DATE_KEY in obj:
            return self.str_to_date(obj[settings.SERIALIZE_DATE_KEY])

        if settings.SERIALIZE_DATETIME_KEY in obj:
            return self.str_to_datetime(obj[settings.SERIALIZE_DATETIME_KEY])

        if settings.SERIALIZE_UNDEFINED_KEY in obj:
            return self.str_to_undefined(obj[settings.SERIALIZE_UNDEFINED_KEY])

        return obj


def dumps(
    obj: Any,
    *, # Limits that only named arguments can be passed after this
    allow_nan: bool = True,
    check_circular: bool = True,
    cls: type = JSONEncoder,
    date_format: str = settings.SERIALIZE_DATE_FORMAT,
    datetime_format: str = settings.SERIALIZE_DATETIME_FORMAT,
    default: callable = None,
    ensure_ascii: bool = True,
    indent: int = None,
    protocol: str = 'json',
    separators: tuple = None,
    skipkeys: bool = False,
    sort_keys: bool = False,
    use_undefined: bool = settings.SERIALIZE_USE_UNDEFINED
) -> str | bytes:
    """
    Serialize `obj` to a JSON/Pickle formatted `str`.

    If `allow_nan` is false, then it will be a `ValueError` to
    serialize out of range `float` values (`nan`, `inf`, `-inf`) in
    strict compliance of the JSON specification, instead of using the
    JavaScript equivalents (`NaN`, `Infinity`, `-Infinity`).

    If `check_circular` is false, then the circular reference check
    for container types will be skipped and a circular reference will
    result in an `RecursionError` (or worse).

    The date_format and datetime_format parameters can be used to specify the
    date and datetime formats to use when serializing date and datetime objects.
    If not specified, the default ISO format is used.

    If `ensure_ascii` is false, then the return value can contain non-ASCII
    characters if they appear in strings contained in `obj`. Otherwise, all
    such characters are escaped in JSON strings.

    If `indent` is a non-negative integer, then JSON array elements and
    object members will be pretty-printed with that indent level. An indent
    level of 0 will only insert newlines. `None` is the most compact
    representation.

    The protocol argument defines the encoding protocol to use. By default, it is 'json'
    and at the moment we only support json and pickle.

    If specified, `separators` should be an `(item_separator, key_separator)`
    tuple.  The default is `(', ', ': ')` if *indent* is `None` and
    `(',', ': ')` otherwise.  To get the most compact JSON representation,
    you should specify `(',', ':')` to eliminate whitespace.

    `default(obj)` is a function that should return a serializable version
    of obj or raise TypeError. The default simply raises TypeError.

    If *sort_keys* is true (default: `False`), then the output of
    dictionaries will be sorted by key.

    To use a custom `JSONEncoder` subclass (e.g. one that overrides the
    `.default()` method to serialize additional types), specify it with
    the `cls` kwarg; otherwise `JSONEncoder` is used.

    If `skipkeys` is true then `dict` keys that are not basic types
    (`str`, `int`, `float`, `bool`, `None`) will be skipped
    instead of raising a `TypeError`.

    The `use_undefined` parameter can be used to serialize `Undefined` objects
    as a string. If set to True, the default parse string of the `Undefined` object is used.
    Otherwise, `Undefined` objects are serialized as `None`.
    """
    if protocol == 'json':
        if isinstance(obj, bytes):
            obj = obj.decode(json.detect_encoding(obj))

        return json.dumps(
            obj, allow_nan=allow_nan, check_circular=check_circular, cls=cls, date_format=date_format,
            datetime_format=datetime_format, default=default, ensure_ascii=ensure_ascii, indent=indent,
            separators=separators, skipkeys=skipkeys, sort_keys=sort_keys, use_undefined=use_undefined
        )
    if protocol == 'pickle':
        return pickle.dumps(obj)

    raise ValueError(f"Unsupported serialize protocol '{protocol}'. Use 'json' or 'pickle'.")

def loads(
    string: str | bytes | bytearray,
    *, # Limits that only named arguments can be passed after this
    cls: type = JSONDecoder,
    date_format: str = settings.SERIALIZE_DATE_FORMAT,
    datetime_format: str = settings.SERIALIZE_DATETIME_FORMAT,
    object_hook: callable = None,
    object_pairs_hook: callable = None,
    parse_constant: callable = None,
    parse_float: callable = None,
    parse_int: callable = None,
    protocol: str = 'json',
    use_undefined: bool = settings.SERIALIZE_USE_UNDEFINED,
    **kwargs
) -> Any:
    """
    Deserialize ``string`` (a ``str``, ``bytes`` or ``bytearray`` instance
    containing a JSON/Pickle document) to a Python object.

    ``object_hook`` is an optional function that will be called with the
    result of any object literal decode (a ``dict``). The return value of
    ``object_hook`` will be used instead of the ``dict``. This feature
    can be used to implement custom decoders (e.g. JSON-RPC class hinting).

    ``object_pairs_hook`` is an optional function that will be called with the
    result of any object literal decoded with an ordered list of pairs.  The
    return value of ``object_pairs_hook`` will be used instead of the ``dict``.
    This feature can be used to implement custom decoders.  If ``object_hook``
    is also defined, the ``object_pairs_hook`` takes priority.

    ``parse_float``, if specified, will be called with the string
    of every JSON float to be decoded. By default this is equivalent to
    float(num_str). This can be used to use another datatype or parser
    for JSON floats (e.g. decimal.Decimal).

    ``parse_int``, if specified, will be called with the string
    of every JSON int to be decoded. By default this is equivalent to
    int(num_str). This can be used to use another datatype or parser
    for JSON integers (e.g. float).

    ``parse_constant``, if specified, will be called with one of the
    following strings: -Infinity, Infinity, NaN.
    This can be used to raise an exception if invalid JSON numbers
    are encountered.

    The protocol argument defines the encoding protocol to use. By default, it is 'json'
    and at the moment we only support json and pickle.

    To use a custom ``JSONDecoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``JSONDecoder`` is used.
    """
    if protocol == 'json':
        if isinstance(string, bytes):
            string = string.decode(json.detect_encoding(string))

        return json.loads(
            string, cls=cls, date_format=date_format, datetime_format=datetime_format, object_hook=object_hook,
            object_pairs_hook=object_pairs_hook, parse_constant=parse_constant, parse_float=parse_float,
            parse_int=parse_int, use_undefined=use_undefined, **kwargs
        )

    if protocol == 'pickle':
        return pickle.loads(string)

    raise ValueError(f"Unsupported serialize protocol '{protocol}'. Use 'json' or 'pickle'.")
