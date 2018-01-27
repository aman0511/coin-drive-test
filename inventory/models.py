from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class Inventory(models.Model):
    """ inventory model """
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

    ACTION_CHOICE = (
        (CREATE, "Create New Invnetory"),
        (UPDATE, "Update Inventory"),
        (DELETE, "Delete Inventory")
    )

    PENDING = "PENDING"
    ACCEPT = "ACCEPT"

    STATUS_CHOICE = (
        (PENDING, "Pending"),
        (ACCEPT, "Accept")
    )

    name = models.CharField(max_length=255)
    vendor = models.ForeignKey(
        "vendor.Vendors", related_name="inventroy", on_delete=models.CASCADE)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    batch_num = models.CharField(max_length=255)
    batch_date = models.DateField()
    quantity = models.PositiveIntegerField()

    ## contain new update data 
    update_data = JSONField(null=True, blank=True)
 
    status = models.CharField(max_length=255, choices=STATUS_CHOICE)
    action = models.CharField(max_length=255, choices=ACTION_CHOICE)
