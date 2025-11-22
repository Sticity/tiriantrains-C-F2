from django.contrib import admin
from .models import Passenger, Ticket

# Register your models here.
class PassengerAdmin(admin.ModelAdmin):
    model = Passenger

    list_display = ('id','Given_Name','Middle_Initial','Last_Name',)
    list_filter = ('Given_Name','Middle_Initial','Last_Name',)

class TicketAdmin(admin.ModelAdmin):
    model = Ticket

    list_display = ('id','Customer_ID__id',)

admin.site.register(Passenger, PassengerAdmin)
admin.site.register(Ticket, TicketAdmin)

