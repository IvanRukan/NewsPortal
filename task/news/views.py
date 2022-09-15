import json

from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.http import HttpResponse
from .forms import NewsForm
import datetime
import random


def creator(text, title):
    global data
    new = data
    dictionary = {'created':  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'text': text, 'title': title,
                  'link': random.randint(10, 8000)}
    new.append(dictionary)
    with open('A:\\soft\\django_projects\\HyperNews Portal\\HyperNews Portal\\task\\hypernews\\news.json', 'w') as file:
        json.dump(new, file)


with open('A:\\soft\\django_projects\\HyperNews Portal\\HyperNews Portal\\task\\hypernews\\news.json', 'r') as json_file:
    data = json.load(json_file)


def sorter(data, query=None):
    dates = []
    for date in data:
        dates.append(date['created'].split()[0])
    dates = set(dates)
    dates = [date.split('-') for date in dates]
    sorted_dates = [datetime.datetime(int(date[0]), int(date[1]), int(date[2])).date() for date in dates]
    sorted_dates = sorted(sorted_dates, reverse=True)
    sorted_dates = [str(date) for date in sorted_dates]
    new_data = {key: [] for key in sorted_dates}
    for key in new_data:
        for date in data:
            if date['created'].split()[0] == key:
                temp = []
                temp.append(date['link'])
                temp.append(date['title'])
                new_data[key].append(temp)
    if query:
        result = {}

        for key, title in new_data.items():
            search_result = []
            for each in title:
                if query in each[1]:
                    search_result.append(each)
            if search_result:
                result[key] = search_result
        if not result:
            return None
        return result
    return new_data


class NewsPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/main_copy.html', context={'articles': sorter(data, request.GET.get('q'))})


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class StoryView(View):
    def get(self, request, id):
        for each in data:
            if each['link'] == id:
                created = each['created']
                text = each['text']
                title = each['title']
        return render(request, 'news/story_view.html', context={'title': title, 'date': created, 'text': text})


class CreatorView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')

    def post(self, request):
        form = NewsForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            title = form.cleaned_data.get('title')
            creator(text, title)
        return redirect('/news/')
