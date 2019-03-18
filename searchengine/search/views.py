from django.shortcuts import render
from search.engine.SearchEngine import SearchEngine
from .forms import SearchForm


engine = SearchEngine()


def get_name(request):

    # if this is a POST request we need to process the form data
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        # form = NameForm(request.POST)
        form = SearchForm(request.GET)
        query = request.GET.get('query')

        if not query:
            return render(request, 'search.html', {'form': form})

        else:
            form = SearchForm(query=query)
            # corrected = SearchEngine.spell_check(query)
            corrected = query
            if query != corrected:
                fixed_query = corrected
                documents = engine.query(corrected)
            else:
                fixed_query = None
                documents = engine.query(query)
            return render(request, 'search.html', {'form': form, 'documents': documents, 'query': fixed_query})


    # if a GET (or any other method) we'll create a blank form
    else:
        # form = NameForm()
        form = SearchForm()

    return render(request, 'search.html', {'form': form})
