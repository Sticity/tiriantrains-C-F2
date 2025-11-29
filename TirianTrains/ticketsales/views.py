from django.shortcuts import render, redirect
from .models import Passenger, Ticket, Trip, ItineraryEntry, Route, Station
from .forms import PassengerForm, TicketForm, ItineraryEntryForm, SalesReportForm

from datetime import datetime

def format_duration(duration_time):
    hours = duration_time.hour
    minutes = duration_time.minute

    parts = []
    if hours > 0:
        parts.append(f'{hours} hour' + ('s' if hours > 1 else ''))
    if minutes > 0:
        parts.append(f'{minutes} minute' + ('s' if minutes > 1 else ''))

    return ' '.join(parts) if parts else '0 minutes'

# Main Query
def sales_reports(request):
    form = SalesReportForm(request.GET or None)
    sales = []

    if form.is_valid():
        d1 = form.cleaned_data['start_date']
        d2 = form.cleaned_data['end_date']
        
        sales = Ticket.objects.raw(
            '''
            SELECT
            ticketsales_ticket.id,
            CONCAT(origin.Name, ' -> ', destination.Name) AS Route,
            COUNT(ticketsales_ticket.id) AS Total_Tickets_Sold,
            SUM(ticketsales_route.Cost) AS Total_Revenue
            FROM ticketsales_ticket
            JOIN ticketsales_itineraryentry ON
            ticketsales_itineraryentry.ticketid = ticketsales_ticket.id
            JOIN ticketsales_trip ON ticketsales_trip.id = ticketsales_itineraryentry.tripid
            JOIN ticketsales_route ON ticketsales_route.id = ticketsales_trip.routeid
            JOIN ticketsales_station origin ON origin.id = ticketsales_route.id
            JOIN ticketsales_station destination ON destination.id = ticketsales_route.id
            WHERE ticketsales_ticket.Date BETWEEN %s AND %s
            GROUP BY ticketsales_route.id
            ORDER BY Total_Revenue DESC;
            ''',
            [d1,d2]
        )
    
    return render(request, 'sales_report.html', {'sales':sales,
                                                 'form':form})

# 5 Sample Queries
def general_statistics(request):
    tickets = Ticket.objects.all()
    passengers = Passenger.objects.all()

    passengers_bought = Passenger.objects.raw(
        # List of All the Customers and Amount of Tickets Bought
        '''
        SELECT
            ticketsales_passenger.id,
            CONCAT(ticketsales_passenger.Given_Name, ' ', ticketsales_passenger.Middle_Initial,
            '. ', ticketsales_passenger.Last_Name) AS Customer,
            COUNT(ticketsales_ticket.id) AS Tickets_Bought
        FROM ticketsales_passenger
        LEFT JOIN ticketsales_ticket ON
        ticketsales_passenger.id = ticketsales_ticket.customerid
        GROUP BY ticketsales_passenger.id
        ORDER BY Tickets_Bought DESC;
        '''
    )

    history_sherlock = Passenger.objects.raw(
        # Travel History for Sherlock Holmes
        '''
        SELECT
            ticketsales_passenger.id,
            CONCAT(ticketsales_passenger.Given_Name, ' ',
            ticketsales_passenger.Middle_Initial, '. ',
            ticketsales_passenger.Last_Name) AS Customer,
            ticketsales_ticket.id AS Ticket_ID,
            ticketsales_ticket.Date AS Date,
            ticketsales_route.Cost AS Ticket_Cost,
            CONCAT(origin.Name, ' -> ', destination.Name) AS Route,
            ticketsales_trip.Departure_Time AS Departure
        FROM ticketsales_passenger
        JOIN ticketsales_ticket ON ticketsales_ticket.customerid = ticketsales_passenger.id
        JOIN ticketsales_itineraryentry ON ticketsales_itineraryentry.ticketid = ticketsales_ticket.id
        JOIN ticketsales_trip ON ticketsales_trip.id = ticketsales_itineraryentry.tripid
        JOIN ticketsales_route ON ticketsales_route.id = ticketsales_trip.routeid
        JOIN ticketsales_station origin ON origin.id = ticketsales_route.originid
        JOIN ticketsales_station destination ON destination.id = ticketsales_route.destinationid
        WHERE CONCAT(ticketsales_passenger.Given_Name, ' ', ticketsales_passenger.Middle_Initial,
        '. ', ticketsales_passenger.Last_Name) = "Sherlock S. Holmes"
        ORDER BY ticketsales_ticket.Date;
        '''
    )

    route_gender = Passenger.objects.raw(
        # Route Popularity per Gender
        '''
        SELECT
            ticketsales_passenger.id,
            ticketsales_passenger.Gender,
            CONCAT(origin.Name, ' -> ', destination.Name) AS Route,
            COUNT(ticketsales_ticket.id) AS Total_Tickets
        FROM ticketsales_passenger
        JOIN ticketsales_ticket ON ticketsales_ticket.customerid = ticketsales_passenger.id
        JOIN ticketsales_itineraryentry ON ticketsales_itineraryentry.ticketid = ticketsales_ticket.id
        JOIN ticketsales_trip ON ticketsales_trip.id = ticketsales_itineraryentry.tripid
        JOIN ticketsales_route ON ticketsales_route.id = ticketsales_trip.routeid
        JOIN ticketsales_station origin ON origin.id = ticketsales_route.originid
        JOIN ticketsales_station destination ON destination.id = ticketsales_route.destinationid
        GROUP BY ticketsales_passenger.Gender, Route
        ORDER BY Total_Tickets DESC;
        '''
    )

    destination_gender = Passenger.objects.raw(
        # Destination per Gender
        '''
        SELECT
            ticketsales_passenger.id,
            ticketsales_passenger.Gender,
            destination.Name AS Destination,
            COUNT(ticketsales_ticket.id) AS Tickets_Bought
        FROM ticketsales_passenger
        JOIN ticketsales_ticket ON ticketsales_ticket.customerid = ticketsales_passenger.id
        JOIN ticketsales_itineraryentry ON ticketsales_itineraryentry.ticketid = ticketsales_ticket.id
        JOIN ticketsales_trip ON ticketsales_trip.id = ticketsales_itineraryentry.tripid
        JOIN ticketsales_route ON ticketsales_route.id = ticketsales_trip.routeid
        JOIN ticketsales_station destination ON destination.id = ticketsales_route.destinationid
        GROUP BY ticketsales_passenger.Gender, Destination
        ORDER BY ticketsales_passenger.Gender, Tickets_Bought DESC;
        '''
    )

    revenue_local = Ticket.objects.raw(
        # Revenue for Local / Route Tracker
        '''
        SELECT
            ticketsales_ticket.id,
            CONCAT(origin.Name, ' -> ', destination.Name) AS Route,
            COUNT(ticketsales_ticket.id) AS Total_Tickets_Sold,
            SUM(ticketsales_route.Cost) AS Total_Revenue
        FROM ticketsales_ticket
        JOIN ticketsales_itineraryentry ON ticketsales_itineraryentry.ticketid = ticketsales_ticket.id
        JOIN ticketsales_trip ON ticketsales_trip.id = ticketsales_itineraryentry.tripid
        JOIN ticketsales_route ON ticketsales_route.id = ticketsales_trip.routeid
        JOIN ticketsales_station origin ON origin.id = ticketsales_route.originid
        JOIN ticketsales_station destination ON destination.id = ticketsales_route.destinationid
        WHERE origin.Locality = 'Local' AND destination.Locality = 'Local'
        GROUP BY ticketsales_route.id
        ORDER BY Total_Revenue DESC;
        '''
    )

    return render(request, 'statistics.html', {'passengers_bought':passengers_bought,
                                               'history_sherlock':history_sherlock,
                                               'route_gender':route_gender,
                                               'destination_gender':destination_gender,
                                               'revenue_local':revenue_local})

# Full Database + Custom Queries + Ticket, Passenger, ItineraryEntry Creation
def full_database(request):
    if request.method == 'POST':

        # which form was submitted
        if 'passenger_submit' in request.POST:
            passenger_form = PassengerForm(request.POST)
            if passenger_form.is_valid():
                passenger_form.save()
                return redirect('ticketsales:full_database')

        elif 'ticket_submit' in request.POST:
            ticket_form = TicketForm(request.POST)
            if ticket_form.is_valid():
                ticket_form.save()
                return redirect('ticketsales:full_database')

        elif 'itinerary_submit' in request.POST:
            itinerary_form = ItineraryEntryForm(request.POST)
            if itinerary_form.is_valid():
                itinerary_form.save()
                return redirect('ticketsales:full_database')

    else:
        passenger_form = PassengerForm()
        ticket_form = TicketForm()
        itinerary_form = ItineraryEntryForm()

    # query data
    passengers = Passenger.objects.all()
    tickets = Ticket.objects.all()
    itinerary_entries = ItineraryEntry.objects.all()
    trips = Trip.objects.all()
    routes = Route.objects.all()
    stations = Station.objects.all()

    for r in routes:
        r.Duration = format_duration(r.Duration)

    return render(request, 'database_view.html', {'passengers':passengers,
                                                  'tickets':tickets,
                                                  'itinerary_entries':itinerary_entries,
                                                  'trips':trips,
                                                  'routes':routes,
                                                  'stations':stations,

                                                  'passenger_form':passenger_form,
                                                  'ticket_form':ticket_form,
                                                  'itinerary_form':itinerary_form})
    

# Ticket Details (replicates the table in proj case)

def calculate_arrival_time(dep_time, duration_time):
    dep_hour = dep_time.hour
    dep_minute = dep_time.minute

    dur_minutes = duration_time.hour * 60 + duration_time.minute

    total_minutes = dep_minute + dur_minutes
    arrival_hour = (dep_hour + total_minutes // 60) % 24
    arrival_minute = total_minutes % 60

    period = "a.m." if arrival_hour < 12 else "p.m."

    hour_12 = arrival_hour % 12
    if hour_12 == 0:
        hour_12 = 12

    return f"{hour_12}:{arrival_minute:02d} {period}"


def ticket(request, id):
    ticket = Ticket.objects.get(pk=id)
    passenger = Passenger.objects.get(pk=ticket.Customer_ID.id)
    itinerary_entries = ItineraryEntry.objects.filter(Ticket_ID=id)

    for entry in itinerary_entries:
        entry.Trip_ID.Arrival_Time = calculate_arrival_time(entry.Trip_ID.Departure_Time,entry.Trip_ID.Route_ID.Duration)
        entry.Trip_ID.Route_ID.Duration = format_duration(entry.Trip_ID.Route_ID.Duration)
    
    total_cost = sum(entry.Trip_ID.Route_ID.Cost for entry in itinerary_entries)

    return render(request, 'ticket.html', {'ticket':ticket,
                                           'passenger':passenger,
                                           'itinerary_entries':itinerary_entries,
                                           'total_cost':total_cost,
                                           })


