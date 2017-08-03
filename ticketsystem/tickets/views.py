from django.http import HttpResponse, HttpResponseRedirect
from tickets.models import Ticket
from tickets.forms import EnterTicketForm, LoginForm, DetailForm,\
    EditableDataForm
from django.shortcuts import render
from django.db.models import Q
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.forms.models import model_to_dict

#needed later
#from django.core.mail import send_mail, get_connection

#function for 'tickets/login'
def login_user(request):
    error = False
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/tickets/overview/')
            else:
                error=True
                form = LoginForm()

    else:
        form = LoginForm()
    
    return render(request, 'ticket_login.djhtml', {'form':form,
                                                       'error':error})

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
                       creator='ppssystem',#request.META['USERNAME'],
                       responsible_person='forner', 
                       comment='', solution='',keywords=''
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

#function for 'tickets/overview'
@login_required(login_url='/tickets/login/')
def show_ticket_list(request):
    print(request.user.username)
    groups = []
    for group in request.user.groups.all():
        groups.append(group.name)

    
    #search for open tickets to be displayed according to the
    #requesting user and the groups he's in 
    tickets = Ticket.objects.filter(Q(status='open'), 
                                Q(responsible_person=request.user.username) | 
                                Q(sector__in=groups))

    #return the template with the fetched data on display
    return render(request, 'ticket_overview.djhtml', {'tickets':tickets})

#function for 'tickets/d{1,4}'
def show_ticket_detail(request, ticketid):
    if request.method=="GET":
        ticket = Ticket.objects.get(ticketid=str(ticketid))
        ticket_dict = model_to_dict(ticket)
        detailform = DetailForm(initial=ticket_dict)
        editform = EditableDataForm(initial=ticket_dict)
        
        return render(request, 'ticket_detail.djhtml', {'detailform':detailform,
                                                        'editform':editform,
                                                        'readonly':"disabled"})
    #checks for the id in the database, fetch the ticket data and
    #show it in the template for ticket details

#function for 'tickets/d{1,4}/edit'
def edit_ticket_detail(request, ticketid):
    if request.method=="GET":
        ticket = Ticket.objects.get(ticketid=str(ticketid))
        ticket_dict = model_to_dict(ticket)
        detailform = DetailForm(initial=ticket_dict)
        editform = EditableDataForm(initial=ticket_dict)
        return render(request, 'ticket_detail.djhtml', {'detailform':detailform,
                                                        'editform':editform,
                                                        'readonly':""})
    #check if user may edit tickets, check for ticket id in the database, display
    #the ticket data and save any changes to the database on confirmation
    return HttpResponse("Edit details of %s" % (ticketid))



#function for 'tickets/search'
def search_tickets(request):
    if request.method=="GET":
        #check for valid input, search in the database and
        #fetch any results
        return HttpResponse("GET request detected")
    else:
        #display error page "Not a valid GET request(?)"
        return HttpResponse("NON GET request detected")
