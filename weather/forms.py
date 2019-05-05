# For using ModelForm provided by django
from django.forms import ModelForm, TextInput
from .models import City

class CityForm(ModelForm):
    class Meta:
        # This form will take the data for our model "City"
        model = City
        # This form has fields - name of city
        fields = ['name']
        # Giving attributes to fields
        widgets = { 'name' : TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'}) }