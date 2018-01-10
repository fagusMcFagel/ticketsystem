# Django
from django.contrib.auth.models import Group

#class which contains constants for form and model fields
class FieldConstants():    
    #constants for compact and detailed measure field labels
    COMPACT_MEASURE_FIELD_LABELS = {
        'measureid':'UID', 
        'creationdatetime':'Zeitpunkt', 
        'shortdsc':'Kurzbeschreibung', 
        'dsc':'Beschreibung', 
        'result':'Ergebnis', 
        'isSolution':'ist Lösung'}
    
    MEASURE_FIELD_LABELS = {
        'ticketid':'TicketID', 
        'shortdsc':'Kurzbeschreibung',
        'dsc':'Beschreibung', 
        'result':'Ergebnis', 
        'isSolution':'ist Lösung'
    }
    
    #constant for ticket field labels
    TICKET_FIELD_LABELS = {
        'ticketid':'TicketID', 
        'sector':'Bereich', 
        'category':'Art', 
        'subject':'Betreff',
        'description':'Beschreibung', 
        'status':'Status', 
        'priority':'Priorität', 
        'comment':'Kommentar',
        'keywords':'Schlagworte', 
        'responsible_person':'Verantwortliche/r', 
        'workinghours':'Bearbeitungszeit (in h)',
        'creationdatetime':'Erstell-Zeitpunkt', 
        'creator':'Erstellt von', 
        'closingdatetime':'Abschlussdatum', 
        'image':'Screenshot'
    }
   
    #constants for choice fields in tickets and measures
    SECTOR_FIELD_CHOICES = [
        (Group.objects.get(name='Saperion'), 'Saperion'),
    ]
    
    CATEGORY_FIELD_CHOICES = [
        ('Problem','Problem'), 
        ('Vorschlag','Vorschlag')
    ]
    
    STATUS_FIELD_CHOICES = [
        ('open','Offen'),
        ('delayed','Verzögert'),
        ('processing','In Bearbeitung')
    ]
    
    PRIORITY_FIELD_CHOICES = [
        ('',''), 
        ('low','niedrig'), 
        ('moderate','normal'), 
        ('high','hoch')
    ]
    
    SOLUTION_FIELD_CHOICES = [
        ('',''), 
        ('unsuccesful', 'erfolglos'), 
        ('temporary', 'temporär'), 
        ('partly','teilweise'), 
        ('solution', 'Lösung')
    ]