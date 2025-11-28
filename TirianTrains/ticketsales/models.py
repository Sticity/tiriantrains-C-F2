from django.db import models

class Passenger(models.Model):
    gender_options = [
        ('None','None'),
        ('Male','Male'),
        ('Female','Female'),
        ('Rather not Disclose','Rather not Disclose')
    ]
    
    Given_Name = models.CharField(max_length=255)
    Last_Name = models.CharField(max_length=255)
    Middle_Initial = models.CharField(max_length=1)
    Birth_Date = models.DateTimeField()
    Gender = models.CharField(choices=gender_options)

class Ticket(models.Model):
    Customer_ID = models.ForeignKey(Passenger,null=True,on_delete=models.SET_NULL,db_column="customerid")
    Date = models.DateTimeField()
    Total_Cost = models.IntegerField(default=0)

class Trip(models.Model):
    Date = models.DateTimeField()
    Train_ID = models.IntegerField(default=0)
    Arrival_Time = models.TimeField()
    Departure_Time = models.TimeField()

class ItineraryEntry(models.Model):
    Ticket_ID = models.ForeignKey(Ticket,null=True,on_delete=models.SET_NULL)
    Trip_ID = models.ForeignKey(Trip,null=True,on_delete=models.SET_NULL)

class Station(models.Model):
    locality_options = [
        ('Local','Local'),
        ('Inter-town','Inter-town'),
    ]
    
    Name = models.CharField(max_length=255)
    Locality = models.CharField(choices=locality_options)


class Route(models.Model):
    Station_ID = models.ForeignKey(Station,null=True,on_delete=models.SET_NULL)
    Cost = models.IntegerField(default=0)
    Duration = models.TimeField()
