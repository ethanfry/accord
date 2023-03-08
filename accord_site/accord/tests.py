from django.test import TestCase
from django.utils import timezone

import factory

from accord import urls as accord_urls
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


class AccordTestCase(TestCase):

    def assertIsValidResourceObject(self, obj_dict):
        self.assertIsInstance(obj_dict, dict)
        self.assertIn('type', obj_dict)
        self.assertIn('id', obj_dict)

    def assertResourceObjectContainsAttributes(self, obj_dict, model):
        self.assertIn('attributes', obj_dict)
        field_names = set([field.name for field in model._meta.fields]) - set([model._meta.pk.name])
        self.assertEqual(set(obj_dict['attributes'].keys()), field_names)

    def assertIsValidResourceIdentifier(self, obj_dict):
        pass

    def assertIsValidResourceDataSingle(self, obj_dict):
        try:
            self.assertIsValidResourceObject(obj_dict)
        except AssertionError as e:
            try:
                self.assertIsValidResourceIdentifier(obj_dict)
            except AssertionError as e:
                self.assertIsNone(obj_dict)

    def assertIsValidResourceDataArray(self, array):
        self.assertIsInstance(array, list)
        try:
            for el in array:
                self.assertIsValidResourceDataSingle(el)
        except AssertionError as e:
            for el in array:
                try:
                    self.assertIsValidResourceIdentifier(el)
                except AssertionError as e:
                    self.assertEqual(0, len(array))

    def assertHasValidDataMember(self, dict):
        '''
        per https://jsonapi.org/format/#document-top-level
        We verify that we have a 'data' member
        and that we do not have an 'errors' member
        '''

        self.assertIn('data', dict)
        self.assertNotIn('errors', dict)
        try:
            self.assertIsValidResourceDataSingle(dict['data'])
        except AssertionError as e:
            self.assertIsValidResourceDataArray(dict['data'])

    def assertHasValidLinksMember(self, dict):
        '''
        per https://jsonapi.org/format/#document-top-level
        Verify that we have a valid 'links' member

        Note: While the 'links' member is optional per the spec,
        we include it by default.
        '''
        self.assertIn('links', dict)


    def assertHasValidErrorsMember(self, dict):
        self.assertIn('errors', dict)
        self.assertNotIn('data', dict)

    def assertHasValidMetaMember(self, dict):
        self.assertIn('meta', dict)

    def assertJSONAPIResponse(self, response):
        self.assertIn('Content-Type', response.headers)
        self.assertEqual('application/vnd.api+json', response.headers['Content-Type'])
        body = response.json()
        self.assertHasValidLinksMember(body)
        try:
            self.assertHasValidDataMember(body)
        except AssertionError as e:
            try:
                self.assertHasValidErrorsMember(body)
            except AssertionError as e:
                self.assertHasValidMetaMember(body)


class URLTestCase(TestCase):
    '''
    At this point, we have the following models:
    MyResource
    MyRelatedResource

    Because Resource is a FK on RelatedResource, we should have a bunch of URLs out of the box
    '''

    def testResourceUrls(self):
        self.assertIn('resource_list', [url.name for url in accord_urls.urlpatterns])
        self.assertIn('resource_detail', [url.name for url in accord_urls.urlpatterns])
        self.assertIn('resource_relatedresource_related', [url.name for url in accord_urls.urlpatterns])

    def testRelatedResourceUrls(self):
        self.assertIn('relatedresource_list', [url.name for url in accord_urls.urlpatterns])
        self.assertIn('relatedresource_detail', [url.name for url in accord_urls.urlpatterns])
        self.assertIn('relatedresource_resource_related', [url.name for url in accord_urls.urlpatterns])


class ResourceResponseTestCase(AccordTestCase):
    '''
    Verify responses for /resource endpoints
    '''

    def testResourceListResponse(self):
        resources = ResourceFactory.create_batch(10)
        response = self.client.get('/api/resource')
        self.assertJSONAPIResponse(response)
        self.assertEqual(10, len(response.json()['data']))

    def testResourceDetailResponse(self):
        resources = ResourceFactory.create_batch(10)
        response = self.client.get(f'/api/resource/{str(resources[0].id)}')
        self.assertJSONAPIResponse(response)
        self.assertIsInstance(response.json()['data'], dict)
        self.assertResourceObjectContainsAttributes(response.json()['data'], models.Resource)

    def testResourceDetailWithRelatedResource(self):
        pass