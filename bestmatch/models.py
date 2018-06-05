# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=30)
    sex = models.CharField(max_length=1)
    photo = models.ImageField(upload_to=None, blank=True, null=True)
    stud_id = models.CharField(max_length=10)
    rating = models.DecimalField(max_digits=10, decimal_places=5, default = 0)
    rated_num = models.DecimalField(max_digits=1000000, decimal_places=1,default=0)

    def __str__(self):
        return '{}: {}'.format(self.name, self.sex)

