from django.urls import path
from .views import lists, ticket

urlpatterns = [
    path('', lists, name='list_view'),
    path('ticket/<int:id>/', ticket, name='detail_view'),
]

app_name = 'ticketsales'
