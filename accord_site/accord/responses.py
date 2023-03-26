import json
import uuid

from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, BadHeaderError


class JsonApiResponse(HttpResponse):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, content_type='application/vnd.api+json', **kwargs)


class UnknownRelationshipErrorResponse(JsonApiResponse):
    status_code = 404
    
    def __init__(self, model, related_field, self_link):
        super().__init__()
        
        response_dict = {
            'errors': [
                {
                    'id': str(uuid.uuid4()),
                    'links': {'self': self_link,},
                    'status': '404',
                    'title': 'Unknown Relationship Error',
                    'detail': f'Model {model} has no related field {related_field}'
                }
            ]
        }
        self.content = json.dumps(response_dict)
        
