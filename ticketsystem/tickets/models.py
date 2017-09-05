from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Ticket(models.Model):   
    #constants for choices in form(and template) fields and
    SECTOR_CHOICES = [(Group.objects.get(name='Saperion'), 'Saperion'),]
    CATEGORY_CHOICES = [('Problem','Problem'), ('Vorschlag','Vorschlag')]
    STATUS_CHOICES = [('open','Offen'),('delayed','Verzögert'),('processing','In Bearbeitung')]
    PRIORITY_CHOICES = [('',''), ('low','niedrig'), ('moderate','normal'), ('high','hoch')]
    
    #primary key
    ticketid = models.AutoField(primary_key=True, verbose_name="TicketID")
    
    #data input by user at ticket creation
    sector = models.ForeignKey(Group, max_length=50, verbose_name="Bereich")
    category = models.CharField(max_length=30, verbose_name="Art")
    subject = models.CharField(max_length=50, verbose_name="Betreff")
    description = models.CharField(max_length=400, verbose_name="Beschreibung")
    
    #data editable/input by user/s processing the ticket
    status = models.CharField(max_length=20, verbose_name="Status")
    priority = models.CharField(max_length=20, verbose_name="Priorität")
    comment = models.CharField(max_length=100, verbose_name="Kommentar")
    solution = models.CharField(max_length=400, verbose_name="Lösung")
    keywords = models.CharField(max_length=100, verbose_name="Keywords") 
    responsible_person = models.ForeignKey(User, max_length=50, verbose_name="Verantwortliche/r", null=True)   
    workinghours = models.FloatField(default=0.0, verbose_name="Bearbeitungszeit")
    
    #data which is filled at ticket creation/closing
    creationdatetime = models.DateTimeField(verbose_name="Erstell-Zeitpunkt")
    creator = models.CharField(max_length=40, verbose_name="Ersteller")
    closingdatetime = models.DateTimeField(null=True, blank=True, verbose_name="Abschlussdatum")
    
    #field for appended file(-> image, screenshot)
    image = models.FileField(null=True, blank=True, upload_to='uploads/')