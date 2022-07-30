from genericpath import exists
from random import randint
from urllib.error import URLError
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import NoReverseMatch
from . import models
from . import util
from django.core.files.storage import default_storage


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def create(request):
    if request.method == "POST":
        form = models.WikiPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
    return render(request, "encyclopedia/create.html", {
        "form": models.WikiPageForm()
    })


def pages(request, title):
    entry_list = util.list_entries()
    if title in entry_list:
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "content": util.get_entry(title)
        })
    else:
        return render(request, "encyclopedia/404.html", {})


def randomPage(request):
    title = util.list_entries()[randint(0, len(util.list_entries()) - 1)]
    return render(request, "encyclopedia/random.html", {
        "title": title,
        "content": util.get_entry(title)
    })


def searchPage(request):
    search = request.GET.get("q", "")
    titles = util.list_entries()
    found = [i for i in titles if search.lower() in i.lower()]
    if len(found) != 0:
        return render(request, "encyclopedia/search.html", {
            "title": found[0],
            "content": util.get_entry(found[0])
        })
    return render(request, "encyclopedia/search.html", {
        "title": "None",
        "content": "No Content"
    })


def error_404_view(request, exception):
    data = {}
    return render(request,'encyclopedia/404.html', data)


def edit(request, title):
    if request.method == "POST":
        form = models.WikiPageForm(request.POST)
        if form.is_valid():
            # save and then replace
            new_title = form.cleaned_data["title"]
            new_content = form.cleaned_data["content"]
            util.save_entry(new_title, new_content)
            delete(title)
            return redirect("/")

    return render(request, "encyclopedia/edit.html", {"title": title, "form": models.WikiPageForm()})


def delete(title):
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
