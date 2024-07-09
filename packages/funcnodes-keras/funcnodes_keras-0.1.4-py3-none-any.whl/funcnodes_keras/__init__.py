import funcnodes as fn
from .applications import APPLICATION_NODE_SHELFE
from .fit import FIT_NODE_SHELFE
from .datasets import DATASETS_NODE_SHELFE

__version__ = "0.1.4"

NODE_SHELF = fn.Shelf(
    name="Keras",
    description="Tensorflow-Keras for funcnodes",
    nodes=[],
    subshelves=[DATASETS_NODE_SHELFE, APPLICATION_NODE_SHELFE, FIT_NODE_SHELFE],
)
