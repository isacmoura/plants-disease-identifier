from django.urls import path
from . import views

urlpatterns = [
    path('', views.__index__function, name='index'),
    path('predict', views.predict_plant_disease),
    path('feedback', views.predict_feedback),
]