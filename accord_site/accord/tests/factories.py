import factory

from django.utils import timezone

from accord_site import models


class ResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Resource
    
    boolean_field = factory.Faker('boolean')
    char_field = factory.Faker('text')
    datetime_field = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())
    text_field = factory.Faker('text')


class RelatedResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.RelatedResource

    boolean_field = factory.Faker('boolean')
    char_field = factory.Faker('text')
    datetime_field = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())
    resource = factory.SubFactory(ResourceFactory)

