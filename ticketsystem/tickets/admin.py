from django.contrib import admin
from .models import Ticket

#registering the model for Ticket with the admin site
admin.site.register(Ticket)