# This module provides JWT authentication functionality
# It re-exports the existing functionality from the middleware module

from .middleware import JWTBearer, get_current_user

__all__ = ["JWTBearer", "get_current_user"]