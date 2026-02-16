from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time 
from datetime import datetime, timezone

from backend.utils.logging import logger as log

class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, duration of execution. Logs should be printed using the custom logging module provided.
        Logs should be printed so that they are easily readable and understandable.

        :param request: Request received to this middleware from client (it is supplied by FastAPI)
        :param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        :return: Response from endpoint
        """
        # TODO:(Member) Finish implementing this method

        start_time = time.perf_counter()
        request_time = datetime.now(timezone.utc).isoformat()

        method = request.method
        url = str(request.url)
        query_params = dict(request.query_params)

        response = await call_next(request)

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        log.info(
            "Request | time={} | method={} | url={} | query={} | status={} | duration_ms={:.2f}",
            request_time,
            method,
            url,
            query_params,
            response.status_code,
            duration_ms,
        )

        return response
