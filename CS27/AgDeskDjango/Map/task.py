from celery import shared_task
from .views import get_ndvi_image_binary
import logging
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

@shared_task
def update_ndvi_cache(geometry, start_date, end_date, evalscript):
    """
    Celery 任务：强制刷新并写入 NDVI 图像缓存（无返回，仅存储）。
    """
    async def run():
        async with aiohttp.ClientSession() as session:
            await get_ndvi_image_binary(
                session=session,
                geometry=geometry,
                start_date=start_date,
                end_date=end_date,
                evalscript=evalscript,
                use_cache=True  # ✅ 使用缓存逻辑写入
            )

    try:
        logger.info("Updating NDVI cache...")
        asyncio.run(run())
        logger.info("NDVI cache updated successfully.")
    except Exception as e:
        logger.error(f"Error updating NDVI cache: {e}")
