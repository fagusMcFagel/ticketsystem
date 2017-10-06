from django import forms
from tickets.models import Ticket, SolvingMeasures

#form for entering ticket data
class EnterTicketForm(forms.Form):
    sector = forms.ChoiceField(choices = Ticket.SECTOR_CHOICES, label="Bereich")
    category = forms.ChoiceField(choices = Ticket.CATEGORY_CHOICES, label="Art")
    subject = forms.CharField(max_length=50, label="Betreff")
    description = forms.CharField(max_length=400,widget=forms.Textarea, label="Beschreibung")
    image = forms.FileField(required=False)

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
    priority = forms.ChoiceField(choices = Ticket.PRIORITY_CHOICES, label="Priorität", required=False)
    comment = forms.CharField(widget=forms.Textarea, max_length=100, label="Kommentar", required=False)
    keywords = forms.CharField(widget=forms.Textarea,max_length=100, label="Keywords", required=False)

#form for display of closed ticket's data entered by ticket processor;
class ClosedDataForm(forms.Form):
    status = forms.CharField(label="Status", required=False, disabled=True)
    comment = forms.CharField(widget=forms.Textarea, max_length=100, label="Kommentar", required=False)
    keywords = forms.CharField(widget=forms.Textarea,max_length=100, label="Keywords", required=False)

#form for ticket data especially relevant & partly required when closing ticket
class ClosingDataForm(forms.Form):
    status = forms.ChoiceField(choices=[('closed','closed')],initial='closed', disabled=True, label="Status")
    comment = forms.CharField(widget=forms.Textarea, max_length=100, required=False, label="Kommentar")
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
    keywords = forms.CharField(max_length=40, required=False, label="Keywords")

#compact form for the taken measures for the solution of the Ticket
#compact through decreasing textarea sizes for short preview of the texts (dsc, result)
class CompactMeasureForm(forms.Form):
    FIELD_LABELS = {'measureid':'UID', 'creationdatetime':'Zeitpunkt', 'shortdsc':'Kurzbeschreibung', 
                    'dsc':'Beschreibung', 'result':'Ergebnis', 'isSolution':'ist Lösung'}
    measureid = forms.IntegerField(label=FIELD_LABELS['measureid'], disabled=True)
    creationdatetime = forms.DateTimeField(widget=forms.DateTimeInput, label=FIELD_LABELS['creationdatetime'], disabled=True)
    shortdsc = forms.CharField(max_length=100, label=FIELD_LABELS['shortdsc'], disabled=True)
    dsc = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 30}), max_length=400, label=FIELD_LABELS['dsc'], disabled=True)
    result = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 30}), max_length=400, label=FIELD_LABELS['result'], disabled=True)
    isSolution = forms.ChoiceField(choices=SolvingMeasures.SOLUTION_CHOICES, label=FIELD_LABELS['isSolution'], disabled=True)

#complete form for taken measures for the solution of the Ticket
#complete form in a way, that all necessary fields are displayed at a normal size (not decreased)
#ticketid is a field used for display only, since the ticketid is taken from the ticket object in the view function
class MeasureForm(forms.Form):
    FIELD_LABELS = {'ticketid':'TicketID', 'shortdsc':'Kurzbeschreibung', 
                    'dsc':'Beschreibung', 'result':'Ergebnis', 'isSolution':'ist Lösung'}
    ticketid = forms.IntegerField(label=FIELD_LABELS['ticketid'], required=False)
    shortdsc = forms.CharField(max_length=100, label=FIELD_LABELS['shortdsc'])
    dsc = forms.CharField(widget=forms.Textarea(), max_length=400, label=FIELD_LABELS['dsc'], required=False)
    result = forms.CharField(widget=forms.Textarea(), max_length=400, label=FIELD_LABELS['result'])
    isSolution = forms.ChoiceField(choices=SolvingMeasures.SOLUTION_CHOICES, label=FIELD_LABELS['isSolution'])