from django.http import JsonResponse
from django.views import View
from django.utils import timezone


class StatusView(View):
    """Public status endpoint to verify API is running"""
    
    def get(self, request):
        return JsonResponse({
            'status': 'healthy',
            'service': 'Gym Management API',
            'timestamp': timezone.now().isoformat(),
            'version': '1.0.0',
            'environment': 'production'
        })
