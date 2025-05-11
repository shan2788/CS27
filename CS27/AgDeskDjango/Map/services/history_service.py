# services/history_service.py

import json
from django.utils.dateparse import parse_date

class HistoryService:

    @staticmethod
    def get_filtered_queryset(request, model_class, farm, logger):
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
