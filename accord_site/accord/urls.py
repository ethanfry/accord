import inspect
import sys
import pprint

from django.conf import settings
from django.db.models.fields import related_descriptors
from django.urls import include, path


# relationship_classes are classes defined in django.db.models.fields that represent relationships
# between models. They are:
#   ForeignKeyDeferredAttribute
#   ForwardManyToOneDescriptor
#   ForwardOneToOneDescriptor
#   ManyToManyDescriptor
#   ReverseManyToOneDescriptor
#   ReverseOneToOneDescriptor
#  We will use these to create views for related entities, per the JSON API spec
relationship_classes = {thing[0]:thing[1] for thing in inspect.getmembers(sys.modules['django.db.models.fields.related_descriptors'], inspect.isclass) if inspect.getmodule(thing[1]) is related_descriptors}
relationship_classes.pop('ForeignKeyDeferredAttribute')
models = getattr(__import__(settings.ACCORD['MODELS_APP']), 'models')
from . import views


urlpatterns = []

'''
JSONAPI endpoints

Resource views:

Resource list
GET /<model_name>

Resource detail
GET /<model_name>/<model_instance_id>

Related resource detail
GET /<model_name>/<model_instance_id>/<related_model_name> HTTP/1.1


For each model in our domain, we are going to create resource views. 
Each model will have a resource list view, and a resource detail view.
We will handle these each on a single view for simplicity

'''
# This loop iterates on models in our models module
# (based on https://jsonapi.org/format/#fetching-resources)
# It adds the following routes:
#    - /<model_name>
#    - /<model_name>/<model_instance_id>
#    For each related model:
#      - /<model_name>/<model_instance_id>/<related_model_name>

for model in [m for m in inspect.getmembers(models, inspect.isclass) if m[1].__module__ == f'{settings.ACCORD["MODELS_APP"]}.models']:
    print(f'Adding urls for model {model}')
    model_name = model[0] # The name of the model
    model_class = model[1] # The model class (not the name of the class, the class)

    # the model view is named for the model
    view_name = f'{model_name}View'

    # we generate a view class using a factory.
    model_view = views.list_view_factory(model_class)

    # We add that model view class back into the views module
    setattr(views, view_name, model_view)

    # Add the list view for all instances of a resource
    print(f'adding view for model {model_name.lower()} at path {model_name.lower()}')
    urlpatterns.append(
        path(
            model_name.lower(), 
            model_view.as_view(), 
            name=f'{model_name.lower()}_list'))

    # add the Resource Detail View to urls
    print(f'adding view for model {model_name.lower()} at path {model_name.lower()}/<uuid:id>')
    urlpatterns.append(
        path(
            f'{model_name.lower()}/<uuid:id>', 
            model_view.as_view(), 
            name=f'{model_name.lower()}_detail'))

    # # We also need to add views for all of the related resources (foreign keys and such)
    related_field_names = [attr for attr in dir(model_class) if getattr(model_class, attr).__class__.__name__ in relationship_classes]

    for related_field_name in related_field_names:
        relationship_descriptor = getattr(model_class, related_field_name)
        if hasattr(relationship_descriptor, 'rel'):
            related_model_class = getattr(model_class, related_field_name).rel.related_model
        else:
            related_model_class = getattr(model_class, related_field_name).field.related_model

        # create the view for the related model
        related_view = views.related_view_factory(model_class, related_model_class)

        # add the view to views
        setattr(views, view_name, related_view)

        # Add a URL for the view
        print(f'adding path for related field {related_field_name} at {model_name.lower()}/<uuid:id>/{related_model_class.__name__.lower()}')
        urlpatterns.append(
            path(
                f'{model_name.lower()}/<uuid:id>/{related_model_class.__name__.lower()}', 
                related_view.as_view(),
                name=f'{model_name.lower()}_{related_model_class.__name__.lower()}_related')),
