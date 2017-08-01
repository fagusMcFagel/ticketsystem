from django.http import Http404, HttpResponse#, HttpResponseRedirect
#from django.shortcuts import render

#needed later
#from django.core.mail import send_mail, get_connection

#function for 'tickets/enter'
def enter_ticket(request):
    if request.method=="POST":
        #read the entered data and create it as data set 
        #in the database with the next number/id
        return HttpResponse("POST request detected")
    else:
        #return the empty template with default values
        return HttpResponse("Not a POST request")
    return Http404

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
    #search for the tickets to be displayed according to the 
    #requesting user and return the template with the fetched data on display
    return HttpResponse("All the tickets")

#function for 'tickets/search'
def search_tickets(request):
    if request.method=="GET":
        #check for valid input, search in the database and 
        #fetch any results
        return HttpResponse("GET request detected")
    else:
        #display error page "Not a valid GET request(?)"
        return HttpResponse("NON GET request detected")