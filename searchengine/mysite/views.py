from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import PersonForm


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        # form = NameForm(request.POST)
        form = PersonForm(request.GET)
        query = request.GET.get('query')
        print(query)

        if not query:
            form = PersonForm()
            return render(request, 'search.html', {'form': form})

        else:
            form = PersonForm(query=query)
            return render(request, 'search.html', {'form': form})
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        # form = NameForm()
        form = PersonForm()

    return render(request, 'search.html', {'form': form})
