from django.conf.urls import url#, include
from . import views
urlpatterns = [    
    url(r'^tickets/$', views.enter_ticket),
    url(r'^tickets/login/$', views.login_user, name='login_page'),
    url(r'^tickets/enter/$', views.enter_ticket),
    url(r'^tickets/overview/$', views.show_ticket_list, name='list_ticket'),
    url(r'^tickets/search/$', views.search_tickets, name='search_ticket'),
    url(r'^tickets/(\d{1,4})/edit$', views.edit_ticket_detail, name='edit_ticket'),
    url(r'^tickets/(\d{1,4})/close$', views.close_ticket, name='close_ticket'),
    url(r'^tickets/(\d{1,4})/$', views.show_ticket_detail, name='view_ticket'),
    url(r'^tickets/(\d{1,4})/image/$', views.show_ticket_image, name='view_image'),
    url(r'^tickets/(\d{1,4})/image/uploads/(.*)', views.get_ticket_image, name='get_image')
]