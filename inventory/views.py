from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, views, exceptions, response

from . import models as inv_model
from . import serializers as inv_serializer

from account.models import UserMixIn
from account.permissions import IsStoreManager


class InventoryView(viewsets.ModelViewSet):
    model = inv_model.Inventory
    queryset = model.objects.all()
    serializer_class = inv_serializer.InventorySerilizer

    def perform_create(self, serializer):
        user = self.request.user
        if UserMixIn.is_user_store_manager(user):
            serializer.validated_data['status'] = inv_model.Inventory.ACCEPT
        elif UserMixIn.is_user_department_manager(user):
            serializer.validated_data['status'] = inv_model.Inventory.PENDING
        serializer.validated_data['action'] = inv_model.Inventory.CREATE
        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        if UserMixIn.is_user_store_manager(user):
            serializer.validated_data['status'] = inv_model.Inventory.ACCEPT
        elif UserMixIn.is_user_department_manager(user):
            serializer.validated_data['status'] = inv_model.Inventory.PENDING
        serializer.validated_data['action'] = inv_model.Inventory.UPDATE
        serializer.save()

    def perform_destroy(self, serializer):
        user = self.request.user
        if UserMixIn.is_user_store_manager(user):
            serializer.validated_data['status'] = inv_model.Inventory.ACCEPT
        elif UserMixIn.is_user_department_manager(user):
            serializer.validated_data['status'] = inv_model.Inventory.PENDING
        serializer.validated_data['action'] = inv_model.Inventory.DELETE
        serializer.save()


class AccepetRejectInventory(views.APIView):
    """ accept or reject inventory"""
    permission_classes = (
        permissions.IsAuthenticated, IsStoreManager,
    )

    def post(self, request, *args, **kwargs):
        action_name = kwargs['action_type']
        try:
            inventory = inv_model.Inventory.objects.get(id=kwargs['id'])
        except inv_model.Inventory.DoesNotExist:
            raise exceptions.ParseError({'details':"Invalid id"})
       
        if action_name == "accept":
            update_data = inventory.update_data
            for key, value in update_data:
                setattr(inventory, key, value)
            inventory.status = inv_model.Inventory.ACCEPT
            inventory.save()
        else:
            inventory.status = inv_model.Inventory.PENDING
            inventory.save()
        return response.Response({'details': "Inventroy updated successfully."})
