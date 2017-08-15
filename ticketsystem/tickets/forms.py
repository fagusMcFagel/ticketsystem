from django import forms
from tickets.models import Ticket

#form for entering ticket data
class EnterTicketForm(forms.Form):
    sector = forms.ChoiceField(choices = Ticket.SECTOR_CHOICES, label="Bereich")
    category = forms.ChoiceField(choices = Ticket.CATEGORY_CHOICES, label="Art")
    subject = forms.CharField(max_length=50, label="Betreff")
    description = forms.CharField(max_length=400,widget=forms.Textarea, label="Beschreibung")
    image = forms.ImageField()

#form for entering login data
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label="Benutzername")
    password = forms.CharField(max_length=40, widget=forms.PasswordInput, label="Passwort")
    
#form for display of unchangeable ticket data (except by admins)
class DetailForm(forms.Form):
    #basic ticket data
    ticketid = forms.CharField(max_length=10, disabled=True, label="TicketID")
    sector = forms.CharField(max_length=30, disabled=True, label="Bereich")
    category = forms.CharField(max_length=30, disabled=True, label="Art")
    subject = forms.CharField(max_length=50, disabled=True, label="Betreff")
    description = forms.CharField(widget=forms.Textarea, max_length=400, disabled=True, label="Beschreibung")
    creationdatetime = forms.DateField(widget=forms.DateInput, disabled=True, label="Erstellungsdatum")

    # TODO: create separate class Person and change to foreign key?
    responsible_person = forms.CharField(max_length=40, disabled=True, label="Verantwortlicher")
    creator = forms.CharField(max_length=40, disabled=True, label="Ersteller")

#form for display of ticket data changeable by the ticket processors
class EditableDataForm(forms.Form):
    status = forms.ChoiceField(choices = Ticket.STATUS_CHOICES, label="Status", required=False)
    comment = forms.CharField(widget=forms.Textarea, max_length=100, label="Kommentar", required=False)
    solution = forms.CharField(widget=forms.Textarea,max_length=400, label="Lösung", required=False)
    keywords = forms.CharField(widget=forms.Textarea,max_length=100, label="Keywords", required=False)

#form for ticket data especially relevant & partly required when closing ticket
class ClosingDataForm(forms.Form):
    status = forms.ChoiceField(choices=[('closed','closed')],initial='closed', disabled=True, label="Status")
    comment = forms.CharField(widget=forms.Textarea, max_length=100, required=False, label="Kommentar")
    solution = forms.CharField(widget=forms.Textarea,max_length=400, required=True, label="Lösung")
    keywords = forms.CharField(widget=forms.Textarea,max_length=100, required=True, label="Keywords")
    workinghours = forms.FloatField(required=True, label="Bearbeitungszeit (in Std)")

#form for entering query data
class SearchForm(forms.Form):
    sector = forms.ChoiceField(choices = Ticket.SECTOR_CHOICES+[('','')], required=False, label="Bereich")
    category = forms.ChoiceField(choices = Ticket.CATEGORY_CHOICES+[('','')], required=False, label="Art")
    status = forms.ChoiceField(choices = Ticket.STATUS_CHOICES+[('','')], required=False, label="Status")
    subject = forms.CharField(max_length=40, required=False, label="Betreff")
    description = forms.CharField(max_length=40, required=False, label="Beschreibung")  
    comment = forms.CharField(max_length=40, required=False, label="Kommentar")
    solution = forms.CharField(max_length=40, required=False, label="Lösung")
    keywords = forms.CharField(max_length=40, required=False, label="Keywords")