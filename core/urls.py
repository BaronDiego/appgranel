from django.urls import path, include
from .views import home, HomeSinPrevilegios

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('index/', home, name='home'),
    path('sin_privilegios/', HomeSinPrevilegios.as_view(), name='sin_privilegios')
]