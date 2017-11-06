# Django
from django.contrib import admin
# local Django
from .models import Ticket, Measures

#registering the model for Ticket with the admin site
admin.site.register(Ticket)
admin.site.register(Measures)