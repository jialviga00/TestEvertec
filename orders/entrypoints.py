from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect, HttpResponse
from orders.models import Order
from json import dumps


def getOrders(request):
    orders = Order.objects.all()
    response = {'records': [], 'status': 'SUCCESS'}
    for order in orders:
        response['records'].append({
            'id': order.id,
            'customer_name': order.customer_name,
            'customer_email': order.customer_email,
            'customer_mobile': order.customer_mobile,
            'status': order.status,
            'created_at': order.created_at,
            'updated_at': order.updated_at,
            'amount': order.amount,
            'total': order.total,
            'unit_value': order.unit_value,
        })

    return HttpResponse(dumps(response, cls=DjangoJSONEncoder), content_type='application/json')


def getOrderInformation(request):
    from lib.placetopay import getRequestInformation
    order = Order.objects.get(id=request.POST.get('orderId', None))
    request_information = getRequestInformation(order)
    STATUS_PLACETOPAY = request_information.get('status', {}).get('status', '__UNDEFINED_STATUS__')
    MESSAGE_PLACETOPAY = request_information.get('status', {}).get('message', '__UNDEFINED_MESSAGE__')
    order.status = STATUS_PLACETOPAY
    order.placetopay_message = MESSAGE_PLACETOPAY
    order.save()
    response = { 
        'status': 'SUCCESS',
        'status_placetopay': STATUS_PLACETOPAY,
        'message_placetopay': MESSAGE_PLACETOPAY,
    }
    return HttpResponse(dumps(response, cls=DjangoJSONEncoder), content_type='application/json')

def payOrder(request):
    
    from lib.placetopay import sendToPlaceTopay
    from time import time

    order = Order.objects.get(id=request.POST.get('orderId', None))
    FAILED_EVERTEC = "FAILED"
    SUCCESS_EVERTEC = "SUCCESS"
    SUCCESS_PLACETOPAY = "OK"
    FAILED_PLACETOPAY = "FAILED"

    if order.placetopay_process_url is not None and order.status not in ['CREATED', 'REJECTED']:
        response = {
            'exists': True,
            'message': 'PROCESSING',
            'status': SUCCESS_EVERTEC,
            'requestId': order.placetopay_request_id,
            'processUrl': order.placetopay_process_url,
        }
        return HttpResponse(dumps(response, cls=DjangoJSONEncoder), content_type='application/json')

    reference = str(int(time()))
    response_send = sendToPlaceTopay(order, reference)
    print(response_send)
    STATUS_PLACETOPAY = response_send.get('status', {}).get('status', '__UNDEFINED_STATUS__')
    MESSAGE_PLACETOPAY = response_send.get('status', {}).get('message', '__UNDEFINED_MESSAGE__')
    print(STATUS_PLACETOPAY, " :: ", MESSAGE_PLACETOPAY)
    if STATUS_PLACETOPAY == FAILED_PLACETOPAY:
        response = {
            'status': FAILED_EVERTEC,
            'message': "Se ha presentado un error, consulte con el administrador del sistema \n" + MESSAGE_PLACETOPAY,
        }
    elif STATUS_PLACETOPAY == SUCCESS_PLACETOPAY:
        order.reference = reference
        order.placetopay_request_id = response_send.get('requestId', '__UNDEFINED_REQUESTID__')
        order.placetopay_process_url = response_send.get('processUrl', '__UNDEFINED_PROCESSURL__')
        order.status = 'PROCESSING'
        order.save()
        response = {
            'status': SUCCESS_EVERTEC,
            'message': MESSAGE_PLACETOPAY,
            'requestId': response_send.get('requestId', '__UNDEFINED_REQUESTID__'),
            'processUrl': response_send.get('processUrl', '__UNDEFINED_PROCESSURL__'),
        }
    else:
        response = {
            'status': FAILED_EVERTEC,
            'message': "Se ha presentado un error,  con el administrador del sistema, no s epudo obtener una respuesta valida con la pasarela de pagos",
        }
    return HttpResponse(dumps(response, cls=DjangoJSONEncoder), content_type='application/json')