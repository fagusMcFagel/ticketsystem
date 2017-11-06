from django.db import models
from django.contrib.auth.models import User, Group
from tickets.field_constants import FieldConstants

# model for tickets
class Ticket(models.Model):
    CATEGORY_CHOICES = FieldConstants.get_CATEGORY_FIELD_CHOICES()
    STATUS_CHOICES = FieldConstants.get_STATUS_FIELD_CHOICES()
    PRIORITY_CHOICES = FieldConstants.get_PRIORITY_FIELD_CHOICES()
    
    # primary key
    ticketid = models.AutoField(primary_key=True, verbose_name="TicketID")
    
    # data input by user at ticket creation
    sector = models.ForeignKey(Group, max_length=50, related_name="+")
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=30, verbose_name="Art")
    subject = models.CharField(max_length=50, verbose_name="Betreff")
    description = models.CharField(max_length=400, verbose_name="Beschreibung")
    
    # data editable/input by user/s processing the ticket
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, verbose_name="Status")
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=20, verbose_name="Priorität")
    comment = models.CharField(max_length=100, verbose_name="Kommentar")
    keywords = models.CharField(max_length=100, verbose_name="Keywords") 
    responsible_person = models.ForeignKey(User, max_length=50, related_name="+", null=True)   
    workinghours = models.FloatField(default=0.0, verbose_name="Bearbeitungszeit")
    
    # data which is filled at ticket creation/closing
    creationdatetime = models.DateTimeField(verbose_name="Erstell-Zeitpunkt")
    creator = models.CharField(max_length=40, verbose_name="Ersteller")
    closingdatetime = models.DateTimeField(null=True, blank=True, verbose_name="Abschlussdatum")
    
    # field for appended file(-> image, screenshot)
    image = models.FileField(null=True, blank=True, upload_to='uploads/')

# model for measures taken to solve the user's problem
class Measures(models.Model):
    SOLUTION_CHOICES = FieldConstants.get_SOLUTION_FIELD_CHOICES()
    # primary key
    measureid = models.AutoField(primary_key=True, verbose_name="UID")
    
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="Measures", null=True)
    creationdatetime = models.DateTimeField(verbose_name="Zeitpunkt")
    shortdsc = models.CharField(max_length=100, verbose_name="Kurzbeschreibung")
    dsc = models.CharField(max_length=400, verbose_name="Beschreibung", null=True)
    result = models.CharField(max_length=400, verbose_name="Ergebnis")
    isSolution = models.CharField(choices=SOLUTION_CHOICES, max_length=30, verbose_name="Ist Lösung")
    
