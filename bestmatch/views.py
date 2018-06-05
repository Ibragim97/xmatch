# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail

from math import ceil
import string
import random
import os
import math

from .models import Person


def get_photo_url(person):
    url = os.path.join(settings.MEDIA_ROOT, person.sex, person.photo.url)
    return url

def check_id(request):
    data = request.GET

    try:
        Person.objects.get(stud_id=data['id'])
        response = {'valid': True}
    except:
        response = {'notValid': "Не удалось найти человека по такому ID. Обратитесь по почте nu.bestmatch@gmail.com"}

    return JsonResponse(response)


def index(request):
    return render(request,'bestmatch/index.html')

def get_rand_person(sex):
    choice = random.randint(0, 2)

    all = Person.objects.filter(sex=sex)

    #beatiful
    if choice == 0:
        beatiful = all.order_by('-rating')[:300]
        ind = random.randint(0, beatiful.count() - 1)
        return beatiful[ind]

    # young genereation
    elif choice == 1:
        young = all.filter(Q(stud_id__startswith="2015") | Q(stud_id__startswith="2016"))
        ind = random.randint(0, young.count() - 1)
        return young[ind]

    #rare voted
    else:
        rare = all.order_by('rated_num')[:800]
        ind = random.randint(0, rare.count() - 1)
        return rare[ind]


def rating(request):

    key1 = 1000000007
    key2 = 1000000009

    def rand_str():
        return ''.join(random.choice(string.digits) for _ in range(4))    

    def clean_name(name):
        return name.replace('_', ' ')

    def encrypt(idx):
        idx = str((int(idx) + key2) ^ key1)
        return rand_str() + idx + rand_str()

    def decrypt(code):
        code = code[4:]
        code = code[:-4]
        return str((int(code) ^ key1) - key2)

    try:
        sex = request.POST['sex'][0]
    except:
        return HttpResponseRedirect('/')

    try:
        idx = decrypt(request.POST['token'])
        print idx
        person = Person.objects.get(stud_id=idx)
        rating_x = int(request.POST['rating'])
        rating_x = min(rating_x, 10)
        print '@'*80
        print person.name
        print person.rating
        print person.rated_num
        print '@'*80
        person.rating = (float(person.rating * person.rated_num) + float(rating_x)) / (float(person.rated_num) + float(1.0))
        person.rated_num += 1
        print '#'*80
        print person.name
        print person.rating
        print person.rated_num
        print '#'*80
        print "\n" * 2
        person.save()
    except:
        print "EXCEPTION"
        pass

    try:
        cnt = int(request.POST['cnt']) + 1
    except:
        cnt = 0

    try:
        rating_x = request.POST['rating']
    except:
        pass

    find = (cnt >= 5)

    random_person = get_rand_person(sex)

    content = {
        'find': find,
        'cnt': cnt,
        'name': clean_name(random_person.name),
        'url': get_photo_url(random_person),
        'sex': sex,
        'token': encrypt(random_person.stud_id),
    }

    return render(request,'bestmatch/rating.html', content)



def listPage(request):
    data = request.POST

    id = data['stud_id']

    person = Person.objects.get(stud_id=id)
    sex = person.sex

    numOfMales = Person.objects.filter(sex='M').count()
    numOfFemales = Person.objects.filter(sex='F').count()

    males = []
    m_places = []

    females = []
    f_places = []

    for i, female in enumerate(Person.objects.filter(sex='F').order_by('-rating')):
        females.append(female)
        f_places.append(i)

    for i, male in enumerate(Person.objects.filter(sex='M').order_by('-rating')):
        j = int(math.floor((i * 1.0/numOfMales)*numOfFemales))
        males.append(male)
        m_places.append(j)


    if sex == 'M':
        index = males.index(person)
        place = m_places[index]
        place_top = place * 100 / numOfMales

        if place == numOfFemales - 1:
            bestMatch_1 = females[place - 2]
            bestMatch_2 = females[place - 1]
            bestMatch_3 = females[place]
        elif place == 0:
            bestMatch_1 = females[place]
            bestMatch_2 = females[place + 1]
            bestMatch_3 = females[place + 2]
        else:
            bestMatch_1 = females[place - 1]
            bestMatch_2 = females[place]
            bestMatch_3 = females[place + 1]



    if sex == 'F':
        place = females.index(person)
        place_top = place * 100 / numOfFemales

        match_place1 = place - 1
        match_place2 = place
        match_place3 = place + 1
        if place == 0:
            match_place1 += 1
            match_place2 += 1
            match_place3 += 1
        if place == numOfFemales - 1:
            match_place1 -= 1
            match_place2 -= 1
            match_place3 -= 1

        index1 = m_places.index(match_place1)
        index2 = m_places.index(match_place2)
        index3 = m_places.index(match_place3)

        bestMatch_1 = males[index1]
        bestMatch_2 = males[index2]
        bestMatch_3 = males[index3]

    if place_top <= 10:
        place_top = 10
    elif place_top <= 30:
        place_top = 30
    else:
        place_top = None

    text = None

    if place_top:
        text = "Вы входите в  TOP-{0}%!".format(place_top)

    if person.stud_id == "":
            bestMatch_1 = bestMatch_2 = bestMatch_3 = Person.objects.get(stud_id="******")
            text = "Ты самая красивая в NU!"
            # try:
            send_mail(
                'BestMatch',
                '****** was visited',
                'nu.bestmatch@gmail.com',
                ['nu.bestmatch@gmail.com'],
                fail_silently=False,
            )
            # except:
                # print "Message was not sent"

    if id == "*******":
            bestMatch_1 = bestMatch_2 = bestMatch_3 = Person.objects.get(stud_id = "*******")
            text = "Что это мы здесь ищем??? У тебя есть парень, иди учиться!!!"
            # try:
            send_mail(
                'BestMatch',
                'nu.bestmatch@gmail.com',
                fail_silently=False,
            )



    content = {
        'text': text,
        'myname': person.name,
        'myurl': get_photo_url(person),

        'best1_name': bestMatch_1.name,
        'best1_url': get_photo_url(bestMatch_1),

        'best2_name': bestMatch_2.name,
        'best2_url': get_photo_url(bestMatch_2),

        'best3_name': bestMatch_3.name,
        'best3_url': get_photo_url(bestMatch_3),
    }

    return render(request,'bestmatch/list.html', content)



def top(request):
    males = Person.objects.filter(sex='M').order_by('-rating')[:10]
    females = Person.objects.filter(sex='F').order_by('-rating')[:10]

    pairs = zip(males, females)
    males = []
    females = []

    for m, f in pairs:
        males.append((m.name, get_photo_url(m)))
        females.append((f.name, get_photo_url(f)))
        print f


    content = {
        'males': males,
        'females': females,
    }

    return render(request, 'bestmatch/top.html', content)
