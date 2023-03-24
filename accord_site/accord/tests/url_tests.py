from unittest import TestCase


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

