from django.db import models
from django.utils import timezone

# Create your models here.

class Feedback(models.Model):
    data = models.DateTimeField(blank = True)
    result = models.CharField(max_length = 3, null=True)

    def store(self):
        self.data = timezone.now()
        self.save()

class Document(models.Model):
    upload = models.FileField()