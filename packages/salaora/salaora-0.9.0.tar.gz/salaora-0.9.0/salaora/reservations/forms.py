from django import forms

class ReservationForm(forms.Form):
    vehicle = forms.CharField(max_length=12)
    client_name = forms.CharField(max_length=100)
    departure_dt = forms.DateTimeField()
    return_dt = forms.DateTimeField()
    details = forms.CharField()
