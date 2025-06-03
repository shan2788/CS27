# services/tree_recommendation_service.py
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import base64
import matplotlib

matplotlib.use("Agg")  # ✅ 避免后端 GUI 卡死（必须有！）

import matplotlib.pyplot as plt

from io import BytesIO
from django.template.loader import render_to_string
from .statistics_service import StatisticsService
from datetime import datetime, timedelta
from .prediction_service import CropModelService, BiomassModelService
import pandas as pd
import seaborn as sns
import re
import ast
from collections import Counter
import numpy as np


class TreeRecommendationService:
    _instance = None

    def __new__(cls, model_paths=None, logger=None):
        if cls._instance is None:
            cls._instance = super(TreeRecommendationService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_paths=None, logger=None):
        """
        Initialize the TreeRecommendationService with model paths, report storage path, and optional logger.
        Args:
            model_paths (dict): Dictionary containing paths to required ML models and scalers.
            logger (Logger, optional): Logger instance for error logging.
        """
        if self._initialized:
            return
        self.model_paths = model_paths
        self.logger = logger
        self._initialized = True

    @staticmethod
    def get_most_frequent_top1(predicted_crop_text):
        # 提取所有的预测列表字符串
        matches = re.findall(r"\[\(.*?\)\]", predicted_crop_text)

        top1_list = []
        for match in matches:
            try:
                pred_list = ast.literal_eval(match)
                if pred_list:
                    top1_class = pred_list[0][0]
                    top1_list.append(top1_class)
            except:
                continue

        # 统计出现次数最多的 top1 类别
        count = Counter(top1_list)
        most_common = count.most_common(1)

        return most_common[0] if most_common else ("N/A", 0)

    def generate(self, geometry, start_date, end_date, farm_id):

        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

        start_date_prev = (start_date_obj - timedelta(days=365)).strftime("%Y-%m-%d")
        end_date_prev = (end_date_obj - timedelta(days=365)).strftime("%Y-%m-%d")

        # get statistics for model input
        formatted_data = StatisticsService.get_statistics_for_model_input(geometry, start_date_prev, end_date_prev)
        if not formatted_data:
            raise ValueError("No NDVI stats available")

        # Crop prediction
        crop_model = CropModelService(self.logger, model_path=self.model_paths['crop_model'],
                                      encoder_path=self.model_paths['crop_encoder'])
        predicted_crop = crop_model.make_prediction(formatted_data)
        recommend_crop = TreeRecommendationService.get_most_frequent_top1(predicted_crop)[0]

        # Biomass prediction
        biomass_model = BiomassModelService(
            self.logger,
            self.model_paths['biomass_model'],
            self.model_paths['scaler_X'],
            self.model_paths['scaler_y']
        )
        predicted_biomass = biomass_model.make_prediction(formatted_data)

        # calculate average of predicted biomass
        biomass_values = np.array(predicted_biomass).flatten()
        density = np.mean(biomass_values)
        predicted_carbon = biomass_model.convert_tree_biomass_array_to_CO2(predicted_biomass)
        carbon_values = np.array(predicted_carbon).flatten()

        # generate carbon chart
        chart_base64 = self._plot_carbon_chart(carbon_values)

        # render HTML template
        html = render_to_string("./Map/tree_result.html", {
            "species": recommend_crop,
            "density": density,
            "carbon": chart_base64,
            "farm_id": farm_id,
            "currentFarmID": farm_id,  
        })

        return html

    def _plot_carbon_chart(self, carbon_values):
        df = pd.DataFrame({
            "Interval": [f"Week{i + 1}" for i in range(len(carbon_values))],
            "Carbon (tons)": carbon_values
        })

        # 绘图
        plt.figure()
        sns.lineplot(x="Interval", y="Carbon (tons)", data=df, marker="o", color="seagreen")
        plt.title("Predicted Carbon Trend")
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        buffer.close()
        return f"data:image/png;base64,{img_base64}"

