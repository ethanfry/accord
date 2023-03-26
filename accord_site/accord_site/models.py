import uuid

from django.db import models

# Create your models here.

'''
boolean
char
date
datetime
decimal
duration
email
filepath
float
integer
biginteger
ipaddress
genericipaddress
nullboolean
positiveinteger
positivesmallinteger
slug
smallinteger
text
time
url
binary
uuid
'''

class Resource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    boolean_field = models.BooleanField(null=True)
    char_field = models.CharField(null=True, max_length=200)
    datetime_field = models.DateTimeField(null=True)
    text_field = models.TextField(null=True)


class RelatedResource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='related_resource')
    boolean_field = models.BooleanField()
    char_field = models.CharField(max_length=200)
    datetime_field = models.DateTimeField()
