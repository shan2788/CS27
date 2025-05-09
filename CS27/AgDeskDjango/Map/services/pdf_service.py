from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
import numpy as np
from shapely.geometry import Polygon
import geopandas as gpd

class PDFService:
    def __init__(self):
        pass
    
    @staticmethod
    def draw_wrapped_text(p, text, x, y, max_width, line_height=15):
        """
        Draw text with automatic line wrapping.
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
    def generate_pdf_report(start_date, end_date, predicted_crop, predicted_biomass, formatted_data):
        """
        Generate a PDF report for NDVI data.
        """
        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        # Title and metadata
        p.drawString(100, 800, "NDVI Report")
        p.drawString(100, 780, f"Start Date: {start_date}")
        p.drawString(100, 760, f"End Date: {end_date}")

        # Add predicted crop and biomass with wrapping
        y_position = 740
        y_position = PDFService.draw_wrapped_text(p, f"Predicted Crop: {predicted_crop}", 100, y_position, max_width=400)
        y_position = PDFService.draw_wrapped_text(p, f"Predicted Biomass: {predicted_biomass}", 100, y_position - 20, max_width=400)

        # Add NDVI mean and bands mean
        y_position -= 20
        for entry in formatted_data:
            y_position = PDFService.draw_wrapped_text(p, f"Time Interval: {entry['from']} → {entry['to']}", 100, y_position, max_width=400)
            y_position -= 20
            y_position = PDFService.draw_wrapped_text(p, f"NDVI Mean: {entry['ndvi_mean']:.4f}", 100, y_position, max_width=400)
            y_position -= 20
            p.drawString(100, y_position, "Bands Mean (x10000):")
            y_position -= 20

            for band, mean in entry["bands_mean"].items():
                y_position = PDFService.draw_wrapped_text(p, f"{band}: {mean:.2f}", 120, y_position, max_width=400)
                y_position -= 20

            y_position -= 10
            if y_position < 100:
                p.showPage()
                y_position = 800

        # Save the PDF
        p.showPage()
        p.save()

        # Return PDF as response
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_credit_report(start_date, end_date, estimated_area_square, geometry_data, predicted_CO2, formatted_data):
        """
        Generate a PDF report for carbon credit data.
        """
        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        # Title and metadata
        p.drawString(100, 800, "Carbon Credit Report")
        p.drawString(100, 780, f"Start Date: {start_date}")
        p.drawString(100, 760, f"End Date: {end_date}")

        # Add predicted CO2 and area information
        y_position = 740
        y_position = PDFService.draw_wrapped_text(p, f"Farm Geometry: {geometry_data['coordinates'][0]}", 100, y_position, max_width=400)
        average_CO2 = np.array(predicted_CO2)
        y_position = PDFService.draw_wrapped_text(p, f"Predicted average carbon stock for the selected time period (kg): {PDFService.calculate_positive_average(average_CO2)}", 100, y_position - 20, max_width=400)
        y_position = PDFService.draw_wrapped_text(p, f"Estimate area square (km2): {estimated_area_square}", 100, y_position - 20, max_width=400)
        y_position = PDFService.draw_wrapped_text(p, f"Estimate area square (ha): {estimated_area_square * 100}", 100, y_position - 20, max_width=400)

        if estimated_area_square * 100 < 0.2:
            y_position = PDFService.draw_wrapped_text(p, f"The selected area is too small to earn Australian carbon credit units.", 100, y_position - 20, max_width=400)
        else:
            y_position = PDFService.draw_wrapped_text(p, f"If the farm is cleared of forest for 5 years and located in FullCAM area, the {estimated_area_square:.2f} km² is eligible to earn Australian carbon credit units.", 100, y_position - 20, max_width=400)

        # Save the PDF
        p.showPage()
        p.save()

        # Return PDF as response
        buffer.seek(0)
        return buffer

    @staticmethod
    def calculate_positive_average(array):
        """
        Calculate the average of positive values in a numpy array.
        """
        positive_values = array[array > 0]
        if positive_values.size > 0:
            return np.mean(positive_values)
        else:
            return None