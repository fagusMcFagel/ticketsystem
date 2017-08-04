from django import forms
from tickets.models import Ticket

#form for entering ticket data
class EnterTicketForm(forms.Form):
    sector = forms.ChoiceField(choices = Ticket.SECTOR_CHOICES)
    category = forms.ChoiceField(choices = Ticket.CATEGORY_CHOICES)
    subject = forms.CharField(max_length=50)
    description = forms.CharField(max_length=400,widget=forms.Textarea)

#form for entering login data
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=40, widget=forms.PasswordInput)
    
#form for display of unchangeable ticket data (except by admins)
class DetailForm(forms.Form):
    #basic ticket data
    sector = forms.CharField(max_length=30, disabled=True)
    category = forms.CharField(max_length=30, disabled=True)
    subject = forms.CharField(max_length=50, disabled=True)
    description = forms.CharField(max_length=400, disabled=True)
    creationdate = forms.DateField(widget=forms.DateInput, disabled=True)
    ticketid = forms.CharField(max_length=10, disabled=True)

    # TODO: create separate class Person and change to foreign key?
    responsible_person = forms.CharField(max_length=40, disabled=True)
    creator = forms.CharField(max_length=40, disabled=True)

#form for display of ticket data changeable by the ticket processors
class EditableDataForm(forms.Form):
    status = forms.ChoiceField(choices = Ticket.STATUS_CHOICES)
    comment = forms.CharField(widget=forms.Textarea, max_length=100)
    solution = forms.CharField(widget=forms.Textarea,max_length=400)
    keywords = forms.CharField(widget=forms.Textarea,max_length=100)