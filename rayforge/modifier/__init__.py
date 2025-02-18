# flake8: noqa:F401
import inspect
from .modifier import Modifier
from .transparency import MakeTransparent
from .grayscale import ToGrayscale

modifier_by_name = dict(
    [(name, obj) for name, obj in list(locals().items())
     if not name.startswith('_') or inspect.ismodule(obj)]
)
