from django.test import tag, TestCase


class AccordTestCase(TestCase):

    # TODO: Fix object matching. right now Dates do not work
    def assertResponseMatchesDB(self, model_class, data_dict):
        self.assertIn('id', data_dict)
        instance = model_class.objects.get(pk=data_dict['id'])
        for key, val in data_dict['attributes'].items():
            if 'date' in key or 'time' in key:
                continue
            self.assertEqual(str(getattr(instance, key)), str(val))

    def assertIsValidJsonApiResponse(self, response):
        self.assertJsonapiMediaType(response)
        self.assertIsValidJsonApiDocument(response.json())

    def assertJsonapiMediaType(self, response):
        '''
        Per Section 5 (https://jsonapi.org/format/#jsonapi-media-type)
        Response must have a proper Content-Type header
        '''
        self.assertIn('Content-Type', response.headers)
        self.assertEqual('application/vnd.api+json', response.headers['Content-Type'])

    def assertIsValidJsonApiDocument(self, document):
        '''
        Per Section 7 (https://jsonapi.org/format/#document-structure),
        Each response body must be properly structured
        '''
        self.assertDocumentTopLevel(document)
    
    def assertDocumentTopLevel(self, document):
        '''
        Per Section 7.1 (https://jsonapi.org/format/#document-top-level)
         
            - A document MUST contain at least one of the following top-level members:
                data: the document’s “primary data”.
                errors: an array of error objects.
                meta: a meta object that contains non-standard meta-information.
                a member defined by an applied extension. (Accord currently does not make use of extensions)
        '''
        self.assertTrue(set(['data', 'errors', 'meta']).intersection(set(document.keys())))

        '''
            - The members data and errors MUST NOT coexist in the same document.
        '''
        self.assertFalse(set(['data', 'errors']).issubset(set(document.keys())))

        '''
            - A document MAY contain any of these top-level members:

                jsonapi: an object describing the server’s implementation.
                links: a links object related to the primary data.
                included: an array of resource objects that are related to the primary data and/or each other (“included resources”).
        '''
        self.assertTrue(set(document.keys()).issubset(set(['data', 'errors', 'meta', 'jsonapi', 'links', 'included'])))

        '''  
            - If a document does not contain a top-level data key, the included member MUST NOT be present either.
        '''
        self.assertFalse('included' in document and 'data' not in document)

        '''
            - The top-level links object MAY contain the following members:

                self: the link that generated the current response document. If a document has extensions or profiles applied to it, this link SHOULD be represented by a link object with the type target attribute specifying the JSON:API media type with all applicable parameters.
                related: a related resource link when the primary data represents a resource relationship.
                describedby: a link to a description document (e.g. OpenAPI or JSON Schema) for the current document.
                pagination links for the primary data.
                Note: The self link in the top-level links object allows a client to refresh the data 
                represented by the current response document. The client should be able to use the 
                provided link without applying any additional information. Therefore the link must contain 
                the query parameters provided by the client to generate the response document. This includes 
                but is not limited to query parameters used for [inclusion of related resources][fetching 
                resources], [sparse fieldsets][fetching sparse fieldsets], [sorting][fetching sorting], 
                [pagination][fetching pagination] and [filtering][fetching filtering].
        '''
        if 'links' in document:
            self.assertIsValidTopLevelLinks(document['links'])

        '''
            - The document’s “primary data” is a representation of the resource or collection of resources targeted by a request.
                Primary data MUST be either:
                    - a single resource object, a single resource identifier object, or null, for requests that target single resources
                    - an array of resource objects, an array of resource identifier objects, or an empty array ([]), for requests that target resource collections
        '''
        if 'data' in document:
            self.assertIsValidData(document['data'])

    # TODO: write this function
    def assertIsValidTopLevelLinks(self, links_dict):
        pass
    
    # TODO: write this function
    def assertIsValidData(self, data_dict):
        pass

    # def assertIsValidResourceObject(self, obj_dict):
    #     self.assertIsInstance(obj_dict, dict)
    #     self.assertIn('type', obj_dict)
    #     self.assertIn('id', obj_dict)
    #     self.assertIn('attributes', obj_dict)
    #     self.assertIn('relationships', obj_dict)
    #     model = getattr(models, obj_dict['type'].capitalize())
    #     field_names = set([field.name for field in model._meta.fields]) - set([model._meta.pk.name])
    #     self.assertEqual(set(obj_dict['attributes'].keys()), field_names)

    # def assertIsValidResourceIdentifier(self, obj_dict):
    #     pass

    # def assertIsValidResourceDataSingle(self, obj_dict):
    #     try:
    #         self.assertIsValidResourceObject(obj_dict)
    #     except AssertionError as e:
    #         try:
    #             self.assertIsValidResourceIdentifier(obj_dict)
    #         except AssertionError as e:
    #             self.assertIsNone(obj_dict)

    # def assertIsValidResourceDataArray(self, array):
    #     self.assertIsInstance(array, list)
    #     try:
    #         for el in array:
    #             self.assertIsValidResourceDataSingle(el)
    #     except AssertionError as e:
    #         for el in array:
    #             try:
    #                 self.assertIsValidResourceIdentifier(el)
    #             except AssertionError as e:
    #                 self.assertEqual(0, len(array))

    # def assertHasValidDataMember(self, dict):
    #     '''
    #     per https://jsonapi.org/format/#document-top-level
    #     We verify that we have a 'data' member
    #     and that we do not have an 'errors' member
    #     '''

    #     self.assertIn('data', dict)
    #     self.assertNotIn('errors', dict)
    #     try:
    #         self.assertIsValidResourceDataSingle(dict['data'])
    #     except AssertionError as e:
    #         self.assertIsValidResourceDataArray(dict['data'])

    # def assertHasValidLinksMember(self, dict):
    #     '''
    #     per https://jsonapi.org/format/#document-top-level
    #     Verify that we have a valid 'links' member

    #     Note: While the 'links' member is optional per the spec,
    #     we include it by default.
    #     '''
    #     self.assertIn('links', dict)


    # def assertHasValidErrorsMember(self, dict):
    #     self.assertIn('errors', dict)
    #     self.assertNotIn('data', dict)

    # def assertHasValidMetaMember(self, dict):
    #     self.assertIn('meta', dict)
