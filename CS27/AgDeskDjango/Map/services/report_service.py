# services/report_generator.py

import os
import datetime
import json
from django.contrib.gis.geos import GEOSGeometry

from .statistics_service import StatisticsService
from .prediction_service import CropModelService, BiomassModelService
from .pdf_service import PDFService
from .geo_service import GeoService
from Map.models import NDVIReport
from FarmAcc.models import FarmInfo

from Map.models import CarbonCredit


class ReportGenerator:
    _instance = None

    def __new__(cls, model_paths=None, report_path=None, logger=None):
        if cls._instance is None:
            cls._instance = super(ReportGenerator, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_paths=None, report_path=None, logger=None):
        if self._initialized:
            return
        self.model_paths = model_paths
        self.report_path = report_path
        self.logger = logger
        self._initialized = True

    def generate(self, geometry_data, start_date, end_date, user):
        try:
            geo_obj = GEOSGeometry(json.dumps(geometry_data), srid=4326)

            # Step 1: 统计数据与模型输入
            formatted_data = StatisticsService.get_statistics_for_model_input(geometry_data, start_date, end_date)

            # Step 2: 作物预测
            crop_model = CropModelService(self.logger, model_path=self.model_paths['crop_model'], encoder_path=self.model_paths['crop_encoder'])
            predicted_crop = crop_model.make_prediction(formatted_data)

            # Step 3: 生物量预测
            biomass_model = BiomassModelService(
                self.logger,
                self.model_paths['biomass_model'],
                self.model_paths['scaler_X'],
                self.model_paths['scaler_y']
            )
            predicted_biomass = biomass_model.make_prediction(formatted_data)

            # Step 4: 报告生成与保存
            buffer = PDFService.generate_pdf_report(start_date, end_date, predicted_crop, predicted_biomass, formatted_data)
            filename = f"NDVI_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            os.makedirs(self.report_path, exist_ok=True)
            file_path = os.path.join(self.report_path, filename)
            with open(file_path, 'wb') as f:
                f.write(buffer.getvalue())

            # Step 5: 写入数据库
            farm = self._get_farm(user)
            NDVIReport.objects.create(
                farm=farm,
                start_date=start_date,
                end_date=end_date,
                file_path=f'report/{filename}',
                geolocation=geo_obj
            )

            buffer.seek(0)
            return buffer, filename

        except Exception as e:
            self.logger.error(f"Report generation failed: {e}")
            raise e  # 交给上层处理

    def _get_farm(self, user):
        farm_id = getattr(user, "currentFarm_id", None)
        return FarmInfo.objects.get(id=farm_id) if farm_id else None

    def generate_carbon_report(self, geometry_data, start_date, end_date, user):
        geo_obj = GEOSGeometry(json.dumps(geometry_data), srid=4326)

        formatted_data = StatisticsService.get_statistics_for_model_input(
            geometry_data, start_date, end_date
        )

        biomass_model = BiomassModelService(
            self.logger,
            self.model_paths['biomass_model'],
            self.model_paths['scaler_X'],
            self.model_paths['scaler_y']
        )
        predicted_biomass = biomass_model.make_prediction(formatted_data)
        predicted_CO2 = biomass_model.convert_tree_biomass_array_to_CO2(predicted_biomass)

        estimated_area_square = GeoService.calculate_area_square(geometry_data['coordinates'][0])

        buffer = PDFService.generate_credit_report(
            start_date, end_date, estimated_area_square,
            geometry_data, predicted_CO2, formatted_data
        )

        filename = f"Carbon_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        os.makedirs(self.report_path, exist_ok=True)
        file_path = os.path.join(self.report_path, filename)
        with open(file_path, 'wb') as f:
            f.write(buffer.getvalue())

        # 数据库写入
        farm_id = getattr(user, "currentFarm_id", None)
        farm = FarmInfo.objects.get(id=farm_id) if farm_id else None
        CarbonCredit.objects.create(
            farm=farm,
            start_date=start_date,
            end_date=end_date,
            file_path=f'report/{filename}',
            geolocation=geo_obj
        )

        buffer.seek(0)
        return buffer
