# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import datetime

from django.db import models

from schedule_match import settings

class Counter(models.Model):
    clicks = models.IntegerField(default=0)

class Session(models.Model):
    hashcode = models.CharField(max_length=50)
    created = models.DateTimeField()
    courses = models.TextField()
    numOfTables = models.IntegerField(default=0)

    @staticmethod
    def create_session(hashcode, courses):
        session = Session()
        session.hashcode = hashcode
        session.created = datetime.datetime.now()
        session.set_courses(courses)

        return session
    
    def set_courses(self, courses):
        self.courses = json.dumps(courses)

    def get_courses(self):
        return json.loads(self.courses)
        
    def __str__(self):
        return self.hashcode


class School(models.Model):
    name = models.CharField(max_length=50)
    last_modified = models.CharField(max_length=50)

    def __str__(self):
        return "%s - %s" % (self.name, self.last_modified)


class Subject(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE)

    abbr = models.CharField(max_length=50, verbose_name=u'Course Abbr')
    title = models.CharField(max_length=50, verbose_name=u'Course Title')
    credits = models.FloatField(max_length=20, default=3.0, verbose_name=u'Cr(US)')

    def __str__(self):
        return self.abbr


class SubjectInstance(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    section = models.CharField(max_length=10)
    days = models.CharField(max_length=10)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    faculty = models.CharField(max_length=50)
    room = models.CharField(max_length=50)

    def get_time(self):
        return "%s-%s" % (self.startTime.strftime("%H:%M"), self.endTime.strftime("%H:%M"))


    def __str__(self):
        return "%s %s"% (self.subject.abbr, self.section)