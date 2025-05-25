from io import BytesIO
from reportlab.pdfbase.pdfmetrics import stringWidth
import numpy as np
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
import numpy as np

class PDFService:
    """
        A service class to generate PDF reports for NDVI and carbon credit data using ReportLab.
        Includes support for drawing wrapped text, generating tables, and formatting detailed content.
    """
    def __init__(self):
        pass
    
    @staticmethod
    def draw_wrapped_text(p, text, x, y, max_width, line_height=15):
        """
        Draw text on a canvas with automatic word wrapping.

        Args:
            p (Canvas): ReportLab canvas object.
            text (str): Text to be drawn.
            x (float): X-coordinate of text start.
            y (float): Y-coordinate of first line.
            max_width (float): Maximum width before wrapping.
            line_height (int): Height between lines.

        Returns:
            float: Updated Y position after drawing.
        """
        words = text.split(' ')
        line = ''
        for word in words:
            if stringWidth(line + word, p._fontname, p._fontsize) <= max_width:
                line += word + ' '
            else:
                p.drawString(x, y, line.strip())
                y -= line_height
                line = word + ' '
        if line:
            p.drawString(x, y, line.strip())
        return y

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

        # Predictions
        story.append(Paragraph("<b>Predicted Crop:</b>", styles["SectionTitle"]))
        story.append(Paragraph(predicted_crop, styles["NormalText"]))
        story.append(Spacer(1, 6))

        story.append(Paragraph("<b>Predicted Biomass:</b>", styles["SectionTitle"]))
        if isinstance(predicted_biomass, np.ndarray):
            flat_values = np.ravel(predicted_biomass)
            biomass_str = ", ".join([f"{float(x):.2f}" for x in flat_values])
        else:
            biomass_str = str(predicted_biomass)

        story.append(Paragraph(f"Predicted Biomass (kg): {biomass_str}", styles["NormalText"]))


        story.append(Spacer(1, 12))

        # NDVI data per interval
        for idx, entry in enumerate(formatted_data):
            story.append(Paragraph(f"<b>Interval {idx+1}</b>", styles["SectionTitle"]))
            story.append(Paragraph(f"Time: {entry['from']} → {entry['to']}", styles["NormalText"]))
            story.append(Paragraph(f"NDVI Mean: {entry['ndvi_mean']:.4f}", styles["NormalText"]))

            story.append(Paragraph("Bands Mean (×10000):", styles["NormalText"]))

            table_data = [["Band", "Mean Value"]]
            for band, mean in entry["bands_mean"].items():
                table_data.append([band, f"{mean:.2f}"])

            table = Table(table_data, colWidths=[5*cm, 5*cm])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))
            story.append(table)
            story.append(Spacer(1, 18))

        # Final page break and build
        story.append(PageBreak())
        doc.build(story)
        buffer.seek(0)
        return buffer

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
        coords_text = str(geometry_data["coordinates"][0])[:500] + "..."
        story.append(Paragraph("<b>Farm Geometry Coordinates:</b>", styles["SectionTitle"]))
        story.append(Paragraph(coords_text, styles["NormalText"]))
        story.append(Spacer(1, 12))

        # Carbon and area stats
        avg_co2 = PDFService.calculate_positive_average(np.array(predicted_CO2))
        story.append(Paragraph(f"<b>Predicted Avg Carbon Credit:</b> {avg_co2:.2f}", styles["NormalText"]))
        story.append(Paragraph(f"<b>Estimated Area:</b> {estimated_area_square:.2f} km² / {estimated_area_square*100:.2f} ha", styles["NormalText"]))
        story.append(Spacer(1, 12))

        # Eligibility statement
        if estimated_area_square * 100 < 0.2:
            msg = "⚠️ The selected area is too small to earn Australian carbon credit units."
        else:
            msg = f"✅ The {estimated_area_square:.2f} km² region is eligible for Australian carbon credit units, if cleared of forest for 5 years and located in a FullCAM area."
        story.append(Paragraph(msg, styles["NormalText"]))
        story.append(Spacer(1, 18))

        # Optional: include formatted_data if needed
        if formatted_data:
            story.append(Paragraph("<b>Detailed Time Intervals:</b>", styles["SectionTitle"]))
            for idx, entry in enumerate(formatted_data):
                story.append(Paragraph(f"Time: {entry['from']} → {entry['to']}", styles["NormalText"]))
                story.append(Spacer(1, 6))

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