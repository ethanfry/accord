from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, BadHeaderError
from django.shortcuts import get_object_or_404
from django.views import View

from .serializers import JsonApiSerializer

def list_view_factory(model_class):

    class ListView(View):

        # model = model_class

        def get(self, request, *args, **kwargs):
            queryset = None
            if 'id' in kwargs:
                queryset = model_class.objects.filter(pk=kwargs['id'])
                if not queryset.count():
                    return HttpResponseNotFound()
            else:
                queryset = model_class.objects.all()
            return HttpResponse(
                JsonApiSerializer().serialize(queryset=queryset, model_class=model_class), 
                content_type='application/vnd.api+json')

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
            return HttpResponse(serializers.serialize('jsonapi', self.model_class.objects.all()), content_type='application/vnd.api+json')

    return RelatedView
