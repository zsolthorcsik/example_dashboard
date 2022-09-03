from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('examply', views.examply, name='examply'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]
