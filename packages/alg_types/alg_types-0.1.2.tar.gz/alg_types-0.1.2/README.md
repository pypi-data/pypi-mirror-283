# alg_types
`alg_types` is my attempt, more of a 'hack' to implement rust like enums in python.

# Examples
Here is an attempt to implement rust result using it
```python
from typing import TypeVar, Generic, Callable, Self
from alg_types import alg, variant
T,U = TypeVar("T"), TypeVar("U")
@alg
class Result(Generic[T,U]):
    @variant
    def Ok(x:T): ...

    @variant
    def Err(st:U): ...
    
    def is_ok(self):
        return isinstance(self, Result.Ok)
    
    def is_err(self):
        return isinstance(self, Result.Err)
    
    def map(self, f: Callable[[T], T]) -> Self:
        match self:
            case Result.Ok(x):
                return Result.Ok(f(x))
            case Result.Err(st):
                return Result.Err(st)
    
    def map_err(self, f: Callable[[U], U]) -> Self:
        match self:
            case Result.Ok(x):
                return Result.Ok(x)
            case Result.Err(st):
                return Result.Err(f(st))
    
    def unwrap(self) -> T:
        match self:
            case Result.Ok(x):
                return x
            case Result.Err(st):
                raise Exception(st)
    
    def unwrap_err(self) -> U:
        match self:
            case Result.Ok(x):
                raise Exception(x)
            case Result.Err(st):
                return st
    
    def unwrap_or(self, default: T) -> T:
        match self:
            case Result.Ok(x):
                return x
            case Result.Err(st):
                return default
    
    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        match self:
            case Result.Ok(x):
                return x
            case Result.Err(st):
                return f()
    
    def expect(self, msg: str) -> T:
        match self:
            case Result.Ok(x):
                return x
            case Result.Err(_st):
                raise Exception(msg)
    
x = Result.Err("1").map_err(lambda x: x + '1')
print(x)
```
outputs: `Result.Err(st='11')`
