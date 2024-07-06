from typing import Union, Optional, Iterator, Tuple, Callable
import numpy as np
from funcnodes import Shelf, NodeDecorator
from exposedfunctionality import controlled_wrapper
from enum import Enum
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.optimizers import Optimizer





class OptimizerNames(Enum):
    adam = "adam"
    sgd = "sgd"
    rmsprop = "rmsprop"
    adamw = "adamw"
    adagrad = "adagrad"
    adadelta = "adadelta"
    adamax = "adamax"
    adamfactor = "adamfactor"
    nadam = "nadam"
    ftrl = "ftrl"
    lion = "lion"
    loss_scale_opt = "loss scale optizer"

    @classmethod
    def default(cls):
        return cls.rmsprop.value


@NodeDecorator(
    node_id="tensorflow.keras.training.compile ",
    name="compile ",
)
# @controlled_wrapper(compile , wrapper_attribute="__fnwrapped__")
def _compile(
    model: Model,
    optimizer: Union[OptimizerNames, Optimizer]=OptimizerNames.default(),
    loss=None,
    loss_weights=None,
    metrics=None,
    weighted_metrics=None,
    run_eagerly=False,
    steps_per_execution=1,
    jit_compile="auto",
    auto_scale_loss=True,
) -> Model:
    return model.compile(
        optimizer=optimizer,
        loss=loss,
        loss_weights=loss_weights,
        metrics=metrics,
        weighted_metrics=weighted_metrics,
        run_eagerly=run_eagerly,
        steps_per_execution=steps_per_execution,
        jit_compile=jit_compile,
        auto_scale_loss=auto_scale_loss,
    )