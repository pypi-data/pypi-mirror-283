from django.contrib import admin
from artd_paymentsway.models import PaymentsWayCredential, PaymentsWayTestData



@admin.register(PaymentsWayCredential)
class PaymentsWayCredentialAdmin(admin.ModelAdmin):
    list_display = [
        'partner', 
        'merchant_id',  
        'status', 
        'created_at', 
        'updated_at',
    ]

@admin.register(PaymentsWayTestData)
class PaymentsWayTestDataAdmin(admin.ModelAdmin):
    list_display = [
        'payments_way_credential',
        'status',
        'created_at',
        'updated_at',
    ]