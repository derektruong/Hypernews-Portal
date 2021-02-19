from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.http import HttpResponse
import datetime
import random
import json
import os

# Create your views here.


class MainPage(View):
    @staticmethod
    def get(request, *args, **kwargs):
        return redirect('/news/')


class News(View):
    def get(self, request, *args, **kwargs):
        key = str(request.GET.get('q')).lower() if request.GET.get('q') else ""
        news_json_path = os.path.join(settings.BASE_DIR, '../', settings.NEWS_JSON_PATH)
        with open(news_json_path, 'r') as file:
            data = json.load(file)

        filter_data = []

        for ele in data:
            if key in ele['title'].lower():
                filter_data.append(ele)
        created_list = set([val['created'][:10].replace('-', '') for val in filter_data])
        created_list = sorted(created_list, reverse=True)

        for ind in range(len(created_list)):
            created_list[ind] = created_list[ind][:4] + '-' + created_list[ind][4:6] + '-' + created_list[ind][6:]
        if key != "":
            context = {"data": filter_data, "created_list": created_list}
        else:
            context = {"data": data, "created_list": created_list}
        return render(request, "news/news.html", context=context)


class NewPost(View):
    @staticmethod
    def get(request, post_id, *args, **kwargs):
        dic = {}
        news_json_path = os.path.join(settings.BASE_DIR, '../', settings.NEWS_JSON_PATH)
        with open(news_json_path, 'r') as file:
            data = json.load(file)
        for i in data:
            if i['link'] == post_id:
                dic = i
                break
        context = {"data": dic}
        return render(request, "news/index.html", context=context)


class CreatePost(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/create_post.html")

    def post(self, request, *args, **kwargs):
        news_json_path = os.path.join(settings.BASE_DIR, '../', settings.NEWS_JSON_PATH)
        with open(news_json_path, 'r') as file_json:
            data = json.load(file_json)
        created = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        link = random.randint(10, 100000000000)
        title = request.POST.get('title')
        text = request.POST.get('text')
        data.append(
            {
                "created": created,
                "text": text,
                "title": title,
                "link": link
            }
        )
        with open(news_json_path, 'w') as file_json:
            json.dump(data, file_json, indent=4)
        return redirect('/news/')


