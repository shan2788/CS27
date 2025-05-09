# ndvi_service.py

import os, json, hashlib, logging, asyncio, aiohttp, datetime
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from .sentinel_service import SentinelService
from .geo_service import GeoService
from ..models import NDVIRegion
from FarmAcc.models import FarmInfo

class NDVIService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.sentinel = SentinelService()
        self.geo = GeoService()
        self.model_paths = {
            'cache_dir': os.path.join(settings.BASE_DIR, "Map/cache"),
            'cache_index': os.path.join(settings.BASE_DIR, "Map/cache_index.json")
        }
        self.evalscript = """//VERSION=3
function setup() {
  return { input: ["B04", "B08"], output: { bands: 4, sampleType: "UINT8" }};
}
function evaluatePixel(sample) {
  let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
  let r=0,g=0,b=0,a=255;
  if (ndvi < -0.2) r=g=b=0;
  else if (ndvi < 0) { r=165; g=42; b=42; }
  else if (ndvi < 0.2) { r=255; g=255; b=0; }
  else if (ndvi < 0.4) { r=0; g=255; b=0; }
  else { r=0; g=128; b=0; }
  if (sample.B08 === 0 && sample.B04 === 0) a = 0;
  return [r, g, b, a];
}"""

    async def get_ndvi_image(self, geometry, start_date, end_date, use_cache=True):
        cache_key = hashlib.md5(f"{geometry}_{start_date}_{end_date}".encode()).hexdigest()
        cache_path = os.path.join(self.model_paths['cache_dir'], f"{cache_key}.png")

        if use_cache:
            os.makedirs(self.model_paths['cache_dir'], exist_ok=True)
            if os.path.exists(self.model_paths['cache_index']):
                with open(self.model_paths['cache_index'], "r") as f:
                    cache_index = json.load(f)
                for key, entry in cache_index.items():
                    if self.geo.are_geometries_similar(geometry, entry['geometry'], threshold=0.8):
                        self.logger.info("NDVI cache hit (geometry match).")
                        if os.path.exists(entry['cache_path']):
                            with open(entry['cache_path'], 'rb') as f:
                                return f.read()

        payload = {
            "input": {
                "bounds": {"geometry": geometry},
                "data": [{
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "timeRange": {
                            "from": f"{start_date}T00:00:00Z",
                            "to": f"{end_date}T23:59:59Z"
                        }
                    }
                }]
            },
            "output": {
                "width": 512,
                "height": 512,
                "responses": [{
                    "identifier": "default",
                    "format": {"type": "image/png"}
                }]
            },
            "evalscript": self.evalscript
        }

        headers = {
            "Authorization": f"Bearer {self.sentinel.get_token()}",
            "Content-Type": "application/json"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://services.sentinel-hub.com/api/v1/process", headers=headers, json=payload, timeout=30) as resp:
                    if resp.status == 200:
                        image_data = await resp.read()
                        if use_cache:
                            with open(cache_path, 'wb') as f:
                                f.write(image_data)
                            index = {}
                            if os.path.exists(self.model_paths['cache_index']):
                                with open(self.model_paths['cache_index'], 'r') as f:
                                    index = json.load(f)
                            index[cache_key] = {"geometry": geometry, "cache_path": cache_path}
                            with open(self.model_paths['cache_index'], 'w') as f:
                                json.dump(index, f)
                            self.logger.info("NDVI image cached.")
                        return image_data
                    else:
                        self.logger.warning(f"Sentinel error {resp.status}: {await resp.text()}")
        except asyncio.TimeoutError:
            self.logger.error("NDVI request timed out.")
        except Exception as e:
            self.logger.error(f"NDVI fetch error: {e}")
        return None

    async def fetch_and_save_ndvi(self, farm_id, geometry, start_date, end_date):
        image_binary = await self.get_ndvi_image(geometry, start_date, end_date, use_cache=True)
        if not image_binary:
            return None
        geo_obj = GEOSGeometry(json.dumps(geometry), srid=4326)
        farm = FarmInfo.objects.get(id=farm_id)
        region = NDVIRegion(farm=farm, geometry=geo_obj)
        filename = f"ndvi_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        region.image.save(filename, ContentFile(image_binary))
        region.save()
        return region.id
