from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.get_name, name='search'),
    path('search/', include('search.urls')),
    path('admin/', admin.site.urls)
]

