from django.db import models

class Translation(models.Model):
    input_text = models.CharField(max_length=500)
    output_text = models.CharField(max_length=500, null=True, blank=True)
# Create your models here.
