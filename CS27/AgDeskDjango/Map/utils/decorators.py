from functools import wraps
from django.http import JsonResponse

def handle_view_errors(logger):
    """
    Decorator to handle exceptions in Django view functions and return appropriate JSON responses.

    Args:
        logger (Logger): Logger instance to log unexpected exceptions.

    Returns:
        function: Wrapped view function that handles errors gracefully.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            try:
                return func(request, *args, **kwargs)
            except ValueError as ve:
                # Handle known bad requests
                return JsonResponse({'error': str(ve)}, status=400)
            except Exception as e:
                # Log and return internal server error
                logger.error(f"Unhandled error in {func.__name__}: {e}", exc_info=True)
                return JsonResponse({'error': str(e)}, status=500)
        return wrapper
    return decorator