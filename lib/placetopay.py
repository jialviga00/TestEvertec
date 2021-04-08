from datetime import datetime, timedelta
from django.conf import settings
import requests

def getRequestInformation(order):
    PLACE_TO_PAY_CONFIG = settings.PLACE_TO_PAY_CONFIG
    URL = '{url}{request_id}'.format(url=PLACE_TO_PAY_CONFIG.get('URL'), request_id=order.placetopay_request_id)
    LOGIN = PLACE_TO_PAY_CONFIG.get('LOGIN')
    TRANKEY = PLACE_TO_PAY_CONFIG.get('TRANKEY')
    SEED = getSeed()

    order_data = {
        'auth' : {
            'login': LOGIN,
            'tranKey': digest(getNonce(False)+str(SEED)+TRANKEY),
            'nonce': getNonce(True),
            'seed': SEED,
        }
    }
    respose = requests.post(
        URL, 
        json=order_data
    )
    return respose.json()


def sendToPlaceTopay(order, reference):
    PLACE_TO_PAY_CONFIG = settings.PLACE_TO_PAY_CONFIG
    expiration = datetime.now() + timedelta(hours=5)
    order_data = {
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

    URL = PLACE_TO_PAY_CONFIG.get('URL')
    LOGIN = PLACE_TO_PAY_CONFIG.get('LOGIN')
    TRANKEY = PLACE_TO_PAY_CONFIG.get('TRANKEY')
    SEED = getSeed()

    order_data['auth'] = {
        'login': LOGIN,
        'tranKey': digest(getNonce(False)+str(SEED)+TRANKEY),
        'nonce': getNonce(True),
        'seed': SEED,
    }

    respose = requests.post(
        URL, 
        json=order_data
    )
    return respose.json()


def getNonce(decode=False):
    from base64 import b64encode
    tmpNonce = "TURCallXVmlNakJo".encode('utf-8')
    if decode is False:
        return tmpNonce.decode('utf-8')
    return b64encode(tmpNonce).decode('utf-8')

def getSeed():
    from datetime import datetime
    return datetime.now().isoformat()

def digest(cadena):
    from base64 import b64encode
    import hashlib
    h = hashlib.new("sha1", cadena.encode('utf-8'))
    return b64encode(h.digest()).decode('utf-8')