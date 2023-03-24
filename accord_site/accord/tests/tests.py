from django.test import tag

from accord import urls as accord_urls
from .factories import RelatedResourceFactory, ResourceFactory
from . import AccordTestCase


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

    @tag('my')
    def testResourceDetailWithRelatedResource(self):
        '''
        https://jsonapi.org/format/#document-resource-object-relationships
        '''
        resource = ResourceFactory.create()
        related_resources = RelatedResourceFactory(resource=resource)
        response = self.client.get(f'/api/resource/{str(resource.id)}')
        self.assertJSONAPIResponse(response)

        breakpoint()
        print('hi')
