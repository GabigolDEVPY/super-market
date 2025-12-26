from django import forms
from models import InfosForm


class InfosForm(forms.ModelForm):
    class Meta:
        model = InfosForm()
        fields = ("address", "complement", "neighborhood", "number", "tel", "city", "cap", "state")
        
    