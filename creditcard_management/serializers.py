from rest_framework import serializers
from .models import CreditCard

class CreditCardSerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source="user.username")
	class Meta:
		model = CreditCard
		fields = ["id", "card_no", "cvv", "issued", "expiry", "user"]