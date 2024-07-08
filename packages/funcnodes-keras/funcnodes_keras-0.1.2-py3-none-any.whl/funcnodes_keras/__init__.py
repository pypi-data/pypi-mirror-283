import funcnodes as fn
from .applications import APPLICATION_NODE_SHELFE
from .fit import FIT_NODE_SHELFE

__version__ = "0.1.2"

NODE_SHELF = fn.Shelf(
    name="Keras",
    description="Tensorflow-Keras for funcnodes",
    nodes=[],
    subshelves=[APPLICATION_NODE_SHELFE, FIT_NODE_SHELFE],
)
