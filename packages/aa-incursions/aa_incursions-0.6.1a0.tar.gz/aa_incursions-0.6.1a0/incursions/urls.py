from django.urls import path

from . import views

app_name = "incursions"

urlpatterns = [
    path('', views.index, name="index"),
    path('history/constellations', views.history_constellations, name="history_constellations"),
    path('history/incursions', views.history_incursions, name="history_incursions"),
]
