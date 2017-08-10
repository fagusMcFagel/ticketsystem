from django.db import models

# Create your models here.
class Ticket(models.Model):   
    #constants for choices in form(and template) fields and
    SECTOR_CHOICES = [('Saperion', 'Saperion'), ('Allgemein','Allgemein')]
    CATEGORY_CHOICES = [('Problem','Problem'), ('Vorschlag','Vorschlag')]
    STATUS_CHOICES = [('open','Offen'),('delayed','Verzögert'),('processing','In Bearbeitung')]
    
    
    ticketid = models.AutoField(primary_key=True, verbose_name="TicketID")
    status = models.CharField(max_length=20, verbose_name="Status")
    
    sector = models.CharField(max_length=30, verbose_name="Bereich")
    category = models.CharField(max_length=30, verbose_name="Art")
    subject = models.CharField(max_length=50, verbose_name="Betreff")
    description = models.CharField(max_length=400, verbose_name="Beschreibung")
    creationdatetime = models.DateTimeField(verbose_name="Erstellungsdatum")
    creator = models.CharField(max_length=40, verbose_name="Ersteller")
    
    responsible_person = models.CharField(max_length=40, blank=True, verbose_name="Verantwortlicher")
    comment = models.CharField(max_length=100, verbose_name="Kommentar")
    solution = models.CharField(max_length=400, verbose_name="Lösung")
    keywords = models.CharField(max_length=100, verbose_name="Keywords")
    closingdatetime = models.DateTimeField(null=True, blank=True, verbose_name="Abschlussdatum")
    workinghours = models.FloatField(default=0.0, verbose_name="Bearbeitungszeit")
    

    
    