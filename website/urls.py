from django.urls import path
from .views import home, contact, pricing

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('pricing/', pricing, name='pricing'),
]
