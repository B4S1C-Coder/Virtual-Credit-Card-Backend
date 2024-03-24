from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class CreditCard(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	card_no = models.CharField(max_length=16)
	cvv = models.CharField(max_length=3)
	issued = models.DateField('issued', default=datetime.now().date())
	expiry = models.DateField('expiry')

	def save(self, *args, **kwargs):
		# Assuming card is valid for 3 years
		if not self.expiry:
			self.expiry = (self.issued + timedelta(days=365 * 3))
		super().save(*args, **kwargs)

	def is_expired(self):
		return datetime.now().date() > self.expiry