from django.db import models

from store.models import Product
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Tag(models.Model):
    lable = models.CharField(max_length=255)

class TaggedItem(models.Model):
    # what tag applies to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # poor way of doing this
    # product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    # generic way of doing this
    # this needs 3 fields 1. content_type, 2. object_id, 3. content_object
    # need Type (product, video, article), id of the object (1, 2, 3) adn content object (actual object)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()  # content_type, object_id