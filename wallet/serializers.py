from rest_framework import serializers
from .models import *

class PaymentWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentWalletB
        fields = "__all__"
