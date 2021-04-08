from django.conf.urls import url, include
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    url(r'^', include('orders.urls')),
    path('admin/', admin.site.urls),
]
