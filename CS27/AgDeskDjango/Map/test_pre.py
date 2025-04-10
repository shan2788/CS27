import random

def make_tree_recommendation(formatted_data):

    return random.choice(["Corn", "Mushroom", "Cabbage"])

def make_density_prediction(formatted_data):
 
    return round(random.uniform(200, 400), 2)

def fake_carbon_series(density):

    base = 1.5 + (density - 200) * 0.01
    return [round(base + 0.2 * i, 2) for i in range(5)]  # 给个5年