from django.db import models

class Releve(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    temperature = models.IntegerField()