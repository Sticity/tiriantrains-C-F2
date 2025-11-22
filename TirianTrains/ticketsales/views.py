from django.shortcuts import render
from .models import Passenger, Ticket
#from .forms import

def tickets_list(request):
    tickets = Ticket.objects.all()
    passengers = Passenger.objects.all()

    # Sample queries
    tickets = Ticket.objects.raw(
        [
        # Tickets that cost <= 100 Lion Coins (ascending)
        '''
        SELECT * FROM ticketsales_ticket, ticketsales_passenger
        WHERE Total_Cost <= 100
        AND ticketsales_passenger.id == ticketsales_ticket.customerid
        ORDER BY Total_Cost ASC
        ''',
        # Tickets bought by "Jane Doe"
        '''
        SELECT * FROM ticketsales_ticket, ticketsales_passenger
        WHERE CONCAT(ticketsales_passenger.Given_Name, " ",
        ticketsales_passenger.Last_Name) == "Jane Doe"
        AND ticketsales_ticket.customerid == ticketsales_passenger.id
        ''',
        ]
        [0] # SELECTOR (choose from index 0 to n)
    )

    return render(request, 'list_view.html', {'tickets':tickets,
                                              'passengers':passengers})

def ticket(request, id):
    ticket = Ticket.objects.get(pk=id)

    return render(request, 'ticket.html', {'ticket':ticket})
