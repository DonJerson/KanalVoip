
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from kamailio import views as views2
from django.urls import path, include
from rest_framework import routers
from kamailio.api import *
from rest_framework_jwt.views import obtain_jwt_token

router = routers.SimpleRouter()
router.register(r'customer', CustomerViewSet, basename='customer')
router.register(r'subscriber', SubscriberViewSet, basename='subscriber')
router.register(r'recarga', RecargaViewSet, basename='recarga')
router.register(r'consumeApi', ApiUsageViewSet, basename='consumeApi')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token-auth/', obtain_jwt_token),
    path('getSub/', get_subscriber),
    path('updateBalance/', update_balance),
    path('newSubscriber/', new_subscriber),
    path('addDevice/', add_device),
    path('deleteDevice/', delete_device),
    path('newCustomer/', new_customer),
    path('api/',include(router.urls)),
    path('consumeApiOG/', ApiUsageOG),
    path('getSubscriberAdmin/', get_subscriber_admin),
    path('recargaOG/', RecargaOG),
    path('getHistory/', get_history),
    path('getHistoryAdmin/', get_history_admin),
    path('getRecargasHistory/', get_recargas_history),
    path('billCall/', bill_call),
    path('deleteSubscriber/', delete_subscriber),
    path('filterNumber/', filter_number),
]
