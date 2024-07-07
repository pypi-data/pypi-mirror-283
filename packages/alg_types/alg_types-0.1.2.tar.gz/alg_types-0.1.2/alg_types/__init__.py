import inspect
from dataclasses import dataclass
from typing import Callable, Any

def variant(f: Callable):
    return inspect.signature(f)

def alg(f: type):
    for name, value in inspect.getmembers(f):
        if isinstance(value, inspect.Signature):
            class Wrapper(f):
                __qualname__ = f.__qualname__ + "." + name
                __annotations__ = {k:v.annotation for k,v in value.parameters.items()}
            for k,v in value.parameters.items():
                if v.default != inspect.Parameter.empty:
                    setattr(Wrapper, k, v.default)
            Wrapper = dataclass(Wrapper) #type: ignore
            setattr(f, name, Wrapper)
    return f