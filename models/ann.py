from torch import nn

class ANNModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.lc1 = nn.Linear(8, 128)
        self.lc2 = nn.Linear(128, 32)
        self.lc3 = nn.Linear(32, 16)
        self.lc4 = nn.Linear(16, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.lc1(x)
        x = self.relu(x)
        x = self.lc2(x)
        x = self.relu(x)
        x = self.lc3(x)
        x = self.relu(x)
        x = self.lc4(x)
        return x;