from django.http.response import HttpResponseRedirect

def redir_to_tickets(request):
    return HttpResponseRedirect('tickets/overview/')