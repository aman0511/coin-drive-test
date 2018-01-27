from rest_framework import serializers
from .models import Inventory

class InventorySerilizer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        exclude = ()
        read_only_fields = ('status', 'action',)