from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your search', max_length=100)


class PersonForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'size': 77, 'placeholder': 'Search...', 'rows': 100}))

    def __init__(self, query = None, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['query'].label = False
        placeholder = 'Search...' if not query else query
        self.fields['query'].widget.attrs['placeholder'] = placeholder
