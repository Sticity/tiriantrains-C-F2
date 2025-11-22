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
    Total_Cost = models.DecimalField(default=0, max_digits=100, decimal_places=2)
