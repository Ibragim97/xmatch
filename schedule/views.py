# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import random
import string 

from django.shortcuts import render, reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic.base import TemplateView

from .utils import generate, deleteTables, refresh_data
from .forms import SubjectsForm
from .models import School, Counter, Subject, Session
from schedule_match import settings


def index(request):
    return HttpResponse("Hello, World!")

class SubjectsView(TemplateView):
    template_name = 'schedule/index.html'

    def get(self, request, *args):
        form = SubjectsForm()
        deleteTables()
        # try:
        date = School.objects.get(name="SST").last_modified
        
        return render(request, self.template_name, {'form': form, 'date': date})

    def post(self, request):

        def gen_hashcode():
            return ''.join(random.choice(string.digits) for _ in range(8))

        data = request.POST
        form = SubjectsForm(data)

        if form.is_valid():
            courses = []
            for field in data:
                if field.startswith('sub_abbr'):
                    if data[field]: 
                        courses.append(data[field].upper())

            while True:
                hashcode = gen_hashcode()
                try: 
                    Session.objects.get(hashcode=hashcode)
                except:
                    newSession = Session.create_session(hashcode=hashcode, courses=courses)
                    newSession.save()
                    break

            return HttpResponseRedirect(
                    reverse('schedule:table',
                            kwargs={'hashcode': hashcode}))
        else:
            return render(request, self.template_name, {'form': form})
        

class TableView(TemplateView):
    template_name = 'schedule/table.html'

    def get(self, request, *args, **kwargs):
        try:
            counter = Counter.objects.get(pk=1)
            counter.clicks += 1
            counter.save()
        except:
            print "Counter is not working"

        hashcode = kwargs.get('hashcode')
        page = request.GET.get('page')
        try:
            session = Session.objects.get(hashcode=hashcode)
        except:
            return HttpResponse("Session expired.")
        courses = session.get_courses()
        print "HERE1"
        tables = generate(hashcode=hashcode, courses=courses)
        # tables = generate(hashcode=hashcode)
        print "HERE2"
        session = Session.objects.get(hashcode=hashcode)
        size = session.numOfTables
        data = {
            'tables': tables,
            'size': size,
            'hashcode': hashcode,
        }
        
        return render(request, self.template_name, data)

class DownloadView(TemplateView):

    def get(self, request, *args, **kwargs):
        hashcode = kwargs.get('hashcode')
        page = int(request.GET.get('page'))
        page -= 1
        
        filename = 'table_%s_%s.xlsx' % (hashcode, page)
        file_path = os.path.join(settings.TABLES_DIR, filename)

        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=%s' % os.path.basename(file_path)
                return response
        raise Http404


def get_subjects(request):
    data = {
        'subjects': [(x.abbr, x.title, x.credits) for x in Subject.objects.all()]
    }
    return JsonResponse(data)

def refresh(request):
    try:
        refresh_data()
    except:
        return HttpResponse("Error...");
    else:
        return HttpResponse("Data refreshed");
