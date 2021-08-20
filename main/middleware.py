from main.models import IPAddress
class SaveIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            data =[dataResult for dataResult in  IPAddress.objects.all() if dataResult.ip_address == ip]
            if len(data) != 0 :
                id_address = IPAddress.objects.filter(ip_address = ip)[0]    
            else :   
                id_address = IPAddress(ip_address = ip)
                id_address.save()
            request.user.ip_address = id_address
        except:
            request.user.ip_address = ""
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response