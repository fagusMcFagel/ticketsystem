from django.http import Http404, HttpResponse#, HttpResponseRedirect
from tickets.models import Ticket
from tickets.forms import EnterTicketForm
from django.shortcuts import render
from django.core.mail import get_connection, send_mail
from test.libregrtest.cmdline import DESCRIPTION
import datetime

#needed later
#from django.core.mail import send_mail, get_connection

#function for 'tickets/enter'
def enter_ticket(request):
    if request.method=="POST":
        #set form as EnterTicketForm-Object with the POST-data
        form = EnterTicketForm(request.POST)
        
        #create an entry in the database with the entered data
        if form.is_valid():
            #get cleaned data and current system time
            cd = form.cleaned_data
            now = datetime.datetime.now()
            
            #init ticket object; 
            #ticketid increments automatically
            #all fields can't be NULL, so explicitly initalised with ''
            t = Ticket(sector='Saperion', category='Problem', 
                       subject=cd['subject'], description=cd['description'],
                       creationdate = now, status='open',
                       creator=request.META['USERNAME'],
                       responsible_person='Falk Forner',
                       closingdate='1999-12-12', comment='', solution='',keywords=''
            )
            
            #save data set to database
            t.save()
            
            thx = True
        else:
            thx = False
    else:
        thx = False
        form = EnterTicketForm()
    
    return render(request, 'ticket_enter.djhtml', {'form':form, 'thx':thx})

#function for 'tickets/d{1,4}'
def show_ticket_detail(request, ticketid):
    #checks for the id in the database, fetch the ticket data and 
    #show it in the template for ticket details
    return HttpResponse("Details of %s" % (ticketid))

#function for 'tickets/d{1,4}/edit'
def edit_ticket_detail(request, ticketid):
    #check if user may edit tickets, check for ticket id in the database, display
    #the ticket data and save any changes to the database on confirmation
    return HttpResponse("Edit details of %s" % (ticketid))

#function for 'tickets/overview'
def show_ticket_list(request):
    tickets = Ticket.objects.filter(status='open')
    #search for the tickets to be displayed according to the 
    #requesting user and return the template with the fetched data on display
    return render(request, 'ticket_overview.djhtml', {'tickets':tickets})

#function for 'tickets/search'
def search_tickets(request):
    if request.method=="GET":
        #check for valid input, search in the database and 
        #fetch any results
        return HttpResponse("GET request detected")
    else:
        #display error page "Not a valid GET request(?)"
        return HttpResponse("NON GET request detected")