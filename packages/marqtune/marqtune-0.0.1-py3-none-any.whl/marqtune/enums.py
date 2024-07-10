from enum import Enum


class ModelType(str, Enum):
    """
    Enum for model type.
    """
    OPEN_CLIP = "open_clip"
    MARQTUNED = "marqtuned"


class DatasetType(str, Enum):
    """
    Enum for dataset type.
    """
    TRAINING = "training"
    EVALUATION = "evaluation"


class InstanceType(str, Enum):
    """
    Enum for instance type.
    """
    BASIC = "marqtune.basic"
    LARGE = "marqtune.performance"
