from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
	
	help = '_orders_ commands'

	def add_arguments(self, parser):
		parser.add_argument('_orders_option_', type=str, nargs='?', help='_orders_ option')

	def handle(self, *args, **options):
		
		if options['_orders_option_'] == 'simulatecron':
			
			from lib.PlaceToPayUtilities import formartOrderDataForRequest
			from lib.PlaceToPay import PlaceToPay
			from orders.models import Order
			from time import time
			
			orders = Order.objects.filter(status__in=['PENDING', 'PROCESSING'])

			if len(orders) > 0:
				for order in orders:
					print("searching order nro: ", order.placetopay_request_id)
					placeToPay = PlaceToPay()
					response_placetopay = placeToPay.getRequestInformation(order.placetopay_request_id)
					STATUS_PLACETOPAY = placeToPay.getResponseStatus()
					MESSAGE_PLACETOPAY = placeToPay.getResponseMessage()
					order.status = STATUS_PLACETOPAY
					order.placetopay_message = MESSAGE_PLACETOPAY
					order.save()
					print(" >> ", STATUS_PLACETOPAY, ":" , MESSAGE_PLACETOPAY)

				self.stdout.write(self.style.SUCCESS('Successfully _orders_ simulatecron'))
			else:
				self.stderr.write("orders with status PENDING not found")
		else:
			self.stderr.write("option not found")

