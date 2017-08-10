from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from tickets.models import Ticket
from tickets.forms import EnterTicketForm, LoginForm, DetailForm, EditableDataForm,\
    ClosingDataForm, SearchForm
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from django.utils import timezone
from _functools import reduce

#needed later
#from django.core.mail import send_mail, get_connection

#function for 'tickets/login'
def login_user(request):
    #initialize variables error and login_user
    error = False
    logged_in_user = None
    
    #when login form is submitted, validate fields 
    #and logout currently logged in user if necessary
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated():
                logout(request)
            #get user name and password from POST data and try to authenticate user
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            
            #if user was authenticated, log the user in and redirect to overview
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/tickets/overview/')
            #reset the form and set error to true
            else:
                error=True
                form = LoginForm()

    #if called normally
    else:
        #display currently logged in user, if existent
        if request.user.is_authenticated():
            logged_in_user = request.user
        #set empty login form
        form = LoginForm()
    
    return render(request, 'ticket_login.djhtml', {'form':form,
                                                   'error':error,
                                                   'login_user':logged_in_user})

#function for 'tickets/enter'
def enter_ticket(request):
    #initialize thx with false -> don't display thank you message
    infomsg=''
    if request.method=="POST":
        #set form as EnterTicketForm-Object with the POST-data
        form = EnterTicketForm(request.POST)

        #create an entry in the database with the entered data
        if form.is_valid():
            #get cleaned data and current system time
            cd = form.cleaned_data
            now = timezone.now()

            #initialize ticket object t with form data
            #ticket id increments automatically
            #fields mustn't be NULL -> initalized with '' (empty String)
            t = Ticket(sector=cd['sector'], category=cd['category'],
                       subject=cd['subject'], description=cd['description'],
                       creationdatetime = now, status='open',
                       creator=request.META['USERNAME'],
                       responsible_person='',
                       comment='', solution='',keywords=''
            )

            #save data set to database
            t.save()
            
            #reset form and display thank-you-message
            infomsg='Ticket erfolgreich erstellt!'
            form=EnterTicketForm()    
    else:
        #initialize empty form
        form = EnterTicketForm()
    
    #form: form to be displayed for ticket entering; thx: display thanks-message 
    return render(request, 'ticket_enter.djhtml', {'form':form, 'infomsg':infomsg})

#function for 'tickets/overview'
@login_required(login_url='/tickets/login/')
def show_ticket_list(request):
    
    #build list of all groups the user is part of
    groups = []
    for group in request.user.groups.all():
        groups.append(group.name)


    #search for open tickets to be displayed according to the
    #the requesting user
    query_user = Q(status='open') & Q(responsible_person=request.user.username)
    tickets_user = Ticket.objects.filter(query_user)
    
    #the groups the user is part of
    query_group = Q(status='open') & Q(responsible_person='') & Q(sector__in=groups)
    tickets_group = Ticket.objects.filter(query_group)
    
    
    #initialise infomsg
    infomsg=''
    
    if request.GET.get('status') :
        if request.GET['status']=='closed':
            infomsg="Ticket abgeschlossen!"
    
    
    #return the template with the fetched data on display
    return render(request, 'ticket_overview.djhtml', {'tickets_group':tickets_group,
                                                      'tickets_user':tickets_user,
                                                      'infomsg':infomsg})

#function for 'tickets/d{1,4}'
@login_required(login_url='/tickets/login/')
def show_ticket_detail(request, ticketid):
    if request.method=="GET":
        #query for ticket with given id
        try:
            ticket = Ticket.objects.get(ticketid=str(ticketid))
        #catch possible exceptions
        except Exception as e:
            if isinstance(e, Ticket.DoesNotExist):
                return render(request, 'ticket_error.djhtml', 
                              {'errormsg':"No Ticket found for this ID"})
            elif isinstance(e, Ticket.MultipleObjectsReturned):
                return render(request, 'ticket_error.djhtml', 
                              {'errormsg':"More than one ticket found for this ID"})
            else:
                return render(request, 'ticket_error.djhtml', 
                              {'errormsg':"An unknown error occured"})
        else:
            #convert ticket to dictionary with it's data
            ticket_dict = model_to_dict(ticket)
            
            #if user is ticket creator or has permissions to change tickets 
            if (request.META['USERNAME']==ticket_dict['creator'] 
                or request.user.has_perm('tickets.change_ticket')
                ):
                detailform = DetailForm(initial=ticket_dict)
                editform = EditableDataForm(initial=ticket_dict)
        
                return render(request, 'ticket_detail.djhtml', {'detailform':detailform,
                                                                'editform':editform})
            #if user is denied to view ticket data, return HTTP 403 Forbidden
            else:
                return HttpResponseForbidden()
    #if the request method is anything other than GET, return HTTP 403 Forbidden
    else:
        return HttpResponseForbidden()

"""
#view function for closing a ticket
#lets the user enter data for status, comment, solution and keywords
#submit
#submit option for closing the ticket -> validates the data and either
#closes the ticket or displays errors in the form fields 
#parameter: HttpRequest request, ticketid (must have a String representation)
#URL:'tickets/<ticketid>/close'
"""
@login_required(login_url='/tickets/login/')
def edit_ticket_detail(request, ticketid):
    #if user is ticket creator or has permissions to change tickets 
    if request.user.has_perm('tickets.change_ticket'):
        if request.method=="GET":
            #query for ticket with given id
            try:
                ticket = Ticket.objects.get(ticketid=str(ticketid))
            #catch possible exceptions
            except Exception as e:
                if isinstance(e, Ticket.DoesNotExist):
                    return render(request, 'ticket_error.djhtml', 
                              {'errormsg':"No Ticket found for this ID"})
                elif isinstance(e, Ticket.MultipleObjectsReturned):
                    return render(request, 'ticket_error.djhtml', 
                              {'errormsg':"More than one ticket found for this ID"})
                else:
                    return render(request, 'ticket_error.djhtml', 
                              {'errormsg':"An unknown error occured"})
            else:
                # FIXME: no ticket found -> id is illegal (when entered in browser bar)
                
                #convert ticket to dictionary with it's data
                ticket_dict = model_to_dict(ticket)
        
                detailform = DetailForm(initial=ticket_dict)
                editform = EditableDataForm(initial=ticket_dict)
                return render(request, 'ticket_edit.djhtml',
                              {'detailform':detailform,'editform':editform})
        elif request.method=="POST":
            infomsg=''
            #when editing is canceled (button "Übersicht" clicked) -> redirect
            if "cancel" in request.POST:
                return HttpResponseRedirect("/tickets/overview")
            #redirect to closing for when button "Abschließen" is clicked
            elif "close" in request.POST:
                return HttpResponseRedirect("/tickets/"+ticketid+"/close")
            #check input data and update database when button "Speichern" is clicked
            elif "confirm" in request.POST:
                editform = EditableDataForm(request.POST)
                try:
                    ticket = Ticket.objects.get(ticketid=str(ticketid))
                    #catch possible exceptions
                except Exception as e:
                    if isinstance(e, Ticket.DoesNotExist):
                        return render(request, 'ticket_error.djhtml', 
                              {'errormsg':"No Ticket found for this ID"})
                    elif isinstance(e, Ticket.MultipleObjectsReturned):
                        return render(request, 'ticket_error.djhtml', 
                              {'errormsg':"More than one ticket found for this ID"})
                    else:
                        return render(request, 'ticket_error.djhtml', 
                              {'errormsg':"An unknown error occured"})
                else:
                    detailform = DetailForm(initial=model_to_dict(ticket))
                    if editform.is_valid():
                        #get cleaned data from editable fields
                        cd = editform.cleaned_data
                        
                        Ticket.objects.filter(ticketid=str(ticketid)).update(
                                                                        status=cd['status'],
                                                                        comment=cd['comment'],
                                                                        solution = cd['solution'],
                                                                        keywords =cd['keywords']
                                                                        )
                        infomsg='Änderungen gespeichert!'
                    
                return render(request, 'ticket_edit.djhtml',
                              {'detailform':detailform,'editform':editform,
                               'infomsg':infomsg})
    else:
        # FIXME: display permission failure
        return HttpResponseForbidden()

"""
#view function for closing a ticket
#lets the user enter data for comment, solution and keywords
#additional submit options for redirecting to the ticket overview and ticket editing 
#submit option for closing the ticket -> validates the data and either
#updates the database and returns to the overview with a message
#or displays errors in the closing forms fields 
#parameter: HttpRequest request, ticketid (must have a String representation)
#URL:'tickets/<ticketid>/close'
"""
@login_required(login_url='/tickets/login/')
def close_ticket(request, ticketid):
    #Get-Request -> Clicked Button 'Abschließen' in ticket details
    if request.user.has_perm('tickets.change_ticket'):
        if request.method=="GET":
            #query for ticket with given id
            try:
                ticket = Ticket.objects.get(ticketid=str(ticketid))
            #catch possible exceptions
            except Exception as e:
                if isinstance(e, Ticket.DoesNotExist):
                    return HttpResponse("No Ticket")
                elif isinstance(e, Ticket.MultipleObjectsReturned):
                    return HttpResponse("Too many Tickets")
                else:
                    return HttpResponse("Unknown error")
            else:
                ticket.status='closed'
                
                # FIXME: no ticket found -> id is illegal (when entered in browser bar)
                
                #convert ticket to dictionary with it's data
                ticket_dict = model_to_dict(ticket)
                
                #if user has permissions to change tickets 
                if request.user.has_perm('tickets.change_ticket'):
                    detailform = DetailForm(initial=ticket_dict)
                    closeform = ClosingDataForm(initial=ticket_dict)
                    return render(request, 'ticket_close.djhtml', {'detailform':detailform,
                                                                    'closeform':closeform
                                                                    })
        #Post-Request -> Clicked Button 'Close'/'Abschließen' in closing template
        elif request.method=="POST":
            if "cancel" in request.POST:
                return HttpResponseRedirect("/tickets/overview")
            elif "edit" in request.POST:
                return HttpResponseRedirect("/tickets/"+ticketid+"/edit")
            elif "close" in request.POST:
                closeform=ClosingDataForm(request.POST)
                #if the data is valid, update ticket in database with entered data
                if closeform.is_valid():
                    Ticket.objects.filter(ticketid=str(ticketid)).update(comment=closeform.cleaned_data['comment'],
                                                                    solution = closeform.cleaned_data['solution'],
                                                                      keywords = closeform.cleaned_data['keywords'],
                                                                      closingdatetime = timezone.now(),
                                                                      status = "closed")
                    return HttpResponseRedirect('/tickets/overview/?status=closed')
                #if data is invalid, display the same template with error messages
                else:
                    ticket = Ticket.objects.get(ticketid=str(ticketid))
                    ticket_dict = model_to_dict(ticket)
                    detailform = DetailForm(initial=ticket_dict)
                    return render(request, 'ticket_close.djhtml',
                                  {'detailform':detailform, 'closeform':closeform})
        #block other request forms with a HTTP 403 (Forbidden) Response
        else:
            return HttpResponseForbidden()
    else:
        # FIXME: display permission failure
        return HttpResponse("Bitte einloggen!")


"""
#view function for ticket search
#searches for tickets which match user-entered criteria and
#returns a template with all results shown
#parameter: HttpRequest request
#URL:'tickets/search'
"""
@login_required(login_url='/tickets/login/')
def search_tickets(request):
    if request.method=="GET":
        #initialize searchform with GET data
        searchform = SearchForm(request.GET)
        
        #if entered data is valid, build a query and query the db for tickets
        if searchform.is_valid():
            searchterms = searchform.cleaned_data
            query_dict = {}
            
            #check all fields/keys for data entered, adjust keys depending on
            #their properties (full text, choice, char...?) and save the adjusted
            #key-value-pairs in query_dict
            for key in searchterms:
                if searchterms[key]!='' and searchterms[key] is not None:
                    # TODO: full text will only work with MySQL (or postgreSQL); 
                    # full text indices must be configured directly in db manager
                    
                    #use __search -> full text search for these fields
                    if key=='description' or key=='solution' or key=='comment':
                        key = key+'__search'
                    #use __contains -> SQL "LIKE '%...%'" for non-choice-fields
                    elif key!='sector' and key!='category' and key!='status':
                        key = key+'__contains'
                    #else: key=key, relevant for choice fields only
                    
                    query_dict[key]=searchterms[key]
            
            # build query from entered data via _functools.reduce and '&'
            # as a Q object
            # one liner form of version with one Q object
            query = reduce(lambda q,key: q&Q(**{key: query_dict[key]}), query_dict, Q())             
            tickets = Ticket.objects.filter(query)
            
            #get fieldnames from Ticket model
            fieldnames=[]
            
            #displayed error can be ignored as the _meta delivers methods to get
            #single or multiple fields from models
            for field in Ticket._meta.get_fields():
                fieldnames.append(field.verbose_name)
            
            #generate list from query results
            results=[]
            for ticket in tickets:
                results.append(model_to_dict(ticket))
            
            return render(request, 'ticket_search.djhtml', {'searchform':searchform,
                                                            'results':results, 
                                                            'fieldnames':fieldnames})
        else:
            return HttpResponse("Form not valid")
    #send Http403 to non GET requests
    else:
        return HttpResponseForbidden()

# OTHER VERSIONS OF BUILDING THE QUERY
# TODO: Remove comments in final version
            #Version with list of Q objects
#             querylist=[]
#             #add a new Q object for each key in query_dict
#             for key in query_dict:
#                 #initialize the Q object via unpacking (**) of a dictionary
#                 #here it's exactly 1 keyword argument (key = value)
#                 querylist.append(Q(**{key:query_dict[key]}))
#             
#             
#             #combines all Q-objects in querylist with AND (operator.and_),
#             #queries the database and stores the results in tickets
#             #see: https://docs.python.org/3/library/functools.html#functools.reduce
#             tickets = Ticket.objects.filter(reduce(operator.and_, querylist))

            #Version with one Q object which is build from all query conditions
#             query = Q()
#             
#             for key in query_dict:
#                 query &= Q(**{key:query_dict[key]})

