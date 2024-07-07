from typing import Any
from django.shortcuts import render
from django.views.generic.base import TemplateView
from artd_partner.models import Partner
from artd_paymentsway.models import PaymentsWayCredential, PaymentsWayTestData
from artd_paymentsway.utils import get_customer_ip
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


class PaymenstWayTest(TemplateView):
    template_name = "payments_way/test.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        pk = kwargs['pk']
        merchant_id = None
        api_key = None
        test_data = None
        partner = Partner.objects.get(pk=pk)
        if partner:
            credential = PaymentsWayCredential.objects.get(
                partner=partner,
            )
            if credential:
                merchant_id = credential.merchant_id
                api_key = credential.api_key
                if PaymentsWayTestData.objects.filter(
                    payments_way_credential=credential,
                ).count():
                    test_data = PaymentsWayTestData.objects.get(
                        payments_way_credential=credential,
                    )

                
        context.update({
            'partner': partner,
            'merchant_id': merchant_id,
            'api_key': api_key,
            'ip_address': get_customer_ip(self.request),
            'test_data': test_data,
        })
        return context 

@csrf_exempt
def payment_response(request):
    try:
        data = json.loads(request.body)
        print(data)
        
        return JsonResponse(
            {
                'message': 'Payment response processed successfully'
            }, 
            status=200
        )
    
    except Exception as e:
        print(str(e))
        return JsonResponse(
            {
                'error': 'Invalid JSON'
            }, 
            status=400
        )
