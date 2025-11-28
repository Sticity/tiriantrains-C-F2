from django.contrib import admin
from .models import Passenger, Ticket, Trip, ItineraryEntry, Route, Station

# Register your models here.
class PassengerAdmin(admin.ModelAdmin):
    model = Passenger

    list_display = ('id','Given_Name','Middle_Initial','Last_Name',)
    list_filter = ('Given_Name','Middle_Initial','Last_Name',)

class TicketAdmin(admin.ModelAdmin):
    model = Ticket

    list_display = ('id','Customer_ID__id',)

class TripAdmin(admin.ModelAdmin):
    model = Trip

    list_display = ('id',)

class ItineraryEntryAdmin(admin.ModelAdmin):
    model = ItineraryEntry

    list_display = ('Ticket_ID__id','Trip_ID__id',)
    list_filter = ('Ticket_ID__id','Trip_ID__id',)

class RouteAdmin(admin.ModelAdmin):
    model = Route

    list_display = ('id',)

class StationAdmin(admin.ModelAdmin):
    model = Station

    list_display = ('id','Locality',)
    list_filter = ('Locality',)

admin.site.register(Passenger, PassengerAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(ItineraryEntry, ItineraryEntryAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Station, StationAdmin)
