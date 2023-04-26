from django import forms

class SearchForm(forms.Form):
    PLATFORM_CHOICES = [
        ('Twitter', 'Twitter'),
        ('YouTube', 'YouTube'),
        ('Instagram', 'Instagram')]
    platform = forms.ChoiceField(choices=PLATFORM_CHOICES)
    username = forms.CharField()
    keyword = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'id_keyword'}))