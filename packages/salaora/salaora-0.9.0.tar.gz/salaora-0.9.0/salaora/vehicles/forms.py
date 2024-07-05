from django import forms

class BulkCreateVehiclesForm(forms.Form):
    csv_data = forms.CharField()
