from django.test import TestCase
from django.forms.models import model_to_dict
from django.contrib.auth.models import User, UserManager
from .models import Ticket
from django.test.client import Client
import datetime
import ticketsystem
import pytz
from django.core.files.base import File

class TicketTest(TestCase):
    TEST_DICT = {'sector':'Saperion', 'category':'Problem', 'subject':'Test Ticket', 'description':'This ticket was created for testing'}
    
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
        self.assertTrue(ticket_dict['sector']==self.TEST_DICT['sector'])
        self.assertTrue(ticket_dict['category']==self.TEST_DICT['category'])
        self.assertTrue(ticket_dict['subject']==self.TEST_DICT['subject'])
        self.assertTrue(ticket_dict['description']==self.TEST_DICT['description'])
        
        TicketTest.editingTestTicket(self, ticket_dict['ticketid'])        
    
    #test ticket creation with File upload;
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
        self.assertTrue(ticket_dict['sector']==self.TEST_DICT['sector'])
        self.assertTrue(ticket_dict['category']==self.TEST_DICT['category'])
        self.assertTrue(ticket_dict['subject']==self.TEST_DICT['subject'])
        self.assertTrue(ticket_dict['description']==self.TEST_DICT['description'])
        
        #check the ticket (dictionary) for a file reference in the image-field
        self.assertFalse(Ticket.objects.filter(image="*").count()>0)
        
    
    #expects ticketid to have a string representation
    def editingTestTicket(self, ticketid):
        REPLACE_DICT= {'status':{'open':'Offen'}, 'comment':'Testing stuff', 'solution':'', 'keywords':''}
        TicketTest.login(self)
        
                
        #check if exactly one ticket is in the db for the given ticket id
        tickets = Ticket.objects.filter(ticketid=str(ticketid))
        self.assertTrue(tickets.count()==1)
        
        ticket=tickets[0]        
        ticket_dict = model_to_dict(ticket)
        DATA_DICT = ticket_dict
        
        for key in REPLACE_DICT.keys():
            if key=='status':
                DATA_DICT[key]=REPLACE_DICT[key]['open']
            else:
                DATA_DICT[key]=REPLACE_DICT[key]
                
        DATA_DICT['submit']='confirm'
        DATA_DICT['image']=None
                        
        editResponse = self.client.post("/tickets/"+str(ticketid)+"/edit/", DATA_DICT)

        tickets = Ticket.objects.filter(ticketid=str(ticketid))
        ticket = tickets[0]
        ticket_dict = model_to_dict(ticket)
        
        self.assertTrue(ticket_dict['status'] in REPLACE_DICT['status'].keys())
        print(ticket_dict['comment']+"; "+REPLACE_DICT['comment'])
        self.assertTrue(ticket_dict['comment']==REPLACE_DICT['comment'])
        self.assertFalse(ticket_dict['solution']==REPLACE_DICT['solution'])
        
    def login(self):
        if User.objects.filter(username='ppssystem').count()==0:
            #create user for pps system
            testuser = User.objects.create_user('ppssystem', 'test@mail.de', 'preuuzalsor')
            #TODO: PERMISSIONS
            testuser.save()        
            
        #login via post to url /tickets/login/
        response=self.client.post("/tickets/login/", {'username':'ppssystem', 'password':'preuuzalsor'})
        
        #check if redirected
        self.assertTrue(response.status_code==302)
        #to the default redirect url: /tickets/overview/
        self.assertTrue(response.url=="/tickets/overview/")