from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,HttpResponseRedirect
from . import models
import json
import requests
from django.db.models import Q

# Create your views here.


@login_required
def myuser(request):
    if request.method == 'GET':
        datas = get_object_or_404(models.Yonghu,username=request.user.username)
        return render(request, 'keshihua/Status_record.html', locals())


@login_required
def myuser_update(request):
    if request.method == 'GET':
        datas = get_object_or_404(models.Yonghu,username=request.user.username)
        return render(request, 'keshihua/update_record.html', locals())
    elif request.method == 'POST':
        data = request.POST
        username = data.get('username','')
        email = data.get('email','')
        set= data.get('set','')
        age = data.get('age', '')

        if not username or not email or not set:
            datas = get_object_or_404(models.Yonghu, username=request.user.username)
            return render(request, 'keshihua/update_record.html', locals())
        test = get_object_or_404(models.Yonghu, username=request.user.username)
        test.username = username
        test.email = email
        test.age = age
        test.set = set
        test.save()

        return redirect('apps1:myuser')



@login_required
def fenxi(request):
    return render(request, 'keshihua/fenxi.html', locals())


@login_required
def pinglun(request):
    if request.method == 'GET':
        gjc = request.GET.get('gjc','')
        if gjc:
            results = models.Case_item.objects.filter(content__icontains=gjc)
        else:
            results = models.Case_item.objects.all()

        return render(request, 'keshihua/pinglun.html', locals())


import time
import datetime
@login_required
def tubiao(request):
    if request.method == 'GET':


        #饼图
        qingan_list = [{'value': len(models.Case_item.objects.filter(status='Positive')), 'name': '积极'},{'value': len(models.Case_item.objects.filter(status='Negative')), 'name': '消极'}
                       ,{'value': len(models.Case_item.objects.filter(status='Neutral')), 'name': '一般'}]

        #散点图
        results = models.Case_item.objects.all()
        list1 = [i.fabushijian.strftime('%Y-%m-%d %H') for i in results]
        print(list1)
        a = {}
        for ii in list(set(list1)):
            if a.get(ii, '') == '':
                a[int(time.mktime(datetime.datetime.strptime(ii, '%Y-%m-%d %H').timetuple()))] = list1.count(ii)

        list1 = sorted(a.items(), key=lambda item: item[0], reverse=True)
        nums = list1[-1][0]
        print(list1)

        list11 = []
        for key, value in list1:
            list22 = []
            list22.append(key - nums)
            list22.append(value)
            list22.append(value * 1000)

            timeArray = time.localtime(key)
            otherStyleTime = time.strftime(
                "%Y-%m-%d %H"
                , timeArray)
            list22.append(otherStyleTime)
            list22.append('微博数')
            list11.append(list22)
        list11.sort(key=lambda xx:xx[-2],reverse=False)

        #折线
        list1 = [i.fabushijian.strftime('%Y-%m-%d') for i in results]
        list2 = list(set(list1))
        list2.sort()

        date_name = []
        jiji_count = []
        xiaoji_count = []
        yiban_count = []
        for ii in list2:
            date_name.append(ii)
            da1 = models.Case_item.objects.filter(
                Q(fabushijian__day=datetime.datetime.strptime(ii, '%Y-%m-%d').day) & Q(status='Positive'))
            jiji_count.append(len(da1))
            da2 = models.Case_item.objects.filter(
                Q(fabushijian__day=datetime.datetime.strptime(ii, '%Y-%m-%d').day) & Q(status='Negative'))
            xiaoji_count.append(len(da2))
            da3 = models.Case_item.objects.filter(
                Q(fabushijian__day=datetime.datetime.strptime(ii, '%Y-%m-%d').day) & Q(
                    status='Neutral'))
            yiban_count.append(len(da3))

        #发布占比图
        results1 = models.Case_item.objects.all()
        da2 = [i.fabu_name for i in results1]
        name_count = []
        for resu in list(set(da2)):
            if da2.count(resu) > 5:
                name_count.append({"name": resu, "value": da2.count(resu)})




        return render(request, 'keshihua/tubiao.html', locals())

