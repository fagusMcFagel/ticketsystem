from django.db import models

# Create your models here.
class Ticket(models.Model):   
    #constants needed for display in the form => template
    SECTOR_CHOICES = [('Saperion', 'Saperion'), ('Allgemein','Allgemein')]
    CATEGORY_CHOICES = [('Problem','Problem'), ('Vorschlag','Vorschlag')]
    STATUS_CHOICES = [('open','open'),('delayed','delayed'),('processing','processing'),('closed','closed')]
    #
    # TODO: CREATE VALIDATORS FOR CRITICAL FIELDS ??
    # 
    
    #basic ticket data
    sector = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    subject = models.CharField(max_length=50)
    description = models.CharField(max_length=400)
    creationdate = models.DateField()
    
    #advanced/background ticket data
    ticketid = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20)
    closingdate = models.DateField(null=True, blank=True)
    comment = models.CharField(max_length=100)
    solution = models.CharField(max_length=400)
    keywords = models.CharField(max_length=100)
    
    # TODO: create separate class Person and change to foreign key?
    responsible_person = models.CharField(max_length=40)
    creator = models.CharField(max_length=40)
    
    