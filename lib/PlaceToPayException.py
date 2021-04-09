class PlaceToPayException(Exception):
	"""
		Exception raised for errors in the PlaceToPay.

		Attributes:
			@message -- explanation of the error
	"""
	def __init__(self, message=""):
		self.message = message
		super().__init__(self.message)

	def __str__(self):
		return f'PlaceToPayException: {self.message}'