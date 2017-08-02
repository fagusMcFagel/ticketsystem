from django import forms
from tickets.models import Ticket

#form for creating a ticket
class EnterTicketForm(forms.Form):
    sector = forms.ChoiceField(choices = Ticket.SECTOR_CHOICES)
    category = forms.ChoiceField(choices = Ticket.CATEGORY_CHOICES)
    subject = forms.CharField(max_length=50)
    description = forms.CharField(max_length=400,widget=forms.Textarea)