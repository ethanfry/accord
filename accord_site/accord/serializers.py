"""
Serialize data to/from JSON
"""

from collections import OrderedDict
import datetime
import decimal
import json
import uuid

from django.core.serializers.base import DeserializationError, Serializer
from django.core.serializers.python import (
    Deserializer as PythonDeserializer, Serializer as PythonSerializer,
)
from django.core.serializers.json import Serializer as JSONSerializer
from django.utils.duration import duration_iso_string
from django.utils.encoding import is_protected_type
from django.utils.functional import Promise
from django.utils.timezone import is_aware


class JsonApiSerializer(JSONSerializer):

    def serialize(self, *args, **kwargs):
        data = {'data': None}
        queryset = kwargs['queryset']

        if queryset.count() == 1:
            data['data'] = self.serialize_instance(queryset[0])
        else:
            data['data'] = list()
            for el in queryset:
                data['data'].append(self.serialize_instance(el))
        return json.dumps(data)

    def serialize_instance(self, instance):
        retval = {'type': instance.__class__.__name__.lower(), 'id': str(instance.pk)}
        return retval


def Deserializer(stream_or_string, **options):
    """Deserialize a stream or string of JSON data."""
    if not isinstance(stream_or_string, (bytes, str)):
        stream_or_string = stream_or_string.read()
    if isinstance(stream_or_string, bytes):
        stream_or_string = stream_or_string.decode()
    try:
        objects = json.loads(stream_or_string)
        yield from PythonDeserializer(objects, **options)
    except (GeneratorExit, DeserializationError):
        raise
    except Exception as exc:
        raise DeserializationError() from exc


class DjangoJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time, decimal types, and
    UUIDs.
    """
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, datetime.timedelta):
            return duration_iso_string(o)
        elif isinstance(o, (decimal.Decimal, uuid.UUID, Promise)):
            return str(o)
        else:
            return super().default(o)
