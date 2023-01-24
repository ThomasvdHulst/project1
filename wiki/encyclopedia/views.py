from django.shortcuts import render, redirect
from django import forms
from markdown2 import Markdown
from . import util
import random

markdowner = Markdown()

class NewPageForm(forms.Form):
    page_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'New Page Title'}))
    page_content = forms.CharField(widget=forms.Textarea(attrs={"rows":"2", 'placeholder': 'New Page Content'}))

def index(request):
    random_variable = request.GET.get('random', 'FALSE')

    if random_variable == "TRUE":

        entries = util.list_entries()
        random_page = random.choice(entries)

        return redirect('/wiki/' + random_page)

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view_page(request, page_name):
    page_content_markdown = util.get_entry(page_name)
    page_content_html = markdowner.convert(page_content_markdown)

    return render(request, "encyclopedia/view_page.html", {
        "page_name": page_name,
        "page_content": page_content_html
    })

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            page_title = form.cleaned_data["page_title"].lower()
            all_pages = util.list_entries()
            all_pages_lower = [page.lower() for page in all_pages]
            if page_title in all_pages_lower:
                error_msg = "There already exists a page with this title. Please choose a new title of visit the existing page with this title."
                return render(request, "encyclopedia/new_page.html", {
                    "error_msg":error_msg,
                    "form": form
                })
            else:
                return redirect('/')

    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForm()
    })
