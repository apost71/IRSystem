from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'size': 77, 'placeholder': 'Search...', 'rows': 100}))

    def __init__(self, query = None, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['query'].label = False
        if query:
            self.fields['query'].widget.attrs['value'] = query
