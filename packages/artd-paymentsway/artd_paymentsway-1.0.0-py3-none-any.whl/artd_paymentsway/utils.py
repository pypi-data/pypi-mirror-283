def get_customer_ip(request):
    try:
        ip = request.META.get('REMOTE_ADDR')
        forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded_for:
            ip = forwarded_for.split(',')[0]
        
        return ip
    except Exception as e:
        return None