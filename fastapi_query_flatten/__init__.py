# A simple middleware to flatten query parameters in FastAPI

__version__ = "0.1.2"

from .middleware import QueryFlattenMiddleware

__all__ = ["QueryFlattenMiddleware"]
