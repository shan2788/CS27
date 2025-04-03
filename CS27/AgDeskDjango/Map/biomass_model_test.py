import torch
import numpy as np

class BiomassRegressor(torch.nn.Module):
    def __init__(self, input_dim):
        super(BiomassRegressor, self).__init__()
        self.model = torch.nn.Sequential(
            torch.nn.Linear(input_dim, 128),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.3),
            torch.nn.Linear(128, 64),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.3),
            torch.nn.Linear(64, 32),
            torch.nn.ReLU(),
            torch.nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.model(x)

input_dim = 13

# 加载模型
model = torch.load('biomass_model.pkl', weights_only=False)
model.eval()

sample_data = np.array(
    [0.55, 0.42, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110],
  )

# 转换为 torch 张量
sample_tensor = torch.tensor(sample_data, dtype=torch.float32)

with torch.no_grad():
    predictions = model(sample_tensor)

print(predictions.numpy())