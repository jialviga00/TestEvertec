from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from orders.models import Order
from django.urls import reverse

def index(request):
    orders_list = Order.objects.order_by('created_at')
    return render(
        request, 
        'orders/__index.html', 
        {
            'orders_list': orders_list,
        }
    )

def create(request):
    return render(
        request, 
        'orders/__create.html', 
        {}
    )

def detail(request, order_id):
    from orders.models import Order
    order = Order.objects.get(id=order_id)
    return render(
        request, 
        'orders/__detail.html', 
        {
            'order': order,
        }
    )

def save(request):
    from orders.models import Order
    import time

    order = Order()
    order.customer_name = request.POST.get('customer_name', '')
    order.customer_email = request.POST.get('customer_email', '')
    order.customer_mobile = request.POST.get('customer_mobile', '')
    order.amount = request.POST.get('amount', 0)
    order.total = request.POST.get('total', 0)
    order.unit_value = request.POST.get('unit_value', 0)
    order.status = 'CREATED'
    order.reference = str(int(time.time()))
    order.save()
    
    return HttpResponseRedirect(reverse('detail', args=(order.id, )))