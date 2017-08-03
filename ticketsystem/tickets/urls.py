from django.conf.urls import url#, include
from . import views
urlpatterns = [    
    url(r'^tickets/login/$', views.login_user),
    url(r'^tickets/enter/$', views.enter_ticket),
    url(r'^tickets/overview/$', views.show_ticket_list),
    url(r'^tickets/search/$', views.search_tickets),
    url(r'^tickets/(\d{1,4})/edit$', views.edit_ticket_detail, name='edit_ticket'),
    url(r'^tickets/(\d{1,4})/$', views.show_ticket_detail, name='view_ticket'),
]