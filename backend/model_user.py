from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    mail = models.CharField(max_length = 50)
    password = models.CharField(max_length = 100)
