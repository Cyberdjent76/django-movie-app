from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os
import wikipedia


AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
              'Movies',
              api_key=os.environ.get('AIRTABLE_API_KEY'))

# Create your views here.
def home_page(request):
    #context = AT.get_all([{movie.fields.Name}, 'Name' in sorted(search_result.items(), key=lambda item:('name'[0]))])
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend) #,context)


def create(request):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'http://www.uh.edu/pharmacy/_images/students/pcol-pceu/no-image-available-2.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
            #'Link': request.POST.get(wikipedia.WikipediaPage.HTML('link'))
        }
        try:
            response = AT.insert(data)
            messages.success(request, "New movie added: {}".format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, "Got an error when adding the new movie: {}".format(e))
    return redirect('/')

def edit(request, movie_id):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'http://www.uh.edu/pharmacy/_images/students/pcol-pceu/no-image-available-2.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes'),
            'Links': request.POST.get('links')
        }
        try:
            response = AT.update(movie_id, data)
            messages.info(request, "Updated movie: {}".format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, "Got an error when trying to update the movie: {}".format(e))
    return redirect("/")

def delete(request, movie_id):
    try:
        movie_name = AT.get(movie_id)['fields'].get('Name')
        response = AT.delete(movie_id)
        messages.warning(request, "Deleted movie: {}".format(movie_name))
    except Exception as e:
        messages.warning(request, "Got an error when trying to delete the movie: {}".format(e))
    return redirect("/")
