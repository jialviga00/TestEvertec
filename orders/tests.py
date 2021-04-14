from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from .models import Order


def create_order_test(amout=0, unit_value=0):
	"""
		Create a order
		@param amout [decimal]
		@param amout [int]
	"""
	order = Order()
	order.customer_name = 'TEST_CUSTOMER_NAME'
	order.customer_email = 'TEST_CUSTOMER_EMAIL'
	order.customer_mobile = '3008008080'
	order.amount = amout
	order.unit_value = unit_value
	order.total = amout * unit_value
	order.updated_at = timezone.now()
	order.status = 'CREATED'
	order.save()
	return order

class OrderModelTests(TestCase):

	def test_create_order(self):
		"""
			validate create order
		"""
		order = create_order_test()
		self.assertIs(Order.objects.all().count() > 0, True)

	def test_no_orders(self):
		"""
			If no orders exist, an appropriate message is displayed.
		"""
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No orders are available.")
		self.assertQuerysetEqual(response.context['orders_list'], [])

	def test_one_questions(self):
		"""
			The orders index page may display multiple orders.
		"""
		order1 = create_order_test()
		order2 = create_order_test()
		response = self.client.get(reverse('index'))
		self.assertQuerysetEqual(
			response.context['orders_list'],
			[order1, order2],
			transform=lambda x: x
		)

	def test_detail_order(self):
		"""
			validate detail view order
		"""
		order = create_order_test()
		url = reverse('detail', args=(order.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	def test_create_order(self):
		"""
			validate create view order
		"""
		url = reverse('create')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	def test_send_to_placetopay_failed(self):
		"""
			validate failed send to placetopay
		"""

		from lib.PlaceToPayUtilities import formartOrderDataForRequest
		from lib.PlaceToPay import PlaceToPay
		from time import time

		order = create_order_test()
		reference = str(int(time()))
		placeToPay = PlaceToPay()
		data = formartOrderDataForRequest(order, reference)
		placeToPay.sendToPlaceTopay(data)
		STATUS_PLACETOPAY = placeToPay.getResponseStatus()

		self.assertEqual(STATUS_PLACETOPAY, PlaceToPay._FAILED_EVERTEC)

	def test_send_to_placetopay_success(self):
		"""
			validate success send to placetopay
		"""
		
		from lib.PlaceToPayUtilities import formartOrderDataForRequest
		from lib.PlaceToPay import PlaceToPay
		from time import time

		order = create_order_test(2, 4500)
		reference = str(int(time()))
		placeToPay = PlaceToPay()
		data = formartOrderDataForRequest(order, reference)
		placeToPay.sendToPlaceTopay(data)
		STATUS_PLACETOPAY = placeToPay.getResponseStatus()

		self.assertEqual(STATUS_PLACETOPAY, PlaceToPay._SUCCESS_PLACETOPAY)