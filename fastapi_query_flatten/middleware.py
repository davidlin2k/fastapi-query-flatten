from typing import List, Tuple
from urllib.parse import urlencode

from fastapi.datastructures import QueryParams
from fastapi.requests import Request
from fastapi.responses import Response

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp


class QueryFlattenMiddleware(BaseHTTPMiddleware):
    def __init__(self: "QueryFlattenMiddleware", app: ASGIApp, delimiter: str = ","):
        super().__init__(app)
        self.delimiter = delimiter

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request.scope["query_string"] = self.query_flatten(request.query_params)

        return await call_next(request)

    def query_flatten(self, query: QueryParams) -> bytes:
        flattened: List[Tuple[str, str]] = []

        for key, value in query.multi_items():
            flattened.extend((key, entry) for entry in value.split(self.delimiter))

        return urlencode(flattened, doseq=True).encode("utf-8")
