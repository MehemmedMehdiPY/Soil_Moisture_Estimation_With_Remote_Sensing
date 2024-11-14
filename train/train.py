import torch
from typing import Tuple, Optional

class Trainer:
    def __init__(self, model: torch.nn.Module, train_loader: torch.utils.data.DataLoader, val_loader: torch.utils.data.DataLoader,
                 optimizer: torch.optim.Adam, loss_fn: torch.nn.modules.loss.BCELoss, epochs: int, filepath: str,
                 device: Optional[str] = None):
        """The class to support training process
        Args:
            model:                    Model to train
            train_loader:             Data Loader for training set
            val_loader:               Data Loader for validation set
            optimizer:                Optimizer
            loss_fn:                  Loss function
            epochs:                   The number of epochs for training
            filepath:                 Filepath to save the training model
            num_classes:              The number of channels in the output
            scheduler:                Learning scheduler
            is_context_loss:          If True, BiSeNet-V1 training will be adjusted
            device:                   Device to use trainer object
        """

        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.optimizer = optimizer
        self.loss_fn = loss_fn

        self.train_len = len(self.train_loader)
        self.val_len = len(self.val_loader)

        self.epochs = epochs
        self.filepath = filepath
        self.device = (device if device is not None else 'cpu')

    def train_model(self, epoch: int) -> float:

        self.model.train()
        train_loss = 0

        for i, (X, Y) in enumerate(self.train_loader):
            X = X.to(self.device)
            Y = Y.to(self.device)

            self.optimizer.zero_grad()

            out = self.model(X)
            loss = self.loss_fn(out, Y)

            loss_item = loss.item()
            train_loss += loss_item

            loss.backward()
            self.optimizer.step()

        train_loss = train_loss / self.train_len
        return train_loss

    def evaluate_model(self) -> Tuple[float]:

        self.model.eval()
        with torch.no_grad():
            test_loss = 0

            for X, Y in self.val_loader:
                X = X.to(self.device)
                Y = Y.to(self.device)

                pred = self.model(X)

                loss = self.loss_fn(pred, Y)
                test_loss += loss.item()

        test_loss = test_loss / self.val_len

        return test_loss

    def run(self, epoch_start: Optional[int] = 0) -> None:
        """The function to control training"""

        for epoch in range(epoch_start, self.epochs):
            print('-' * 50)

            train_loss = self.train_model(epoch)
            test_loss = self.evaluate_model()

            print(train_loss, test_loss)

    def save_model(self, filepath=None):
        if filepath is None:
            filepath = self.filepath
        checkpoints = self.model.state_dict()
        torch.save(checkpoints, filepath)
