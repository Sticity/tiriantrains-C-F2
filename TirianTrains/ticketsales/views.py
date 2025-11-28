from django.shortcuts import render
from .models import Passenger, Ticket, Trip, ItineraryEntry, Route, Station
#from .forms import

# Sample queries
def lists(request):
    tickets = Ticket.objects.all()
    passengers = Passenger.objects.all()

    tickets = Ticket.objects.raw(
        [
        # Top 5 Tickets that have the most buyers
        # | Ticket ID | Total Cost | No. of Buyers |
        '''
        SELECT * FROM ticketsales_ticket, ticketsales_passenger
        WHERE Total_Cost <= 100
        AND ticketsales_passenger.id == ticketsales_ticket.customerid
        ORDER BY Total_Cost ASC
        ''',
        # Most expensive tickets (lim=10, ascending)
        # | Ticket ID | Total Cost | Buyers |

        # Passenger organized by gender (M)
        # | Ticket ID | Total Cost | Passenger Name |

        
        '''
        SELECT * FROM ticketsales_ticket, ticketsales_passenger
        WHERE CONCAT(ticketsales_passenger.Given_Name, " ",
        ticketsales_passenger.Last_Name) == "Jane Doe"
        AND ticketsales_ticket.customerid == ticketsales_passenger.id
        ''',
        
        # Tickets with Trips located inside Inter-town
        # | Ticket ID | Duration | Locality |
        
        
        # Trips that don't have an attributed Ticket
        # | Trip ID | Train ID | Date | Arrival Time | Departure Time |
        
        ]
        [0] # SELECTOR (choose from index 0 to n-1)
    )

    return render(request, 'list_view.html', {'tickets':tickets,
                                              'passengers':passengers})
# Ticket Details (includes everything else)
def ticket(request, id):
    ticket = Ticket.objects.get(pk=id)

    return render(request, 'ticket.html', {'ticket':ticket})

# Trip Details 

#def trips(request, id):
    
