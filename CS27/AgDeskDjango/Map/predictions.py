import numpy as np
import torch
import os
import joblib

def make_crop_prediction(model, encoder, formatted_data, logger):
    """
    Use the given model and encoder to predict the class of the plant.

    Args:
        model: The trained machine learning model (e.g., Random Forest).
        encoder: The label encoder used to encode class labels.
        formatted_data: A list of dictionaries, where each dictionary contains:
            - "from": Start of the time interval
            - "to": End of the time interval
            - "bands_mean": A dictionary of mean values for all bands
            - "ndvi_mean": The calculated NDVI mean value for the interval

    Returns:
        A string representing the predicted class of the plant.
    """

    try:
        # Extract the band values from the formatted data
        band_values = []
        for entry in formatted_data:
            bands_mean = entry["bands_mean"]
            # Ensure the order of bands matches the expected input format
            band_values.append([
                bands_mean.get("B01", 0),
                bands_mean.get("B02", 0),
                bands_mean.get("B03", 0),
                bands_mean.get("B04", 0),
                bands_mean.get("B05", 0),
                bands_mean.get("B06", 0),
                bands_mean.get("B07", 0),
                bands_mean.get("B08", 0),
                bands_mean.get("B8A", 0),
                bands_mean.get("B09", 0),
                bands_mean.get("B11", 0),
                bands_mean.get("B12", 0)
            ])

        # Convert to a NumPy array for model input
        band_values = np.array(band_values)

        # Make predictions using the model
        predictions = model.predict(band_values)

        # Ensure predictions are a 1D array
        predictions = np.array(predictions).flatten()

        # Decode the predicted labels using the encoder
        decoded_results = encoder.inverse_transform(predictions)

        return decoded_results

    except Exception as e:
        logger.error(f"Error in make_crop_prediction: {e}")
        return "Error in prediction"
    

def calculate_evi(bands_mean, logger):
    """
    Calculate the Enhanced Vegetation Index (EVI) from band means.

    Args:
        bands_mean: A dictionary containing mean values for all bands.

    Returns:
        The calculated EVI value.
    """
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
        logger.error(f"Error calculating EVI: {e}")
        return 0


def make_biomass_prediction(model, scaler_X, scaler_y, formatted_data, logger):
    """
    Predict biomass using the given model and formatted data.

    Args:
        model: The trained machine learning model for biomass prediction.
        formatted_data: A list of dictionaries, where each dictionary contains:
            - "from": Start of the time interval
            - "to": End of the time interval
            - "bands_mean": A dictionary of mean values for all bands
            - "ndvi_mean": The calculated NDVI mean value for the interval

    Returns:
        A list of predicted biomass values.
    """
    model.eval()  # Set the model to evaluation mode
    try:
        # Extract the band values and indices (NDVI, EVI) from the formatted data
        band_values = []
        for entry in formatted_data:
            bands_mean = entry["bands_mean"]
            ndvi_mean = entry.get("ndvi_mean", 0)  # NDVI mean value
            evi_mean = calculate_evi(bands_mean, logger)  # Calculate EVI (see helper function below)

            # Ensure the order of inputs matches the expected input format
            band_values.append([
                ndvi_mean,  # NDVI
                evi_mean,   # EVI
                bands_mean.get("B01", 0),
                bands_mean.get("B02", 0),
                bands_mean.get("B03", 0),
                bands_mean.get("B04", 0),
                bands_mean.get("B05", 0),
                bands_mean.get("B06", 0),
                bands_mean.get("B07", 0),
                bands_mean.get("B08", 0),
                bands_mean.get("B8A", 0),
                bands_mean.get("B11", 0),
                bands_mean.get("B12", 0)
            ])

        # Convert to a NumPy array for model input
        band_values = np.array(band_values)
        band_scaled = scaler_X.transform(band_values)
        band_values_tensor = torch.tensor(band_scaled, dtype=torch.float32)

        # Make predictions using the model
        with torch.no_grad():
            predictions = model(band_values_tensor)
            predictions_log = scaler_y.inverse_transform(predictions.numpy())
            predictions_mu = np.expm1(predictions_log)

        return predictions_mu

    except Exception as e:
        logger.error(f"Error in make_biomass_prediction: {e}")
        
        return "Error in prediction"
    

def convert_tree_biomass_array_to_CO2(tree_biomass_array, carbon_content_percentage=50):
    """
    Convert an array of tree biomass values to equivalent CO2 emissions.
    :param tree_biomass_array: Array of tree biomass values (in kilograms)
    :param carbon_content_percentage: Percentage of biomass that is carbon (default: 50%)
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

# Example usage
# tree_biomass_array = [100, 200, 300, 400]  # Example array of tree biomass in kilograms
# carbon_content = 50  # Carbon content percentage (default for trees)

# CO2_emissions_array = convert_tree_biomass_array_to_CO2(tree_biomass_array, carbon_content)
# print(f"CO2 emissions for each tree biomass: {CO2_emissions_array}")
