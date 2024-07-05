import os
import random
import shutil
import time
from typing import Callable

import numpy as np
import torch
import torchmetrics
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

from trainlogger import basics


class CustomValTrainer:
    """
    This class enables training with a train and validating dataset given a modular set of parameters.
    It supports the saving of the configuration to a file and rich logging to tensorboard.
    """

    def __init__(self,
                 num_epochs: int,
                 device: torch.device,
                 train_loader: torch.utils.data.DataLoader,
                 valid_loader: torch.utils.data.DataLoader,
                 model: torch.nn.Module,
                 optimizer: torch.optim.Optimizer,
                 loss_function: torch.nn.Module,
                 score_function: torchmetrics.Metric,
                 weight_init: Callable = None,
                 lr_scheduler: torch.optim.Optimizer = None,  # :torch.optim.lr_scheduler._LRScheduler
                 seed: int = None,
                 data_logger: Callable = None,
                 result_logger: Callable = None):

        self.num_epochs = num_epochs
        self.device = device
        self.train_loader = train_loader
        self.valid_loader = valid_loader
        self.model = model
        self.weight_init = weight_init
        self.optimizer = optimizer
        self.lr_scheduler = lr_scheduler
        self.loss_function = loss_function
        self.score_function = score_function
        self.seed = seed if seed is not None else int(time.time())
        self.data_logger = data_logger
        self.result_logger = result_logger

    @classmethod
    def from_file(cls, file_path):
        """
        Loads the object from the given file path via torch and returns it, if it is of this class.
        """
        trainer = torch.load(file_path)
        if isinstance(trainer, cls):
            return trainer
        else:
            return None

    def to_file(self, file_path):
        """
        Saves this object with its parameters at the given file path via torch.
        """
        # Create necessary directories
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        # Save this config object via torch
        torch.save(self, file_path)

    def load_state_dicts(self, file_path):
        """
        Loads the state dicts from the given file path via torch and applies them to the respective modules.
        """
        checkpoint = torch.load(file_path)
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        if self.lr_scheduler is not None:
            self.lr_scheduler.load_state_dict(checkpoint["scheduler_state_dict"])

    def save_state_dicts(self, file_path):
        """
        Saves the state dicts at the given file path via torch.
        """
        # Create necessary directories
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        # Save the state dicts via torch
        torch.save({"model_state_dict": self.model.state_dict(),
                    "optimizer_state_dict": self.optimizer.state_dict(),
                    "scheduler_state_dict": self.lr_scheduler.state_dict() if self.lr_scheduler is not None else None,
                    }, file_path)

    def to_tensorboard(self, writer: SummaryWriter) -> None:
        """
        Writes the parameters of this trainer as formatted Markdown text to the given tensorboard writer.
        """
        # Add every component of this config with a unique tag to tensorboard as Markdown text.
        writer.add_text(tag="00 Base Parameters",
                        text_string=basics.to_markdown(basics.get_trainer_as_string(self)))
        writer.add_text(tag="01 Train Dataset",
                        text_string=basics.to_markdown(basics.get_data_loader_as_string(self.train_loader)))
        writer.add_text(tag="02 Validation Dataset",
                        text_string=basics.to_markdown(basics.get_data_loader_as_string(self.valid_loader)))
        writer.add_text(tag="03 Model",
                        text_string=basics.to_markdown(str(self.model)))
        writer.add_text(tag="04 Weight Initialization",
                        text_string=basics.to_markdown(basics.get_method_as_string(self.weight_init)
                                                       if self.weight_init is not None else "None"))
        writer.add_text(tag="05 Optimizer",
                        text_string=basics.to_markdown(str(self.optimizer)))
        writer.add_text(tag="06 Learning Rate Scheduler",
                        text_string=basics.to_markdown(basics.get_state_as_string(self.lr_scheduler)
                                                       if self.lr_scheduler is not None else "None"))
        writer.add_text(tag="07 Loss Function",
                        text_string=basics.to_markdown(str(self.loss_function)))
        writer.add_text(tag="08 Score Function",
                        text_string=basics.to_markdown(str(self.score_function)))

        # Get one sample of the data with the right dimensions and use it to log the graph to tensorboard
        # data_sample, _ = next(iter(DataLoader(self.train_loader.dataset, batch_size=1)))
        # data_sample = data_sample.to(self.device)
        # writer.add_graph(self.model, data_sample)

    def _setup_training(self):
        # Set seeds
        torch.manual_seed(self.seed)
        random.seed(self.seed)
        np.random.seed(self.seed)

        # Move model and functions to device
        self.model.to(self.device)
        self.loss_function.to(self.device)
        self.score_function.to(self.device)

    def _start_logging(self, dir_path):
        # Clean up
        shutil.rmtree(dir_path, ignore_errors=True)

        # Save configuration and base states to disc
        config_path = os.path.join(dir_path, "base_config.pt")
        self.to_file(config_path)

        # Initialize logging
        summary_writer = SummaryWriter(dir_path)
        self.to_tensorboard(summary_writer)

        return summary_writer

    def train_valid_loop(self, dir_path: str) -> (float, float):
        """
        Executes training and validating a model.
        """
        # Setup
        self._setup_training()

        # Initialize logging
        summary_writer = self._start_logging(dir_path)

        # Initialize weights
        if self.weight_init is not None:
            self.model.apply(self.weight_init)

        # Initialize score
        best_valid_score = None

        # Train and validate
        for epoch in tqdm(range(1, self.num_epochs + 1), desc="Epochs", leave=False):
            # Log data one time to tensorboard
            if self.data_logger is not None and epoch == 1:
                self.data_logger(self.train_loader, summary_writer, "Training")
                self.data_logger(self.valid_loader, summary_writer, "Validating")

            # Execute training and validation
            train_loss, train_score = self._train()
            valid_loss, valid_score = self._validate()

            # Log to tensorboard
            summary_writer.add_scalar("Loss/Training", train_loss, epoch)
            summary_writer.add_scalar("Score/Training", train_score, epoch)
            summary_writer.add_scalar("Loss/Validation", valid_loss, epoch)
            summary_writer.add_scalar("Score/Validation", valid_score, epoch)

            # Update learning rate
            if self.lr_scheduler is not None:
                # Log previous lr to tensorboard
                summary_writer.add_scalar("Learning rate", self.optimizer.param_groups[0]["lr"], epoch)
                # Do step
                self.lr_scheduler.step()

            # Track the best performance, and save the model's state
            if (best_valid_score is None or
                    (self.score_function.higher_is_better and valid_score > best_valid_score) or
                    (not self.score_function.higher_is_better and valid_score < best_valid_score)):
                best_valid_score = valid_score
                best_model_path = os.path.join(dir_path, "best_model.pth")
                self.save_state_dicts(best_model_path)

        # Save the best score and add it to tensorboard
        summary_writer.add_text(tag="Score", text_string=f"{best_valid_score:.5f}")

        # Save the last model
        last_model_path = os.path.join(dir_path, "last_model.pth")
        self.save_state_dicts(last_model_path)

        # todo: result logger

        return best_valid_score

    def _train(self) -> (float, float):
        """
        Trains one epoch.
        """
        # Set model to train mode
        self.model.train()

        train_output = []
        train_target = []
        for batch_idx, (data, target) in enumerate(tqdm(self.train_loader, desc="Training", leave=False)):
            # Send data to GPU
            data = data.to(self.device).to(torch.float32)
            target = target.to(self.device).to(torch.float32)

            # Reset optimizer
            self.optimizer.zero_grad()

            # Make prediction
            output = self.model(data)

            # Make sure, that dimensions match
            target = target.squeeze()
            output = output.squeeze()

            # Calculate loss
            loss = self.loss_function(output, target)

            # Update weights
            loss.backward()
            self.optimizer.step()

            # Save
            train_output.extend(output.detach().cpu())
            train_target.extend(target.detach().cpu())

        # Calculate results of training
        train_loss = self.loss_function(torch.stack(train_output), torch.stack(train_target)).item()
        train_score = self.score_function(torch.stack(train_output), torch.stack(train_target)).item()

        return train_loss, train_score

    def _validate(self) -> (float, float):
        """
        Validates one epoch.
        """
        # Set model to eval mode
        self.model.eval()

        val_output = []
        val_target = []
        with torch.no_grad():
            for batch_idx, (data, target) in enumerate(tqdm(self.valid_loader, desc="Validating", leave=False)):
                # Send data to GPU
                data = data.to(self.device).to(torch.float32)
                target = target.to(self.device).to(torch.float32)

                # Make prediction
                output = self.model(data)

                # Make sure, that dimensions match
                target = target.squeeze()
                output = output.squeeze()

                # Save
                val_output.extend(output.detach().cpu())
                val_target.extend(target.detach().cpu())

        # Calculate results of validation
        val_loss = self.loss_function(torch.stack(val_output), torch.stack(val_target)).item()
        val_score = self.score_function(torch.stack(val_output), torch.stack(val_target)).item()

        return val_loss, val_score
