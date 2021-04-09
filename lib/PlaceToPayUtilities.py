from datetime import datetime, timedelta
from django.conf import settings

def formartOrderDataForRequest(order, reference):
    expiration = datetime.now() + timedelta(hours=5)
    data = {
        'locale' : 'es_CO',
        'buyer' : {
            'name' : order.customer_name,
            'email' : order.customer_email,
            'mobile' : order.customer_mobile,
        },
        'payment' : {
            'reference' : reference,
            'description' : 'Item Generico',
            'amount' : {
                'details' : [
                    {
                        'kind' : 'subtotal',
                        'amount' : str(order.total),
                    },
                ],
                'currency' : 'USD',
                'total' : str(order.total),
            },
            'items' : [
                {
                    'sku' : 123456,
                    'name' : 'Item Generico',
                    'category' : 'physical',
                    'qty' : str(order.amount),
                    'price' : str(order.unit_value),
                    'tax' : 0,
                },
            ],
            'allowPartial' : False,
        },
        'expiration' : expiration.isoformat(),
        'ipAddress' : '127.0.0.1',
        'userAgent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
        'returnUrl' : "{site_url}/detail/{order_id}/".format(site_url=settings.SITE_URL, order_id=order.id),
        'cancelUrl' : "{site_url}/detail/{order_id}/".format(site_url=settings.SITE_URL, order_id=order.id),
        'skipResult' : False,
        'noBuyerFill' : False,
        'captureAddress' : False,
        'paymentMethod' : None,
    }
    return data