from django.test import TestCase
from django.forms.models import model_to_dict
from django.contrib.auth.models import Permission, User, UserManager, Group
from .models import Ticket
from django.test.client import Client
import datetime
import ticketsystem
import pytz
from django.core.files.base import File
from django.utils import timezone

class TicketTest(TestCase):
    TEST_DICT = {'sector':Group.objects.get(name='Saperion'), 'category':'Problem', 'subject':'Test Ticket', 'description':'This ticket was created for testing'}
    
    def setUp(self):
        #create group for "Saperion"
        testgroup = Group.objects.create(id=1, name='Saperion', permissions='')
        testgroup.save()
    
    #test for ticket creation without file upload
    def testEnterTicket_noFile(self):
        TicketTest.login(self) 
        #init dictionary with test values
        #create a new ticket via post to url /tickets/enter/
        enter_Response = self.client.post("/tickets/enter/", {'sector':self.TEST_DICT['sector'], 'category':self.TEST_DICT['category'], 'subject':self.TEST_DICT['subject'], 'description':self.TEST_DICT['description']}, USERNAME = 'Mustermann')
        
        tickets = Ticket.objects.all()

        #check if exactly one ticket is in the db
        self.assertTrue(tickets.count()==1)
        
        #get ticket object from queryset
        ticket=tickets[0]    
        ticket_dict = model_to_dict(ticket)
        
        #check if ticket was created in the last second
        self.assertTrue(pytz.utc.localize(datetime.datetime.utcnow())-ticket_dict['creationdatetime']<=datetime.timedelta(seconds=1))
        
        #check if the values of the ticket are the same as for creation
        self.assertTrue(ticket_dict['sector']==self.TEST_DICT['sector'].id)
        self.assertTrue(ticket_dict['category']==self.TEST_DICT['category'])
        self.assertTrue(ticket_dict['subject']==self.TEST_DICT['subject'])
        self.assertTrue(ticket_dict['description']==self.TEST_DICT['description'])
    
    
    #test for ticket creation with File upload;
    def testEnterTicket_File(self):
        TicketTest.login(self) 
        FILE_DIR = 'C:/GitRepos/ticketsystem/ticketsystem/testFiles'
        
        #INCORRECT upload -> not an Image File (here *.txt)
        start_count = Ticket.objects.all().count()
        with open(FILE_DIR+'/testTxt.txt', "rb") as errFO:
            self.assertFalse(errFO==None)
            enter_Response = self.client.post("/tickets/enter/", {'sector':self.TEST_DICT['sector'], 'category':self.TEST_DICT['category'], 'subject':self.TEST_DICT['subject'], 'description':self.TEST_DICT['description'], 'image':errFO}, USERNAME = 'Mustermann')

        tickets = Ticket.objects.all()
        
        #count should remain the same, no ticket should be created
        self.assertTrue(tickets.count()==start_count)
        
        #CORRECT upload -> Image File (here *.bmp)
        #a ticket should be created with the image in the corresponding db field
        start_count = Ticket.objects.all().count()
        with open(FILE_DIR+'/testBMP.bmp', "rb") as imgFO:
            self.assertFalse(imgFO==None)
            enter_Response = self.client.post("/tickets/enter/", {'sector':self.TEST_DICT['sector'], 'category':self.TEST_DICT['category'], 'subject':self.TEST_DICT['subject'], 'description':self.TEST_DICT['description'], 'image':imgFO}, USERNAME = 'Mustermann')
        
        tickets = Ticket.objects.all()
        self.assertTrue(tickets.count()==start_count+1)
        
        #get ticket object from queryset
        ticket=tickets[0]
        self.assertTrue(ticket!=None)
        
        ticket_dict = model_to_dict(ticket)
        
        #check if ticket was created in the last second
        self.assertTrue(pytz.utc.localize(datetime.datetime.utcnow())-ticket_dict['creationdatetime']<=datetime.timedelta(seconds=1))
        
        #check if the values of the ticket are the same as for creation
        self.assertTrue(ticket_dict['sector']==self.TEST_DICT['sector'].id)
        self.assertTrue(ticket_dict['category']==self.TEST_DICT['category'])
        self.assertTrue(ticket_dict['subject']==self.TEST_DICT['subject'])
        self.assertTrue(ticket_dict['description']==self.TEST_DICT['description'])
        
        #check the ticket (dictionary) for a file reference in the image-field
        self.assertFalse(Ticket.objects.filter(image="*").count()>0)
        

    #test for editing a ticket's data
    def testEditTicket(self):
        #init dictionary with ticket data keys/fields and values to set them to
        REPLACE_DICT= {'status': 'open', 'comment':'Testing stuff', 'solution':'This is a test solution', 'keywords':''}
        
        #init ticket data for test ticket and create test ticket in db
        ticket_data = {'sector':Group.objects.get(name__contains='Saperion'), 'category': 'Problem', 'subject':'Editing Tickets', 'description':'Test for editing tickets'}
        now = timezone.now()
        t = Ticket(sector=ticket_data['sector'], category=ticket_data['category'],
                subject=ticket_data['subject'], description=ticket_data['description'],
                creationdatetime = now, status='open',
                creator='ppssystem',
                responsible_person=None,
                comment='', solution='',keywords='',
                image=''
            )
        t.save()
        
        #login user
        TicketTest.login(self)
                
        #check if exactly one ticket is in the db for the given ticket id
        tickets = Ticket.objects.filter(subject='Editing Tickets')
        self.assertTrue(tickets.count()==1)
        
        ticket=tickets[0]        
        ticket_dict = model_to_dict(ticket)
        DATA_DICT = ticket_dict
        
        for key in REPLACE_DICT.keys():
                DATA_DICT[key]=REPLACE_DICT[key]
        
        DATA_DICT['subject']='An alternative subject'
        DATA_DICT['confirm']='confirm'
        DATA_DICT['image']=None
                        
        editResponse = self.client.post("/tickets/"+str(ticket_dict['ticketid'])+"/edit/", DATA_DICT)

        tickets = Ticket.objects.filter(ticketid=ticket_dict['ticketid'])
        ticket = tickets[0]
        ticket_dict = model_to_dict(ticket)
        self.assertFalse(ticket_dict['subject']==DATA_DICT['subject'])
        self.assertTrue(ticket_dict['status']==DATA_DICT['status'])
        self.assertTrue(ticket_dict['comment']==DATA_DICT['comment'])
        self.assertTrue(ticket_dict['solution']==DATA_DICT['solution'])
    
    
    #test for closing a ticket
    def testCloseTicket(self):
                
        #init ticket data for test ticket and create test ticket in db
        ticket_data = {'sector': Group.objects.get(name__contains='Saperion'), 'category': 'Problem', 'subject':'Closing Tickets', 'description':'Test for editing tickets'}
        now = timezone.now()
        t = Ticket(sector=ticket_data['sector'], category=ticket_data['category'],
                subject=ticket_data['subject'], description=ticket_data['description'],
                creationdatetime = now, status='open',
                creator='ppssystem',
                responsible_person=None,
                comment='', solution='',keywords='', 
                image=''
            )
        t.save()
        
        t_dict=model_to_dict(t)
        
        #login user
        TicketTest.login(self)
        
        #check if exactly one ticket is in the db for the given ticket id
        tickets = Ticket.objects.filter(subject='Closing Tickets')
        self.assertTrue(tickets.count()==1)
        
        ticket=tickets[0]        
        ticket_dict = model_to_dict(ticket)
        DATA_DICT = ticket_dict
        DATA_DICT.pop('image')
        
        DATA_DICT['status']='open'
        DATA_DICT['comment']='This is a useful comment'
        DATA_DICT['solution']='The solution was to turn it off and on again'
        DATA_DICT['close']='close'
        DATA_DICT['keywords']=''        
        
              
        closeResponse = self.client.post("/tickets/"+str(ticket_dict['ticketid'])+"/close/", DATA_DICT)
        
        t1 = Ticket.objects.get(ticketid=ticket_dict['ticketid'])
        t1_dict = model_to_dict(t1)
        self.assertTrue(t_dict['status']==t1_dict['status'])
        self.assertTrue(t_dict['comment']==t1_dict['comment'])
        self.assertTrue(t_dict['solution']==t1_dict['solution'])
        self.assertTrue(t_dict['keywords']==t1_dict['keywords'])
        
        DATA_DICT['status']='closed'
        DATA_DICT['comment']='This is a useful comment'
        DATA_DICT['solution']='The solution was to turn it off and on again'
        DATA_DICT['keywords']=''        
        
        closeResponse = self.client.post("/tickets/"+str(ticket_dict['ticketid'])+"/close/", DATA_DICT)
        
        t2 = Ticket.objects.get(ticketid=ticket_dict['ticketid'])
        t2_dict = model_to_dict(t2)
        self.assertTrue(t_dict['status']==t2_dict['status'])
        self.assertTrue(t_dict['comment']==t2_dict['comment'])
        self.assertTrue(t_dict['solution']==t2_dict['solution'])
        self.assertTrue(t_dict['keywords']==t2_dict['keywords'])
        
        DATA_DICT['status']='closed'
        DATA_DICT['comment']='This is a useful comment'
        DATA_DICT['solution']='The solution was to turn it off and on again'
        DATA_DICT['keywords']='test, ticket, solution, closed'        
        
        closeResponse = self.client.post("/tickets/"+str(ticket_dict['ticketid'])+"/close/", DATA_DICT)
        
        t3 = Ticket.objects.get(ticketid=ticket_dict['ticketid'])
        t3_dict = model_to_dict(t3)
        self.assertFalse(t_dict['status']==t3_dict['status'])
        self.assertFalse(t_dict['comment']==t3_dict['comment'])
        self.assertFalse(t_dict['solution']==t3_dict['solution'])
        self.assertFalse(t_dict['keywords']==t3_dict['keywords'])
        
        
    #function to create a test user if none exists and log the test user in
    def login(self):
        if User.objects.filter(username='ppssystem').count()==0:
            #create user for pps system
            testuser = User.objects.create_user('ppssystem', 'test@mail.de', 'preuuzalsor')
            permissions = [Permission.objects.get(codename='add_ticket'), Permission.objects.get(codename='change_ticket'), Permission.objects.get(codename='delete_ticket')]
            testuser.user_permissions.add(permissions[0], permissions[1], permissions[2])
            testuser.save()

            
        #login via post to url /tickets/login/
        response=self.client.post("/tickets/login/", {'username':'ppssystem', 'password':'preuuzalsor'})
        
        #check if redirected
        self.assertTrue(response.status_code==302)
        #to the default redirect url: /tickets/overview/
        self.assertTrue(response.url=="/tickets/overview/")