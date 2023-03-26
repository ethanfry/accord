from django.test import tag

from .factories import RelatedResourceFactory, ResourceFactory
from . import AccordTestCase


class ResourceResponseTestCase(AccordTestCase):
    '''
    Verify responses for /resource endpoints
    '''

    def testResourceListResponse(self):
        resources = ResourceFactory.create_batch(10)
        response = self.client.get('/api/resource')
        self.assertIsValidJsonApiResponse(response)
        self.assertEqual(10, len(response.json()['data']))
        for item in response.json()['data']:
            self.assertResponseMatchesDB(ResourceFactory._meta.get_model_class(), item)

    def testResourceDetailResponse(self):
        resources = ResourceFactory.create_batch(10)
        response = self.client.get(f'/api/resource/{str(resources[0].id)}')
        self.assertIsValidJsonApiResponse(response)
        self.assertResponseMatchesDB(ResourceFactory._meta.get_model_class(), response.json()['data'])

    def testResourceDetailWithRelatedResourceWithoutRelatedFlag(self):
        '''
        https://jsonapi.org/format/#document-resource-object-relationships
        '''
        resource = ResourceFactory.create()
        related_resources = RelatedResourceFactory(resource=resource)
        response = self.client.get(f'/api/resource/{str(resource.id)}')
        self.assertIsValidJsonApiResponse(response)

    @tag('my')
    def testResourceDetailWithRelatedResourceWithRelatedFlag(self):
        '''
        https://jsonapi.org/format/#document-resource-object-relationships
        '''
        resource = ResourceFactory.create()
        related_resources = RelatedResourceFactory(resource=resource)
        response = self.client.get(f'/api/resource/{str(resource.id)}?include=related_resource')
        self.assertIsValidJsonApiResponse(response)

    def testResourceDetailWithRelatedResourceWithUnknownRelatedFlag(self):
        '''
        https://jsonapi.org/format/#document-resource-object-relationships
        '''
        resource = ResourceFactory.create()
        related_resources = RelatedResourceFactory(resource=resource)
        response = self.client.get(f'/api/resource/{str(resource.id)}?include=foo')
        self.assertIsValidJsonApiResponse(response)
        self.assertIn('errors', response.json())
        self.assertEqual('Unknown Relationship Error', response.json()['errors'][0]['title'])

