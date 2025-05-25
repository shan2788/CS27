from io import BytesIO
import numpy as np
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
import numpy as np
import re
import ast
import pandas as pd
from tempfile import NamedTemporaryFile
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon

class PDFService:
    """
        A service class to generate PDF reports for NDVI and carbon credit data using ReportLab.
        Includes support for drawing wrapped text, generating tables, and formatting detailed content.
    """
    def __init__(self):
        pass

    @staticmethod
    def render_crop_predictions(predicted_crop, story, styles):
        """
        Parse and render multiple crop prediction intervals from a text string.
        Each prediction is visualized as a horizontal bar chart using Seaborn.
        """
        story.append(Paragraph("<b>Predicted Crop:</b>", styles["SectionTitle"]))

        if isinstance(predicted_crop, str):
            matches = re.findall(r"\[\(.*?\)\]", predicted_crop)

            if matches:
                for idx, match in enumerate(matches):
                    try:
                        prediction_list = ast.literal_eval(match)
                        labels, percents = zip(*prediction_list)
                        values = [float(p.strip('%')) for p in percents]

                        df = pd.DataFrame({'Class': labels, 'Probability': values})
                        df = df.sort_values(by='Probability', ascending=False)

                        # Seaborn 横向条形图
                        plt.figure(figsize=(5, 2.5))
                        ax = sns.barplot(x='Probability', y='Class', data=df, palette='Set2')
                        plt.title(f"Interval {idx+1} - Top Crop Predictions")
                        plt.xlim(0, 100)
                        plt.xlabel("Probability (%)")
                        plt.tight_layout()

                        # 保存为临时图像
                        with NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
                            plt.savefig(tmpfile.name, dpi=150)
                            plt.close()
                            story.append(Image(tmpfile.name, width=14*cm, height=5*cm))
                            story.append(Spacer(1, 12))

                    except Exception as e:
                        story.append(Paragraph(f"⚠️ Failed to parse interval {idx+1}: {str(e)}", styles["NormalText"]))
            else:
                story.append(Paragraph("⚠️ No prediction pattern found.", styles["NormalText"]))
        else:
            story.append(Paragraph(str(predicted_crop), styles["NormalText"]))
            story.append(Spacer(1, 12))

    @staticmethod
    def render_biomass_trend(predicted_biomass, story, styles):
        """
        Plot predicted biomass values as a line chart across intervals.
        """
        story.append(Paragraph("<b>Predicted Biomass:</b>", styles["SectionTitle"]))

        try:
            # 展平为 list
            if isinstance(predicted_biomass, np.ndarray):
                values = np.ravel(predicted_biomass).tolist()
            elif isinstance(predicted_biomass, list):
                values = predicted_biomass
            else:
                raise ValueError("Unsupported format for predicted_biomass")

            # 构建 DataFrame
            df = pd.DataFrame({
                "Interval": [f"#{i+1}" for i in range(len(values))],
                "Biomass (kg)": values
            })

            # 绘图
            plt.figure(figsize=(5.5, 2.8))
            sns.lineplot(x="Interval", y="Biomass (kg)", data=df, marker="o", color="seagreen")
            plt.title("Predicted Biomass Trend")
            plt.tight_layout()

            with NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
                plt.savefig(tmpfile.name, dpi=150)
                plt.close()
                story.append(Image(tmpfile.name, width=15*cm, height=5.5*cm))
                story.append(Spacer(1, 12))

        except Exception as e:
            story.append(Paragraph("⚠️ Failed to visualize biomass data.", styles["NormalText"]))
            story.append(Paragraph(str(e), styles["NormalText"]))

    @staticmethod
    def render_interval_table(formatted_data, story, styles):

        story.append(Paragraph("<b>NDVI Interval Time Periods</b>", styles["SectionTitle"]))

        table_data = [["Interval", "Time Range"]]
        for idx, entry in enumerate(formatted_data):
            table_data.append([f"Interval {idx+1}", f"{entry['from']} → {entry['to']}"])

        table = Table(table_data, colWidths=[5*cm, 10*cm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(table)
        story.append(Spacer(1, 12))

    
    @staticmethod
    def render_ndvi_trend(formatted_data, story, styles):
        """
        Plot NDVI mean values over intervals as a line chart.
        Also display interval→time mapping before the chart.
        """
        
        # title for the NDVI trend section
        story.append(Paragraph("<b>NDVI Trend Over Time</b>", styles["SectionTitle"]))

        try:
            # prepare data for plotting
            interval_ids = [f"Interval {i+1}" for i in range(len(formatted_data))]
            ndvi_values = [entry["ndvi_mean"] for entry in formatted_data]

            df = pd.DataFrame({
                "Interval": interval_ids,
                "NDVI Mean": ndvi_values
            })

            # draw the line plot
            plt.figure(figsize=(6, 3.5))
            sns.lineplot(x="Interval", y="NDVI Mean", data=df, marker="o", color="blue")

            # show the numbers on top of each point
            for i, value in enumerate(ndvi_values):
                plt.text(i, value, f"{value:.4f}", ha="center", va="bottom", fontsize=8)

            plt.ylim(min(ndvi_values) - 0.05, max(ndvi_values) + 0.05)
            plt.tight_layout()

            # save the plot to a temporary file
            with NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
                plt.savefig(tmpfile.name, dpi=100)
                plt.close()
                story.append(Image(tmpfile.name, width=16*cm, height=6*cm))
                story.append(Spacer(1, 12))

        except Exception as e:
            story.append(Paragraph("⚠️ Failed to generate NDVI trend plot.", styles["NormalText"]))
            story.append(Paragraph(str(e), styles["NormalText"]))



    @staticmethod
    def generate_pdf_report(start_date, end_date, predicted_crop, predicted_biomass, formatted_data, farm_details):
        """
        Generate a PDF report containing NDVI statistics, prediction results, and farm details.

        Args:
            start_date (str): Start date for the report.
            end_date (str): End date for the report.
            predicted_crop (str): Predicted crop type.
            predicted_biomass (float or np.ndarray): Predicted biomass value(s).
            formatted_data (list of dict): Interval-based NDVI and bands data.
            farm_details (dict): Information about the farm (name, location, ID).

        Returns:
            BytesIO: Binary stream of the generated PDF.
        """

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=2*cm, leftMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="SectionTitle", fontSize=14, leading=18, spaceAfter=10, alignment=TA_LEFT, fontName="Helvetica-Bold"))
        styles.add(ParagraphStyle(name="NormalText", fontSize=11, leading=15, spaceAfter=6))

        story = []

        # Title
        story.append(Paragraph("NDVI Report", styles["Title"]))
        story.append(Spacer(1, 12))

        # Farm Details Section
        story.append(Paragraph("<b>Farm Information</b>", styles["SectionTitle"]))
        story.append(Paragraph(f"<b>Farm Name:</b> {farm_details.get('farmName', 'N/A')}", styles["NormalText"]))
        story.append(Paragraph(f"<b>Farm Location:</b> {farm_details.get('farmLocation', 'N/A')}", styles["NormalText"]))
        story.append(Paragraph(f"<b>Farm ID:</b> {farm_details.get('farmId', 'N/A')}", styles["NormalText"]))
        story.append(Spacer(1, 12))

        # Metadata
        story.append(Paragraph("<b>Report Period</b>", styles["SectionTitle"]))
        story.append(Paragraph(f"<b>Start Date:</b> {start_date}", styles["NormalText"]))
        story.append(Paragraph(f"<b>End Date:</b> {end_date}", styles["NormalText"]))
        story.append(Spacer(1, 12))
        PDFService.render_interval_table(formatted_data, story, styles)

        # Predictions
        PDFService.render_crop_predictions(predicted_crop, story, styles)
        PDFService.render_biomass_trend(predicted_biomass, story, styles)

        # NDVI data per interval
        PDFService.render_ndvi_trend(formatted_data, story, styles)

        # Final page break and build
        story.append(PageBreak())
        doc.build(story)
        buffer.seek(0)
        return buffer

    @staticmethod
    def render_geometry_map(geometry_data, story, styles):
        """
        Render a polygon from geometry_data onto a map and insert into PDF.
        """
        story.append(Paragraph("<b>Farm Geometry Map</b>", styles["SectionTitle"]))

        try:
            # Step 1: Construct Polygon
            coords = geometry_data.get("coordinates", [[]])[0]
            polygon = Polygon(coords)
            gdf = gpd.GeoDataFrame(index=[0], geometry=[polygon], crs="EPSG:4326")

            # Step 2: Plot
            fig, ax = plt.subplots(figsize=(4, 4))
            gdf.boundary.plot(ax=ax, edgecolor="green", linewidth=2)
            gdf.plot(ax=ax, color="lightgreen", alpha=0.5)
            ax.set_title("Farm Boundary", fontsize=12)
            ax.axis("equal")
            ax.axis("off")
            plt.tight_layout()

            # Step 3: Save to temp file
            with NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
                plt.savefig(tmpfile.name, dpi=100)
                plt.close()
                story.append(Image(tmpfile.name, width=10*cm, height=10*cm))
                story.append(Spacer(1, 12))

        except Exception as e:
            story.append(Paragraph("⚠️ Failed to render geometry map.", styles["NormalText"]))
            story.append(Paragraph(str(e), styles["NormalText"]))

    @staticmethod
    def generate_credit_report(start_date, end_date, estimated_area_square, geometry_data, predicted_CO2, formatted_data, farm_details):
        """
        Generate a carbon credit eligibility PDF report based on predicted CO₂ data and farm geometry.

        Args:
            start_date (str): Start date for data range.
            end_date (str): End date for data range.
            estimated_area_square (float): Area of the region in km².
            geometry_data (dict): GeoJSON-style geometry information.
            predicted_CO2 (list or np.ndarray): Predicted carbon values.
            formatted_data (list of dict): Optional interval-based report content.
            farm_details (dict): Farm metadata.

        Returns:
            BytesIO: Binary stream of the generated PDF.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=2*cm, leftMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="SectionTitle", fontSize=14, leading=18, spaceAfter=10, alignment=TA_LEFT, fontName="Helvetica-Bold"))
        styles.add(ParagraphStyle(name="NormalText", fontSize=11, leading=15, spaceAfter=6))

        story = []

        # Title
        story.append(Paragraph("Carbon Credit Report", styles["Title"]))
        story.append(Spacer(1, 12))

        # Farm Details Section
        story.append(Paragraph("<b>Farm Information</b>", styles["SectionTitle"]))
        story.append(Paragraph(f"<b>Farm Name:</b> {farm_details.get('farmName', 'N/A')}", styles["NormalText"]))
        story.append(Paragraph(f"<b>Farm Location:</b> {farm_details.get('farmLocation', 'N/A')}", styles["NormalText"]))
        story.append(Paragraph(f"<b>Farm ID:</b> {farm_details.get('farmId', 'N/A')}", styles["NormalText"]))
        story.append(Spacer(1, 12))

        # Metadata
        story.append(Paragraph(f"<b>Start Date:</b> {start_date}", styles["NormalText"]))
        story.append(Paragraph(f"<b>End Date:</b> {end_date}", styles["NormalText"]))
        story.append(Spacer(1, 12))

        # Geometry info
        # PDFService.render_geometry_map(geometry_data, story, styles)

        # Carbon and area stats
        avg_co2 = PDFService.calculate_positive_average(np.array(predicted_CO2))
        story.append(Paragraph(f"<b>Predicted Avg Carbon Credit:</b> {avg_co2:.2f}", styles["NormalText"]))
        story.append(Paragraph(f"<b>Estimated Area:</b> {estimated_area_square:.2f} km² / {estimated_area_square*100:.2f} ha", styles["NormalText"]))
        story.append(Spacer(1, 12))

        # Eligibility statement
        if estimated_area_square * 100 < 0.2:
            story.append(Paragraph(
                "<b><font color='red'>✖ Not Eligible:</font></b> "
                "The selected area is too small to earn Australian carbon credit units (< 0.2 ha).",
                styles["NormalText"]
            ))
        else:
            story.append(Paragraph(
                f"<b><font color='green'>✔ Eligible:</font></b> "
                f"The {estimated_area_square:.2f} km² region qualifies for Australian carbon credit units, "
                "assuming deforestation occurred at least 5 years ago and the area falls within a FullCAM zone.",
                styles["NormalText"]
            ))

        doc.build(story)
        buffer.seek(0)
        return buffer

    @staticmethod
    def calculate_positive_average(array):
        """
        Calculate the mean of all positive values in a numpy array.

        Args:
            array (np.ndarray): Input array containing numerical values.

        Returns:
            float or None: Mean of positive values, or None if none exist.
        """
        positive_values = array[array > 0]
        if positive_values.size > 0:
            return np.mean(positive_values)
        else:
            return None