import markdown2

from django.shortcuts import render

from . import util
from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    markdowner = Markdown()
    return render(request, "encyclopedia/entry.html", {
        "entry": markdowner.convert(util.get_entry(entry))
    })
    

