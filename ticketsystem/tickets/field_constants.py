# Django
from django.contrib.auth.models import User, Group

#class which contains constants for form and model fields
class FieldConstants():    
    #return constants for compact and detailed measure field labels
    def get_COMPACT_MEASURE_FIELD_LABELS():
        COMPACT_MEASURE_FIELD_LABELS = {
            'measureid':'UID', 
            'creationdatetime':'Zeitpunkt', 
            'shortdsc':'Kurzbeschreibung', 
            'dsc':'Beschreibung', 
            'result':'Ergebnis', 
            'isSolution':'ist Lösung'}
        return COMPACT_MEASURE_FIELD_LABELS
    
    def get_MEASURE_FIELD_LABELS():
        MEASURE_FIELD_LABELS = {
            'ticketid':'TicketID', 
            'shortdsc':'Kurzbeschreibung',
            'dsc':'Beschreibung', 
            'result':'Ergebnis', 
            'isSolution':'ist Lösung'
        }
        return MEASURE_FIELD_LABELS
    
    #returns constant for ticket field labels
    def get_TICKET_FIELD_LABELS():
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
        return TICKET_FIELD_LABELS
   
    #getters for constants for choice fields in tickets and measures
    def get_SECTOR_FIELD_CHOICES():
        SECTOR_FIELD_CHOICES = [
            (Group.objects.get(name='Saperion'), 'Saperion'),
        ]
        return SECTOR_FIELD_CHOICES
    
    def get_CATEGORY_FIELD_CHOICES():
        CATEGORY_FIELD_CHOICES = [
            ('Problem','Problem'), 
            ('Vorschlag','Vorschlag')
        ]
        return CATEGORY_FIELD_CHOICES
    
    def get_STATUS_FIELD_CHOICES():
        STATUS_FIELD_CHOICES = [
            ('open','Offen'),
            ('delayed','Verzögert'),
            ('processing','In Bearbeitung')
        ]
        return STATUS_FIELD_CHOICES
    
    def get_PRIORITY_FIELD_CHOICES():
        PRIORITY_FIELD_CHOICES = [
            ('',''), 
            ('low','niedrig'), 
            ('moderate','normal'), 
            ('high','hoch')
        ]
        return PRIORITY_FIELD_CHOICES
    
    def get_SOLUTION_FIELD_CHOICES():
        SOLUTION_FIELD_CHOICES = [
            ('',''), 
            ('unsuccesful', 'erfolglos'), 
            ('temporary', 'temporär'), 
            ('partly','teilweise'), 
            ('solution', 'Lösung')
        ]
        return SOLUTION_FIELD_CHOICES