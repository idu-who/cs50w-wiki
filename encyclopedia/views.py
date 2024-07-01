from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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
