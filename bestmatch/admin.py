# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Person


class Admin(admin.ModelAdmin):
    list_display = ('name', 'rating')
    search_fields = ('stud_id', 'firstName')


admin.site.register(Person, Admin),

