import markdown2

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse

from . import util
from markdown2 import Markdown

class NewEntryForm(forms.Form):
    title = forms.CharField(label="New Entry")
    content = forms.CharField(widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    markdowner = Markdown()
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/nonExistingEntry.html", {
            "entryTitle": entry    
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(entryPage),
            "entryTitle": entry
        })

def newEntry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if(util.get_entry(title) is None):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/newEntry.html", {
                "form": form,
                "existing": True
                })
        else:
            return render(request, "encyclopedia/newEntry.html", {
            "form": form,
            "existing": False
            })
    else:
        return render(request,"encyclopedia/newEntry.html", {
            "form": NewEntryForm(),
            "existing": False
        })    

