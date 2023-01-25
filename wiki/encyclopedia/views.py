from django.shortcuts import render, redirect
from django import forms
from markdown2 import Markdown
from . import util
import random

markdowner = Markdown()

class NewPageForm(forms.Form):
    page_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'New Page Title'}))
    page_content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'New Page Content'}))

class EditPageForm(forms.Form):
    page_content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Edit Page Content'}), label="")

def index(request):
    search_query = request.GET.get('q')
    if search_query:
        return redirect('/search/?q=' + search_query)

    random_variable = request.GET.get('random', 'FALSE')

    if random_variable == "TRUE":

        entries = util.list_entries()
        random_page = random.choice(entries)

        return redirect('wiki/' + random_page)

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def view_page(request, page_name):
    search_query = request.GET.get('q')
    if search_query:
        return redirect('/search/?q=' + search_query)

    page_content_markdown = util.get_entry(page_name)

    if page_content_markdown:
        page_content_html = markdowner.convert(page_content_markdown)
        page_found = True
    else:
        page_content_html = ""
        page_found = False

    return render(request, "encyclopedia/view_page.html", {
        "page_name": page_name,
        "page_content": page_content_html,
        "page_found": page_found
    })


def new_page(request):
    search_query = request.GET.get('q')
    if search_query:
        return redirect('/search/?q=' + search_query)

    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            page_content = form.cleaned_data["page_content"]
            page_title = form.cleaned_data["page_title"]
            page_title_lower = page_title.lower()
            all_pages = util.list_entries()
            all_pages_lower = [page.lower() for page in all_pages]
            if page_title_lower in all_pages_lower:
                error_msg = "There already exists a page with this title. Please choose a new title of visit the existing page with this title."
                return render(request, "encyclopedia/new_page.html", {
                    "error_msg":error_msg,
                    "form": form
                })
            else:
                new_page = open("entries/" + page_title + ".md", "x")
                new_page.write("# " + page_title)
                new_page.write("\n")
                new_page.write(page_content)
                new_page.close()

                return redirect('/wiki/' + page_title)

    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForm()
    })

def edit_page(request, page_name):
    search_query = request.GET.get('q')
    if search_query:
        return redirect('/search/?q=' + search_query)

    if request.method == "POST":
        form = EditPageForm(request.POST)
        print(form)
        if form.is_valid():
            page_content = form.cleaned_data["page_content"]
            util.save_entry(page_name, page_content)

            return redirect('/wiki/' + page_name)
          
    page_content = util.get_entry(page_name)

    form = EditPageForm(initial={'page_content': page_content})

    return render(request, "encyclopedia/edit_page.html", {
        "page_title": page_name,
        "form": form
    })

def searched_pages(request):
    search_query = request.GET.get('q')
    search_query_lower = search_query.lower()
    all_pages = util.list_entries()
    all_pages_lower = [page.lower() for page in all_pages]

    if search_query_lower in all_pages_lower:
        return redirect('/wiki/' + search_query)
    else:
        pages_like = []

        for page in all_pages:
            if search_query in page:
                pages_like.append(page)

        return render(request, "encyclopedia/search_pages.html", {
            "search_query": search_query,
            "pages": pages_like
        })