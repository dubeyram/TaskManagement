"""
LoggerMiddleware class for logging the incoming requests.
"""
import logging

logger = logging.getLogger(__name__)

class LoggerMiddleware:
    """
    LoggerMiddleware class for logging the incoming requests.
    """
    def __init__(self, get_response):
        """
        Initializes the LoggerMiddleware class.

        Args:
            get_response (function): The function to call to get the response.
        """
        self.get_response = get_response
        logger.info("LoggerMiddleware initialized")

    def __call__(self, request):
        """
        Logs the incoming request.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            HttpResponse: The response.
        """
        logger.info(f"[LoggerMiddleware] Incoming {request.method} request to {request.path}")
        response = self.get_response(request)
        return response
