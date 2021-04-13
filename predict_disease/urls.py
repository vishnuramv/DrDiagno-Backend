from django.urls import path
from . import views
urlpatterns = [
	path('', views.PredictDisease.as_view(), name='predict'),
]
