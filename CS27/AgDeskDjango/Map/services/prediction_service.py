# services/prediction_service.py
import joblib
import numpy as np
import torch

class ModelService:
    def __init__(self, logger=None, model_path=None, scaler_X_path=None, scaler_y_path=None, encoder_path=None):
        self.logger = logger
        self.model = torch.load(model_path, weights_only=False) if model_path else None
        self.scaler_X = joblib.load(scaler_X_path) if scaler_X_path else None
        self.scaler_y = joblib.load(scaler_y_path) if scaler_y_path else None
        self.encoder = joblib.load(encoder_path) if encoder_path else None
    
    def make_prediction(self, formatted_data):
        return

class CropModelService(ModelService):
    def __init__(self, logger=None, model_path=None, scaler_X_path=None, scaler_y_path=None, encoder_path=None):
        self.logger = logger
        self.model = joblib.load(model_path) if model_path else None
        self.scaler_X = joblib.load(scaler_X_path) if scaler_X_path else None
        self.scaler_y = joblib.load(scaler_y_path) if scaler_y_path else None
        self.encoder = joblib.load(encoder_path) if encoder_path else None

    # 重写父类方法
    def make_prediction(self, formatted_data):
        try:
            # Extract the band values from the formatted data
            print(0)
            band_values = []
            for entry in formatted_data:
                bands_mean = entry["bands_mean"]
                # Ensure the order of bands matches the expected input format
                band_values.append([
                    bands_mean.get(f"B{str(i).zfill(2)}", 0) 
                    for i in [1,2,3,4,5,6,7,8,'8A',9,11,12]
                ])

            # Convert to a NumPy array for model input
            band_values = np.array(band_values)
            # Make predictions using the model
            predictions = self.model.predict(band_values)
            # Ensure predictions are a 1D array
            predictions = np.array(predictions).flatten()
            # Decode the predicted labels using the encoder
            decoded_results = self.encoder.inverse_transform(predictions)
            
            return decoded_results

        except Exception as e:
            self.logger.error(f"Error in making predictions in crop species: {e}")
            return "Error in prediction"
    

class BiomassModelService(ModelService):
    def __init__(self, logger=None, model_path=None, scaler_X_path=None, scaler_y_path=None, encoder_path=None):
        super().__init__(logger, model_path, scaler_X_path, scaler_y_path, encoder_path)
    

    def calculate_evi(self, bands_mean):
        try:
            G = 2.5
            C1 = 6.0
            C2 = 7.5
            L = 1.0

            nir = bands_mean.get("B08", 0)  # Near-infrared band
            red = bands_mean.get("B04", 0)  # Red band
            blue = bands_mean.get("B02", 0)  # Blue band

            # Avoid division by zero
            denominator = (nir + C1 * red - C2 * blue + L)
            if denominator == 0:
                return 0

            evi = G * (nir - red) / denominator
            return evi

        except Exception as e:
            self.logger.error(f"Error calculating EVI: {e}")
            return 0
        
    def make_prediction(self, formatted_data):
        self.model.eval()  # Set the model to evaluation mode
        try:
            # Extract the band values and indices (NDVI, EVI) from the formatted data
            band_values = []
            for entry in formatted_data:
                bands_mean = entry["bands_mean"]
                ndvi_mean = entry.get("ndvi_mean", 0)  # NDVI mean value
                evi_mean = self.calculate_evi(bands_mean, self.logger)  # Calculate EVI

                # Ensure the order of inputs matches the expected input format
                band_values.append([
                    ndvi_mean,
                    evi_mean,
                    *[bands_mean.get(f"B{str(i).zfill(2)}", 0) for i in range(1, 9)],
                    bands_mean.get("B8A", 0),
                    bands_mean.get("B11", 0), 
                    bands_mean.get("B12", 0)
                ])

            # Convert to a NumPy array for model input
            band_values = np.array(band_values)
            band_scaled = self.scaler_X.transform(band_values)
            band_values_tensor = torch.tensor(band_scaled, dtype=torch.float32)

            # Make predictions using the model
            with torch.no_grad():
                predictions = self.model(band_values_tensor)
                predictions_log = self.scaler_y.inverse_transform(predictions.numpy())
                predictions_mu = np.expm1(predictions_log)

            return predictions_mu

        except Exception as e:
            self.logger.error(f"Error in make_biomass_prediction: {e}")
            
            return "Error in prediction"

def convert_tree_biomass_array_to_CO2(tree_biomass_array, carbon_content_percentage=50):
    """
    Convert an array of tree biomass values to equivalent CO2 emissions.
    :param tree_biomass_array: Array of tree biomass values (in kilograms)
    :param carbon_content_percentage: Percentage of biomass that is carbon (default: 50% for trees)
    :return: Array of CO2 emissions (in kilograms)
    """
    # Constants
    molar_mass_C = 12.01  # g/mol (Carbon)
    molar_mass_CO2 = 44.01  # g/mol (Carbon Dioxide)

    # Convert tree biomass array to grams
    tree_biomass_array_grams = np.array(tree_biomass_array) * 1000  # kilograms to grams

    # Calculate carbon mass in the tree biomass array
    carbon_mass_array = tree_biomass_array_grams * (carbon_content_percentage / 100)

    # Convert carbon mass to CO2 mass (in grams)
    CO2_mass_array_grams = carbon_mass_array * (molar_mass_CO2 / molar_mass_C)

    # Convert CO2 mass back to kilograms
    CO2_mass_array_kg = CO2_mass_array_grams / 1000  # grams to kilograms
    
    return CO2_mass_array_kg
