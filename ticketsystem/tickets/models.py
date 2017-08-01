from django.db import models

# Create your models here.
class Ticket(models.Model):    
    #basic ticket data
    sector = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    subject = models.CharField(max_length=50)
    description = models.CharField(max_length=400)
    creationdate = models.DateField()
    
    #advanced/background ticket data
    ticketid = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20)
    closingdate = models.DateField()
    comment = models.CharField(max_length=100)
    solution = models.CharField(max_length=400)
    keywords = models.CharField(max_length=100)
    
    # FIXME: create separate class Person and change to foreign key?
    responsible_person = models.CharField(max_length=40)
    creator = models.CharField(max_length=40)