from celery import shared_task
from .views import get_ndvi_image_binary
import logging

logger = logging.getLogger(__name__)

@shared_task
def update_ndvi_cache(geometry, start_date, end_date, evalscript):
    """
    Update the NDVI cache for a specific geometry and time range.
    """
    try:
        logger.info("Updating NDVI cache...")
        get_ndvi_image_binary(geometry, start_date, end_date, evalscript)
        logger.info("NDVI cache updated successfully.")
    except Exception as e:
        logger.error(f"Error updating NDVI cache: {e}")