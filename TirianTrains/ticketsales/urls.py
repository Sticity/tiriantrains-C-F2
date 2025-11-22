from django.urls import path
from .views import tickets_list, ticket

urlpatterns = [
    path('tickets/', tickets_list, name='list_view'),
    path('ticket/<int:id>/', ticket, name='detail_view'),
]

app_name = 'ticketsales'
