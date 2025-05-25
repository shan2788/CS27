# services/history_service.py

import json
from django.utils.dateparse import parse_date

class HistoryService:
    """
    A service class for filtering historical records based on date range from a Django request.
    """

    @staticmethod
    def get_filtered_queryset(request, model_class, farm, logger):
        """
        Retrieve a queryset of model records filtered by farm and optionally by a start and end date.

        Args:
            request (HttpRequest): The incoming Django request, expected to contain a JSON body with
                                   optional 'start_date' and 'end_date' fields if POST.
            model_class (Django Model): The Django model class whose records are to be filtered.
            farm (Any): The farm instance used to filter records associated with it.
            logger (Logger): A logger instance used for error logging.

        Returns:
            QuerySet: A Django queryset filtered by the provided farm and (optionally) date range.

        Raises:
            ValueError: If the request body is invalid or cannot be parsed as JSON.
        """
        queryset = model_class.objects.filter(farm=farm).order_by('-created_at')

        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                start_date = data.get('start_date')
                end_date = data.get('end_date')

                if start_date:
                    queryset = queryset.filter(start_date__gte=parse_date(start_date))
                if end_date:
                    queryset = queryset.filter(end_date__lte=parse_date(end_date))
            except Exception as e:
                logger.error(f"Error parsing request body: {e}")
                raise ValueError("Invalid request")

        return queryset
