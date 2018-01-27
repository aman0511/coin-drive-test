from rest_framework import routers
from django.conf.urls import url

from .views import InventoryView, AccepetRejectInventory

routes = routers.DefaultRouter()
routes.register(r'', InventoryView)

urlpatterns = [

    url(r'^(?P<action_type>accept|reject)/(?P<id>\d+)/$',
        AccepetRejectInventory.as_view(), name="accept-reject"),

]

urlpatterns += routes.urls
