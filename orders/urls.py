from django.conf.urls import url, include
from django.urls import path
from . import views
from . import entrypoints

urlpatterns = [
    path('', views.index, name='index'),
    path('save/', views.save, name='save'),
    url(r'^create/', views.create, name='create'),
    path('detail/<str:order_id>/', views.detail, name='detail'),
    url(r'^entrypoint/getOrders/$', entrypoints.getOrders, name='getOrders'),
    url(r'^entrypoint/payOrder/$', entrypoints.payOrder, name='payOrder'),
    url(r'^entrypoint/getOrderInformation/$', entrypoints.getOrderInformation, name='getOrderInformation'),
]