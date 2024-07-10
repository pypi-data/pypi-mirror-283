import logging
import sys
import io
from types import FunctionType
from typing import Callable, Union
from functools import wraps

class OutputLogger(io.TextIOBase):

    def __init__(
        self, 
        logger: logging.Logger,  
        output_name: 'stdout',
        level: int = logging.INFO
    ) -> None:
        
        super().__init__()
        self.output_name = output_name
        self.logger = logger
        self.level = level

    def __enter__(self):
        self.original_stream = getattr(sys, self.output_name)
        setattr(sys, self.output_name, self)

    def __exit__(self, _x, _y, _z):
        setattr(sys, self.output_name, self.original_stream)

    def write(self, s) -> None:
        if s := s.strip():
            self.logger.log(self.level, f"logger: {s}")
    
def log_output(
    fun: Callable = None, 
    *, 
    loggername: str = __name__,
    logger: Union[logging.Logger, None] = None,
    stdout_level: int = logging.INFO, 
    stderr_level: int = logging.ERROR
):
    """

If a function uses print or yields some output, capture it and log it
using the logging module.

Optional keyword arguments:
    * logger:  logger, by default root legger logging
    * stdout:  logging level of the standard output (by default INFO)
    * stderr:  logging level of the standard error (by default ERROR)

"""
    if logger is None:
        logger = logging.getLogger(loggername)

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            with OutputLogger(logger, 'stdout', level=stdout_level):
                with OutputLogger(logger, 'stderr', level=stderr_level):
                    return f(*args, **kwargs)
        
        return wrapper

    if fun:
        return decorator(fun)

    return decorator

import time

