
# annoated integer variable x, that has a query to check if x is between 1 and 100
# if not, throw ValueError exception
# Normally annotated implementations are coded with decorators that we can reuse on functions
# Annotations rely on contextual logic that we write or another library such as Pydantic writes, on their onw; they do not do anything

from typing import Annotated, get_type_hints, get_origin, get_args
from functools import wraps


def check_value_rage(func):
    
    @wraps(func)
    def wrapped(x):
        # get any annotated type hints: include any related extra meta data
        type_hints = get_type_hints(double, include_extras=True)
        hint = type_hints['x']
        
        # if the hint, is an annotated hint, extra the meta data, and validate x according to that
        if get_origin(hint) is Annotated:
            # etracting the argumments, from annotated meta data
            hint_type, *hint_args = get_args(hint)
            low, high = hint_args[0]
            
            # checking if value is within low and how bounds as defined in the annotations
            if not low <= x <= high:
                raise ValueError(f"{x} falls outside boundary {low}-{high}")
            
        # if all is valid, execute and return the function
        return func(x)
    
    # return the wrapped function
    return wrapped

# validation within double function are now handled through a decorator; that extracts validation login from the annotated data passed with parameter
@check_value_rage
def double(x: Annotated[int, (0, 10)]) -> int:    
    return x * 2


result = double(20)
print(f"double results = {result}")