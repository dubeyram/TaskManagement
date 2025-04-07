"""
TimingMiddleware class for logging the time taken for each request.
"""
import time
import logging

logger = logging.getLogger(__name__)

class TimingMiddleware:
    """
    TimingMiddleware class for logging the time taken for each request.
    """
    def __init__(self, get_response):
        """
        Initializes the TimingMiddleware class.

        Args:
            get_response (function): The function to call to get the response.        
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Logs the time taken for each request.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            HttpResponse: The response.
        """
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time
        logger.info(f"[TimingMiddleware] {request.path} took {duration:.2f}s")
        
        return response
