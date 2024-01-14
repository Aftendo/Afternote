from django.db import models

# Create your models here.

class Flipnote(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    real_filename = models.CharField(max_length=24, null=False, unique=True)
    views = models.IntegerField(null=False, default=0)
    saved = models.IntegerField(null=False, default=0)
    def __str__(self):
        return self.real_filename