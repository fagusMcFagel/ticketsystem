#Django
from django import forms

# local Django
from tickets.field_constants import FieldConstants

#form for entering ticket data
class EnterTicketForm(forms.Form):
    sector = forms.ChoiceField(choices = FieldConstants.SECTOR_FIELD_CHOICES, label="Bereich")
    category = forms.ChoiceField(choices = FieldConstants.CATEGORY_FIELD_CHOICES, label="Art")
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
    status = forms.ChoiceField(choices = FieldConstants.STATUS_FIELD_CHOICES, label="Status", required=False)
    priority = forms.ChoiceField(choices = FieldConstants.PRIORITY_FIELD_CHOICES, label="Priorität", required=False)
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
    workinghours = forms.FloatField(required=True, label="Arbeitsstd.")

#form for entering query data
class SearchForm(forms.Form):
    sector = forms.ChoiceField(choices = FieldConstants.SECTOR_FIELD_CHOICES+[('','')], required=False, label="Bereich")
    category = forms.ChoiceField(choices = FieldConstants.CATEGORY_FIELD_CHOICES+[('','')], required=False, label="Art")
    status = forms.ChoiceField(choices = FieldConstants.STATUS_FIELD_CHOICES+[('','')], required=False, label="Status")
    subject = forms.CharField(max_length=40, required=False, label="Betreff")
    description = forms.CharField(max_length=40, required=False, label="Beschreibung")  
    comment = forms.CharField(max_length=40, required=False, label="Kommentar")
    keywords = forms.CharField(max_length=40, required=False, label="Keywords")

#compact form for the taken measures for the solution of the Ticket
#compact through decreasing textarea sizes for short preview of the texts (dsc, result)
class CompactMeasureForm(forms.Form):
    measureid = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'inputfield'}), label=FieldConstants.COMPACT_MEASURE_FIELD_LABELS['measureid'], disabled=True)
    creationdatetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'inputfield'}), label=FieldConstants.COMPACT_MEASURE_FIELD_LABELS['creationdatetime'], disabled=True)
    shortdsc = forms.CharField(widget=forms.TextInput(attrs={'class': 'inputfield'}), max_length=100, label=FieldConstants.COMPACT_MEASURE_FIELD_LABELS['shortdsc'], disabled=True)
    dsc = forms.CharField(widget=forms.Textarea(attrs={'class': 'inputfield', 'rows': 1, 'cols': 30}), max_length=400, label=FieldConstants.COMPACT_MEASURE_FIELD_LABELS['dsc'], disabled=True)
    result = forms.CharField(widget=forms.Textarea(attrs={'class': 'inputfield', 'rows': 1, 'cols': 30}), max_length=400, label=FieldConstants.COMPACT_MEASURE_FIELD_LABELS['result'], disabled=True)
    is_solution = forms.ChoiceField(widget=forms.Select(attrs={'class': 'inputfield'}),choices=FieldConstants.SOLUTION_FIELD_CHOICES, label=FieldConstants.COMPACT_MEASURE_FIELD_LABELS['isSolution'], disabled=True)

#complete form for taken measures for the solution of the Ticket
#complete form in a way, that all necessary fields are displayed at a normal size (not decreased)
#ticketid is a field used for display only, since the ticketid is taken from the ticket object in the view function
class MeasureForm(forms.Form):
    ticketid = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'inputfield'}), label=FieldConstants.MEASURE_FIELD_LABELS['ticketid'], required=False)
    shortdsc = forms.CharField(widget=forms.TextInput(attrs={'class': 'inputfield'}), max_length=100, label=FieldConstants.MEASURE_FIELD_LABELS['shortdsc'])
    dsc = forms.CharField(widget=forms.Textarea(attrs={'class': 'inputfield', 'rows':8}), max_length=400, label=FieldConstants.MEASURE_FIELD_LABELS['dsc'], required=False)
    result = forms.CharField(widget=forms.Textarea(attrs={'class': 'inputfield', 'rows':8}), max_length=400, label=FieldConstants.MEASURE_FIELD_LABELS['result'])
    is_solution = forms.ChoiceField(widget=forms.Select(attrs={'class': 'inputfield'}), choices=FieldConstants.SOLUTION_FIELD_CHOICES, label=FieldConstants.MEASURE_FIELD_LABELS['isSolution'])
