--List of all Customers and Amount of  Tickets Bought
SELECT  
    CONCAT(passenger.Given_Name, ' ', passenger.Middle_Initial, '. ', passenger.Last_Name) AS Customer,
    COUNT(ticket.Ticket_ID) AS `Tickets Bought`
FROM passenger
LEFT JOIN ticket ON passenger.Customer_ID = ticket.Customer_ID
GROUP BY passenger.Customer_ID
ORDER BY `Tickets Bought` DESC;


--Travel History for Sherlock Holmes

SELECT
    CONCAT(passenger.Given_Name, ' ', passenger.Middle_Initial, '. ', passenger.Last_Name) AS Customer,
    ticket.Ticket_ID AS `Ticket ID`,
    ticket.Date AS `Date`,
    ticket.Total_Cost AS `Ticket Cost`,
    CONCAT(origin.Name, ' -> ', destination.Name) AS Route,
    trip.Departure_Time,
    trip.Arrival_Time
FROM passenger
JOIN ticket ON ticket.Customer_ID = passenger.Customer_ID
JOIN itineraryentry ON itineraryentry.Ticket_ID = ticket.Ticket_ID
JOIN trip ON trip.Trip_ID = itineraryentry.Trip_ID
JOIN route ON route.Route_ID = trip.Route_ID
JOIN station origin ON origin.Station_ID = route.Origin_ID
JOIN station destination ON destination.Station_ID = route.Destination_ID
WHERE CONCAT(passenger.Given_Name, ' ', passenger.Middle_Initial, '. ', passenger.Last_Name) = "Sherlock S. Holmes"
ORDER BY ticket.Date;


--Route Popularity Per Gender
SELECT
    passenger.Gender,
    CONCAT(origin.Name, ' -> ', destination.Name) AS Route,
    COUNT(ticket.Ticket_ID) AS Total_Tickets
FROM passenger
JOIN ticket ON ticket.Customer_ID = passenger.Customer_ID
JOIN itineraryentry ON itineraryentry.Ticket_ID = ticket.Ticket_ID
JOIN trip ON trip.Trip_ID = itineraryentry.Trip_ID
JOIN route ON route.Route_ID = trip.Route_ID
JOIN station origin ON origin.Station_ID = route.Origin_ID
JOIN station destination ON destination.Station_ID = route.Destination_ID
GROUP BY passenger.Gender, Route
ORDER BY passenger.Gender, Total_Tickets DESC;


--Destination Popularity Per Gender

  SELECT
    passenger.Gender,
    destination.Name AS Destination,
    COUNT(ticket.Ticket_ID) AS `Tickets Bought`
FROM passenger
JOIN ticket ON ticket.Customer_ID = passenger.Customer_ID
JOIN itineraryentry ON itineraryentry.Ticket_ID = ticket.Ticket_ID
JOIN trip ON trip.Trip_ID = itineraryentry.Trip_ID
JOIN route ON route.Route_ID = trip.Route_ID
JOIN station destination ON destination.Station_ID = route.Destination_ID
GROUP BY passenger.Gender, Destination
ORDER BY passenger.Gender, `Tickets Bought` DESC;


-- Revenue for either Local or Inter-town(Change the where statement in Forms)
-- Also acts as Route tracker

SELECT
    CONCAT(origin.Name, ' -> ', destination.Name) AS Route,
    COUNT(ticket.Ticket_ID) AS `Total Tickets Sold`,
    SUM(ticket.Total_Cost) AS `Total Revenue`
FROM ticket
JOIN itineraryentry ON itineraryentry.Ticket_ID = ticket.Ticket_ID
JOIN trip ON trip.Trip_ID = itineraryentry.Trip_ID
JOIN route ON route.Route_ID = trip.Route_ID
JOIN station origin ON origin.Station_ID = route.Origin_ID
JOIN station destination ON destination.Station_ID = route.Destination_ID
WHERE origin.Locality = 'Local' AND destination.Locality = 'Local'
GROUP BY route.Route_ID
ORDER BY `Total Revenue` DESC;


--Revenue Report for Year

SELECT
    CONCAT(origin.Name, ' -> ', destination.Name) AS Route,
    COUNT(ticket.Ticket_ID) AS `Total Tickets Sold`,
    SUM(ticket.Total_Cost) AS `Total Revenue`
FROM ticket
JOIN itineraryentry ON itineraryentry.Ticket_ID = ticket.Ticket_ID
JOIN trip ON trip.Trip_ID = itineraryentry.Trip_ID
JOIN route ON route.Route_ID = trip.Route_ID
JOIN station origin ON origin.Station_ID = route.Origin_ID
JOIN station destination ON destination.Station_ID = route.Destination_ID
WHERE YEAR(ticket.Date) = '2025'
GROUP BY route.Route_ID
ORDER BY `Total Revenue` DESC;

--Revenue Report For Month

SELECT
    CONCAT(origin.Name, ' -> ', destination.Name) AS Route,
    COUNT(ticket.Ticket_ID) AS `Total Tickets Sold`,
    SUM(ticket.Total_Cost) AS `Total Revenue`
FROM ticket
JOIN itineraryentry ON itineraryentry.Ticket_ID = ticket.Ticket_ID
JOIN trip ON trip.Trip_ID = itineraryentry.Trip_ID
JOIN route ON route.Route_ID = trip.Route_ID
JOIN station origin ON origin.Station_ID = route.Origin_ID
JOIN station destination ON destination.Station_ID = route.Destination_ID
WHERE YEAR(ticket.Date) = 2025 AND MONTH(ticket.Date) = 2
GROUP BY route.Route_ID
ORDER BY `Total Revenue` DESC;




--Revenue Report For Week
--TBD

--Revenue Report for Day

SELECT
    CONCAT(origin.Name, ' -> ', destination.Name) AS Route,
    COUNT(ticket.Ticket_ID) AS `Total Tickets Sold`,
    SUM(ticket.Total_Cost) AS `Total Revenue`
FROM ticket
JOIN itineraryentry ON itineraryentry.Ticket_ID = ticket.Ticket_ID
JOIN trip ON trip.Trip_ID = itineraryentry.Trip_ID
JOIN route ON route.Route_ID = trip.Route_ID
JOIN station origin ON origin.Station_ID = route.Origin_ID
JOIN station destination ON destination.Station_ID = route.Destination_ID
WHERE ticket.Date = '2026-01-01'
GROUP BY route.Route_ID
ORDER BY `Total Revenue` DESC;
