from django import forms
from .models import Ticket, Passenger, ItineraryEntry

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ('Given_Name', 'Last_Name', 'Middle_Initial',
                  'Birth_Date', 'Gender')

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('Customer_ID','Date')

class ItineraryEntryForm(forms.ModelForm):
    class Meta:
        model = ItineraryEntry
        fields = ('Ticket_ID','Trip_ID')

class SalesReportForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
