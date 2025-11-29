from django.urls import path
from .views import sales_reports, general_statistics, full_database, ticket

urlpatterns = [
    path('', sales_reports, name='sales_reports'),
    path('statistics', general_statistics, name='general_statistics'),
    path('database', full_database, name='full_database'),
    path('ticket/<int:id>/', ticket, name='ticket_detail'),
]

app_name = 'ticketsales'
