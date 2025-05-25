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
from ..test_pre import make_tree_recommendation, make_density_prediction, fake_carbon_series


class TreeRecommendationService:
    _instance = None


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TreeRecommendationService, cls).__new__(cls)
        return cls._instance

    def generate(self, geometry, start_date, end_date, farm_id):
        # Step 1: 获取统计数据
        formatted_data = StatisticsService.get_statistics_for_model_input(geometry, start_date, end_date)
        if not formatted_data:
            raise ValueError("No NDVI stats available")

        # Step 2: 树种与碳预测
        species = make_tree_recommendation(formatted_data)
        density = make_density_prediction(formatted_data)
        carbon_list = fake_carbon_series(density)
        years = [str(2025 + i) for i in range(len(carbon_list))]

        # Step 3: 生成图像
        chart_base64 = self._plot_carbon_chart(years, carbon_list)
        # print("DEBUG >>> farm_id:", repr(farm_id))

        # Step 4: 渲染模板
        html = render_to_string("./Map/tree_result.html", {
            "species": species,
            "density": density,
            "carbon": chart_base64,
            "farm_id": farm_id,  # ✅ 原有变量
            "currentFarmID": farm_id,  # ✅ 加入这个变量以供 base.html 使用
        })

        return html

    def _plot_carbon_chart(self, years, carbon_values):
        plt.figure()
        plt.plot(years, carbon_values, marker='o')
        plt.title("Predicted Carbon Change")
        plt.xlabel("Year")
        plt.ylabel("Carbon Emission (ton/year)")
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        buffer.close()
        return f"data:image/png;base64,{img_base64}"

