from django import forms


class EmailForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    text = forms.CharField(max_length=300, required=True)
    datetime = forms.DateTimeField(help_text="Date example: YYYY-MM-DD hh:mm:ss")
