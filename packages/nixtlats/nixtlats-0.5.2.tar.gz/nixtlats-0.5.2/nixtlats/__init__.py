__version__ = "0.5.2"

from .nixtla_client import NixtlaClient, TimeGPT
import warnings
warnings.warn("This package is deprecated, please install nixtla instead.", category=FutureWarning)
