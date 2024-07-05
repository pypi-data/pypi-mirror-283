from starlette.middleware.cors import CORSMiddleware as CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware as GZipMiddleware
from starlette.middleware.httpsredirect import (
    HTTPSRedirectMiddleware as HTTPSRedirectMiddleware,
)
from starlette.middleware.trustedhost import (
    TrustedHostMiddleware as TrustedHostMiddleware,
)
from starlette.middleware.wsgi import WSGIMiddleware as WSGIMiddleware

from .errors import ServerErrorMiddleware
from .exceptions import ExceptionMiddleware
from .function import FunctionBasedMiddleware
from .middleware import EllarMiddleware as Middleware
from .versioning import RequestVersioningMiddleware

__all__ = [
    "Middleware",
    "FunctionBasedMiddleware",
    "CORSMiddleware",
    "ServerErrorMiddleware",
    "ExceptionMiddleware",
    "GZipMiddleware",
    "HTTPSRedirectMiddleware",
    "TrustedHostMiddleware",
    "WSGIMiddleware",
    "RequestVersioningMiddleware",
    "ServerErrorMiddleware",
]
