import inspect
from typing import Callable

from torch.utils.data import DataLoader, SubsetRandomSampler


def to_markdown(string: str) -> str:
    """
    Formats linebreaks and indentation from python format to Markdown format.
    Replaces " " with "&nbsp;&nbsp;".
    Replaces "\n" with "<br />".
    """
    if string is not None:
        formatted_string = string.replace(" ", "&nbsp;&nbsp;").replace("\n", "<br />")
    else:
        formatted_string = "None"
    return formatted_string


def from_markdown(string: str) -> str:
    """
    Formats linebreaks and indentation from Markdown format to python format.
    Replaces "&nbsp;&nbsp;"  with " ".
    Replaces "<br />" with "\n".
    """
    if string is not None:
        formatted_string = string.replace("&nbsp;&nbsp;", " ").replace("<br />", "\n")
    else:
        formatted_string = "None"
    return formatted_string


def get_state_as_string(obj):
    """
    Returns a string representation of the given object with its state dict.
    """
    # Check if object has a state dict, if so parse it
    state_dict = getattr(obj, "state_dict", None)
    if callable(state_dict):
        # Start with the object name
        text = f"{str(obj.__class__.__name__)}("
        # Add every key, value pair
        for key, value in obj.state_dict().items():
            # Exclude private parameters of the state dict
            if not key.startswith("_"):
                text += f"\n  {key}: {value},"
        # Close the text
        text += "\n)"
    else:
        # Only use the object name
        text = f"{str(obj.__class__.__name__)}()"
    return text


def get_method_as_string(method: Callable):
    """
    Returns a string representation of the given method object.
    """
    return inspect.getsource(method)


def get_trainer_as_string(trainer):
    """
    Returns the basic parameters of this trainer as string. Used for cleaner logging to tensorboard.
    """
    return f"{trainer.__class__.__name__}(\n" \
           f"  num_epochs: {trainer.num_epochs}\n" \
           f"  seed: {trainer.seed}\n" \
           f"  device: {trainer.device}\n" \
           f")"


def get_data_loader_as_string(data_loader: DataLoader):
    """

    Parameters
    ----------
    data_loader

    Returns
    -------

    """
    formatted_data_set = str(data_loader.dataset).replace("\n", "\n  ")

    result = f"{data_loader.__class__.__name__}(\n" \
             f"  data_set: {formatted_data_set}\n" \
             f"  batch_size: {data_loader.batch_size}\n"

    if isinstance(data_loader.sampler, SubsetRandomSampler):
        result += f"  indices: {data_loader.sampler.indices}\n"
        result += f"  generator: {data_loader.sampler.generator}\n"
    elif isinstance(data_loader.sampler, list):
        result += f"  indices: {data_loader.sampler}\n"

    result += ")"

    return result
