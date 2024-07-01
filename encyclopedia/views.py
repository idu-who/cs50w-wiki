from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


@require_POST
def search(request):
    query = request.POST["q"].strip()

    if query in util.list_entries():
        return HttpResponseRedirect(
            reverse("entry", kwargs={"title": query})
        )
    else:
        return HttpResponseRedirect(
            reverse("search_results", kwargs={"query": query})
        )


def search_results(request, query):
    results = []

    for entry in util.list_entries():
        if entry.find(query) != -1:
            results.append(entry)

    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "results": results,
    })


def entry(request, title):
    context = {
        "title": title
    }

    content = util.get_entry(title)
    if not content:
        return render(request, "encyclopedia/error.html", context)

    context["content"] = content
    return render(request, "encyclopedia/entry.html", context)
