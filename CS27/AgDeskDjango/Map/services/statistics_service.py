import logging
import requests
from .sentinel_service import SentinelService

SENTINEL_SERVICE = SentinelService()

logger = logging.getLogger(__name__)

class StatisticsService:
    def __init__(self):
        pass

    @staticmethod
    def get_statistics_data(geometry, start_date, end_date):
        evalscript = """//VERSION=3
        function setup() {
          return {
            input: ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B11", "B12", "dataMask"],
            output: [
              { id: "B01", bands: 1, sampleType: "FLOAT32" },
              { id: "B02", bands: 1, sampleType: "FLOAT32" },
              { id: "B03", bands: 1, sampleType: "FLOAT32" },
              { id: "B04", bands: 1, sampleType: "FLOAT32" },
              { id: "B05", bands: 1, sampleType: "FLOAT32" },
              { id: "B06", bands: 1, sampleType: "FLOAT32" },
              { id: "B07", bands: 1, sampleType: "FLOAT32" },
              { id: "B08", bands: 1, sampleType: "FLOAT32" },
              { id: "B8A", bands: 1, sampleType: "FLOAT32" },
              { id: "B09", bands: 1, sampleType: "FLOAT32" },
              { id: "B11", bands: 1, sampleType: "FLOAT32" },
              { id: "B12", bands: 1, sampleType: "FLOAT32" },
              { id: "dataMask", bands: 1 }
            ]
          };
        }
        function evaluatePixel(sample) {
          if (sample.dataMask === 0) {
            return {
              B01: [NaN], B02: [NaN], B03: [NaN], B04: [NaN], B05: [NaN], B06: [NaN], B07: [NaN],
              B08: [NaN], B8A: [NaN], B09: [NaN], B11: [NaN], B12: [NaN], dataMask: [0]
            };
          }
          return {
            B01: [sample.B01], B02: [sample.B02], B03: [sample.B03], B04: [sample.B04],
            B05: [sample.B05], B06: [sample.B06], B07: [sample.B07], B08: [sample.B08],
            B8A: [sample.B8A], B09: [sample.B09], B11: [sample.B11], B12: [sample.B12],
            dataMask: [1]
          };
        }"""

        band_ids = ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B11", "B12"]
        stats = {band: {"statistics": ["min", "max", "mean"]} for band in band_ids}

        payload = {
            "input": {
                "bounds": {"geometry": geometry},
                "data": [{"type": "sentinel-2-l2a"}]
            },
            "aggregation": {
                "timeRange": {
                    "from": f"{start_date}T00:00:00Z",
                    "to": f"{end_date}T23:59:59Z"
                },
                "aggregationInterval": {"of": "P7D"},
                "width": 512,
                "height": 512,
                "evalscript": evalscript
            },
            "calculations": {"default": {"statistics": stats}}
        }

        headers = {
            "Authorization": f"Bearer {SENTINEL_SERVICE.get_token()}",
            "Content-Type": "application/json"
        }

        response = requests.post("https://services.sentinel-hub.com/api/v1/statistics", headers=headers, json=payload)
        if response.status_code == 200:
            return response.json().get("data", [])
        raise Exception(f"Statistics error {response.status_code}: {response.text}")

    @staticmethod
    def get_statistics_for_model_input(geometry, start_date, end_date):
        try:
            raw_stats = StatisticsService.get_statistics_data(geometry, start_date, end_date)
            results = []
            for entry in raw_stats:
                interval = entry.get("interval", {})
                outputs = entry.get("outputs", {})

                bands_mean = {}
                for band_name, band_data in outputs.items():
                    band_stats = band_data.get("bands", {}).get("B0", {}).get("stats", {})
                    mean_val = band_stats.get("mean")
                    bands_mean[band_name] = mean_val * 10000 if mean_val is not None else None

                b08 = bands_mean.get("B08")
                b04 = bands_mean.get("B04")
                ndvi = (b08 - b04) / (b08 + b04) if b08 is not None and b04 is not None and (b08 + b04) != 0 else None

                results.append({
                    "from": interval.get("from"),
                    "to": interval.get("to"),
                    "bands_mean": bands_mean,
                    "ndvi_mean": ndvi
                })

            return results

        except Exception as e:
            logger.error(f"Error processing statistics for model input: {e}")
            return []
