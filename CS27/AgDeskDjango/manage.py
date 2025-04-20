#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import torch.nn as nn

class ResidualBlock(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.fc1 = nn.Linear(dim, dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(dim, dim)
    def forward(self, x):
        identity = x
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return identity + out

class BiomassRegressor(nn.Module):
    def __init__(self, input_dim):
        super(BiomassRegressor, self).__init__()
        self.fc_in = nn.Linear(input_dim, 128)
        self.res1 = ResidualBlock(128)
        self.res2 = ResidualBlock(128)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        self.fc_out = nn.Linear(128, 1)
    def forward(self, x):
        x = self.relu(self.fc_in(x))
        x = self.res1(x)
        x = self.res2(x)
        x = self.dropout(x)
        x = self.fc_out(x)
        return x
    
    
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgDeskDjango.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
