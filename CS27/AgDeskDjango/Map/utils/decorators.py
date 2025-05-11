from functools import wraps
from django.http import JsonResponse

def handle_view_errors(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            try:
                return func(request, *args, **kwargs)
            except ValueError as ve:
                return JsonResponse({'error': str(ve)}, status=400)
            except Exception as e:
                logger.error(f"Unhandled error in {func.__name__}: {e}", exc_info=True)
                return JsonResponse({'error': str(e)}, status=500)
        return wrapper
    return decorator
