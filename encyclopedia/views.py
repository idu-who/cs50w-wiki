from django import forms
from django.core.exceptions import ValidationError
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


def validate_unique_title(title):
    if title in util.list_entries():
        raise ValidationError(
            f'Entry with title "{title}" already exists.'
        )


class CreateEntryForm(forms.Form):
    title = forms.CharField(
        label="Title",
        required=True,
        validators=[validate_unique_title]
    )
    content = forms.CharField(label="Content", widget=forms.Textarea())


def create_entry(request):

    if request.method == "POST":
        form = CreateEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            util.save_entry(title, content)

            return HttpResponseRedirect(reverse(
                "entry",
                kwargs={"title": title}
            ))
        else:
            return render(request, "encyclopedia/create_entry.html", {
                "form": form
            })

    return render(request, "encyclopedia/create_entry.html", {
        "form": CreateEntryForm()
    })
