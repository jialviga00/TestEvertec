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

    from lib.PlaceToPay import PlaceToPay
    
    try:
        order_id = request.POST.get('orderId')
        order = Order.objects.get(id=order_id)
        placeToPay = PlaceToPay()

        response_placetopay = placeToPay.getRequestInformation(order.placetopay_request_id)
        STATUS_PLACETOPAY = placeToPay.getResponseStatus()
        MESSAGE_PLACETOPAY = placeToPay.getResponseMessage()
        order.status = STATUS_PLACETOPAY
        order.placetopay_message = MESSAGE_PLACETOPAY
        order.save()

        response = { 
            'status': placeToPay._SUCCESS_EVERTEC,
            'status_placetopay': STATUS_PLACETOPAY,
            'message_placetopay': MESSAGE_PLACETOPAY,
        }
        return HttpResponse(dumps(response, cls=DjangoJSONEncoder), content_type='application/json')
    
    except Exception as e:
        response = {  'status': PlaceToPay._FAILED_EVERTEC, 'message': str(e) }
        return HttpResponse(dumps(response, cls=DjangoJSONEncoder), content_type='application/json')

def payOrder(request):
    
    from lib.PlaceToPay import PlaceToPay

    try:
        from lib.PlaceToPayUtilities import formartOrderDataForRequest
        from time import time

        order_id = request.POST.get('orderId')
        order = Order.objects.get(id=order_id)
        
        if order.placetopay_process_url is not None and order.status not in ['CREATED', 'REJECTED']:

            response = {
                'exists': True,
                'message': PlaceToPay._PROCESSING,
                'status': PlaceToPay._SUCCESS_EVERTEC,
                'requestId': order.placetopay_request_id,
                'processUrl': order.placetopay_process_url,
            }
            return HttpResponse(dumps(response, cls=DjangoJSONEncoder), content_type='application/json')
        
        placeToPay = PlaceToPay()
        reference = str(int(time()))
        data = formartOrderDataForRequest(order, reference)
        response_placetopay = placeToPay.sendToPlaceTopay(data)
        
        STATUS_PLACETOPAY = placeToPay.getResponseStatus()
        MESSAGE_PLACETOPAY = placeToPay.getResponseMessage()

        if STATUS_PLACETOPAY == PlaceToPay._FAILED_PLACETOPAY:
            response = {
                'status': PlaceToPay._FAILED_EVERTEC,
                'message': "Se ha presentado un error, consulte con el administrador del sistema \n" + MESSAGE_PLACETOPAY,
            }
        elif STATUS_PLACETOPAY == PlaceToPay._SUCCESS_PLACETOPAY:
            order.reference = reference
            order.placetopay_request_id = placeToPay.getResposeRequestId()
            order.placetopay_process_url = placeToPay.getResposeProcessUrl()
            order.status = PlaceToPay._PROCESSING
            order.save()
            response = {
                'status': PlaceToPay._SUCCESS_EVERTEC,
                'message': MESSAGE_PLACETOPAY,
                'requestId': placeToPay.getResposeRequestId(),
                'processUrl': placeToPay.getResposeProcessUrl(),
            }
        else:
            response = {
                'status': placeToPay._FAILED_EVERTEC,
                'message': "Se ha presentado un error,  con el administrador del sistema, no s epudo obtener una respuesta valida con la pasarela de pagos",
            }
        return HttpResponse(dumps(response, cls=DjangoJSONEncoder), content_type='application/json')

    except Exception as e:
        response = {  'status': PlaceToPay._FAILED_EVERTEC, 'message': str(e) }
        return HttpResponse(dumps(response, cls=DjangoJSONEncoder), content_type='application/json')