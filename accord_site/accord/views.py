from django.core import serializers
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views import View

import json

from .responses import JsonApiResponse, UnknownRelationshipErrorResponse
from .serializers import JsonApiSerializer


def list_view_factory(model_class):

    class ListView(View):

        # model = model_class

        def get(self, request, *args, **kwargs):
            queryset = None
            filters = Q()
            if 'id' in kwargs:
                filters &= Q(pk=kwargs['id'])
            queryset = model_class.objects.filter(filters)
            if includes := request.GET.get('include'):
                # breakpoint()
                # User includes related fields by adding ?include=related_1,related_2,...,related_n
                for include in includes.split(','):
                    queryset = queryset.prefetch_related(include)
            try:
                data = json.loads(JsonApiSerializer().serialize(queryset))
                if isinstance(data, list) and len(data) == 1:
                    data = data[0]
                body = {
                    'data': data,
                    'links': {'self': request.build_absolute_uri()},
                }
                return JsonApiResponse(json.dumps(body))
            except AttributeError as e:
                response = UnknownRelationshipErrorResponse(
                    model=model_class.__name__, 
                    related_field='foo', 
                    self_link=request.build_absolute_uri()
                )
                return response

    return ListView


def related_view_factory(model_class, related_model_class):
    '''
    These views handle the following JSONAPI endpoints:

    Related resource detail
    GET /<model_name>/<model_instance_id>/<related_model_name> HTTP/1.1

    Relationship data
    GET /<model_name>/<model_instance_id>/relationships/<related_model_name> HTTP/1.1

    :param model_class: This is the base model class
    :param related_model_class: This is the related model class
    :return:
    '''

    class RelatedView(View):
        # related_field_name = related_field_name

        def get(self, request, *args, **kwargs):
            return JsonApiResponse(serializers.serialize('jsonapi', self.model_class.objects.all()))

    return RelatedView
