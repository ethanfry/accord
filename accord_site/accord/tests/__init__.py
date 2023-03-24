from django.test import tag, TestCase


class AccordTestCase(TestCase):

    def assertIsValidResourceObject(self, obj_dict):
        self.assertIsInstance(obj_dict, dict)
        self.assertIn('type', obj_dict)
        self.assertIn('id', obj_dict)
        self.assertIn('attributes', obj_dict)
        self.assertIn('relationships', obj_dict)
        model = getattr(models, obj_dict['type'].capitalize())
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

