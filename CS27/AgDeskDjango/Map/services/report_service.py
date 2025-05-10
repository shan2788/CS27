# import os
# import json
# import logging
# import joblib
# import torch
# import datetime
# from django.contrib.gis.geos import GEOSGeometry
# from django.conf import settings
# from ..models import NDVIReport, CarbonCredit
# from FarmAcc.models import FarmInfo
# from .prediction_service import make_crop_prediction, make_biomass_prediction, convert_tree_biomass_array_to_CO2
# from ..utils import generate_pdf_report, generate_credit_report, calculate_area_square
# from django.core.files.base import ContentFile
# from io import BytesIO
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch
#
# from .statistics_service import StatisticsService
#
# logger = logging.getLogger(__name__)
#
# class ReportService:
#     """报告服务类，处理所有报告生成相关的操作"""
#
#     def __init__(self):
#         self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         self.report_path = os.path.join(settings.MEDIA_ROOT, "report")
#         self.statistics_service = StatisticsService()
#
#         # 加载模型和编码器
#         self.crop_model = joblib.load(os.path.join(self.base_dir, "rf_model.pkl"))
#         self.crop_encoder = joblib.load(os.path.join(self.base_dir, "label_encoder.pkl"))
#         self.biomass_model = torch.load(os.path.join(self.base_dir, "biomass_model.pkl"), weights_only=False)
#         self.scaler_X = joblib.load(os.path.join(self.base_dir, 'scaler_X.pkl'))
#         self.scaler_y = joblib.load(os.path.join(self.base_dir, 'scaler_y.pkl'))
#
#     def generate_ndvi_report(self, start_date, end_date, geometry, user):
#         """生成 NDVI 报告"""
#         try:
#             # 获取统计数据
#             formatted_data = self.statistics_service.get_statistics_data(geometry, start_date, end_date)
#
#             # 进行预测
#             predicted_crop = make_crop_prediction(self.crop_model, self.crop_encoder, formatted_data, logger)
#             predicted_biomass = make_biomass_prediction(self.biomass_model, self.scaler_X, self.scaler_y, formatted_data, logger)
#             predicted_CO2 = convert_tree_biomass_array_to_CO2(predicted_biomass)
#
#             # 生成 PDF
#             buffer = self._generate_pdf_report(start_date, end_date, predicted_crop, predicted_biomass, formatted_data)
#
#             # 保存报告
#             self._save_report(buffer, user, start_date, end_date, geometry, "NDVI")
#
#             return buffer
#
#         except Exception as e:
#             logger.error(f"Error generating NDVI report: {str(e)}")
#             raise
#
#     def generate_carbon_credit_report(self, start_date, end_date, geometry, user):
#         """生成碳信用报告"""
#         try:
#             # 获取统计数据
#             formatted_data = self.statistics_service.get_statistics_data(geometry, start_date, end_date)
#
#             # 进行预测
#             predicted_biomass = make_biomass_prediction(self.biomass_model, self.scaler_X, self.scaler_y, formatted_data, logger)
#             predicted_CO2 = convert_tree_biomass_array_to_CO2(predicted_biomass)
#             estimated_area = calculate_area_square(geometry['coordinates'][0])
#
#             # 生成 PDF
#             buffer = self._generate_credit_report(start_date, end_date, estimated_area, geometry, predicted_CO2, formatted_data)
#
#             # 保存报告
#             self._save_report(buffer, user, start_date, end_date, geometry, "Carbon")
#
#             return buffer
#
#         except Exception as e:
#             logger.error(f"Error generating carbon credit report: {str(e)}")
#             raise
#
#     def _generate_pdf_report(self, start_date, end_date, predicted_crop, predicted_biomass, formatted_data):
#         """生成 PDF 报告"""
#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer, pagesize=letter)
#         styles = getSampleStyleSheet()
#         story = []
#
#         # 添加标题
#         title_style = ParagraphStyle(
#             'CustomTitle',
#             parent=styles['Heading1'],
#             fontSize=24,
#             spaceAfter=30
#         )
#         story.append(Paragraph("NDVI 分析报告", title_style))
#
#         # 添加日期范围
#         story.append(Paragraph(f"分析时间范围: {start_date} 至 {end_date}", styles['Normal']))
#         story.append(Spacer(1, 12))
#
#         # 添加预测结果
#         story.append(Paragraph("预测结果", styles['Heading2']))
#         story.append(Paragraph(f"预测作物类型: {predicted_crop}", styles['Normal']))
#         story.append(Paragraph(f"预测生物量: {predicted_biomass:.2f} 吨/公顷", styles['Normal']))
#         story.append(Spacer(1, 12))
#
#         # 添加统计数据表格
#         data = [['时间', 'NDVI 平均值', '生物量']]
#         for entry in formatted_data:
#             data.append([
#                 entry['from'][:10],
#                 f"{entry['ndvi_mean']:.3f}" if entry['ndvi_mean'] else 'N/A',
#                 f"{predicted_biomass:.2f}"
#             ])
#
#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('FONTSIZE', (0, 0), (-1, 0), 14),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#             ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#             ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
#             ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
#             ('FONTSIZE', (0, 1), (-1, -1), 12),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('GRID', (0, 0), (-1, -1), 1, colors.black)
#         ]))
#         story.append(table)
#
#         doc.build(story)
#         return buffer
#
#     def _generate_credit_report(self, start_date, end_date, estimated_area, geometry, predicted_CO2, formatted_data):
#         """生成碳信用报告"""
#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer, pagesize=letter)
#         styles = getSampleStyleSheet()
#         story = []
#
#         # 添加标题
#         title_style = ParagraphStyle(
#             'CustomTitle',
#             parent=styles['Heading1'],
#             fontSize=24,
#             spaceAfter=30
#         )
#         story.append(Paragraph("碳信用报告", title_style))
#
#         # 添加基本信息
#         story.append(Paragraph(f"分析时间范围: {start_date} 至 {end_date}", styles['Normal']))
#         story.append(Paragraph(f"分析区域面积: {estimated_area:.2f} 公顷", styles['Normal']))
#         story.append(Spacer(1, 12))
#
#         # 添加碳信用预测
#         story.append(Paragraph("碳信用预测", styles['Heading2']))
#         story.append(Paragraph(f"预测碳吸收量: {predicted_CO2:.2f} 吨/年", styles['Normal']))
#         story.append(Spacer(1, 12))
#
#         # 添加统计数据表格
#         data = [['时间', 'NDVI 平均值', '碳吸收量']]
#         for entry in formatted_data:
#             data.append([
#                 entry['from'][:10],
#                 f"{entry['ndvi_mean']:.3f}" if entry['ndvi_mean'] else 'N/A',
#                 f"{predicted_CO2:.2f}"
#             ])
#
#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('FONTSIZE', (0, 0), (-1, 0), 14),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#             ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#             ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
#             ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
#             ('FONTSIZE', (0, 1), (-1, -1), 12),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('GRID', (0, 0), (-1, -1), 1, colors.black)
#         ]))
#         story.append(table)
#
#         doc.build(story)
#         return buffer
#
#     def _save_report(self, buffer, user, start_date, end_date, geometry, report_type):
#         """保存报告到文件系统"""
#         try:
#             os.makedirs(self.report_path, exist_ok=True)
#
#             # 生成文件名
#             timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
#             filename = f"{report_type}_Report_{timestamp}.pdf"
#             file_path = os.path.join(self.report_path, filename)
#
#             # 保存文件
#             with open(file_path, 'wb') as f:
#                 f.write(buffer.getvalue())
#
#             # 获取用户农场
#             farm_id = getattr(user, "currentFarm_id", None)
#             farm = FarmInfo.objects.get(id=farm_id) if farm_id else None
#
#             # 保存到数据库
#             geo_obj = GEOSGeometry(json.dumps(geometry), srid=4326)
#             if report_type == "NDVI":
#                 NDVIReport.objects.create(
#                     farm=farm,
#                     start_date=start_date,
#                     end_date=end_date,
#                     file_path=f'report/{filename}',
#                     geolocation=geo_obj
#                 )
#             else:
#                 CarbonCredit.objects.create(
#                     farm=farm,
#                     start_date=start_date,
#                     end_date=end_date,
#                     file_path=f'report/{filename}',
#                     geolocation=geo_obj
#                 )
#
#         except Exception as e:
#             logger.error(f"Error saving report: {str(e)}")
#             raise