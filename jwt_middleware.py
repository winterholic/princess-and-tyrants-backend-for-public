from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
import jwt
from fastapi.security import APIKeyHeader
import logging

log = logging.getLogger(__name__)

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

secret_key = "시크릿 키"

class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allowed_routes=None, excluded_prefixes=None):
        super().__init__(app)
        self.allowed_routes = allowed_routes or []
        self.excluded_prefixes = excluded_prefixes or []

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            for prefix in self.excluded_prefixes:
                if request.url.path.startswith(prefix):
                    return await call_next(request)
            allowed = False
            for route in self.allowed_routes:
                if request.url.path == route or request.url.path.startswith(route + "/"):
                    allowed = True
                    break
            if allowed:
                return await call_next(request)

        for prefix in self.excluded_prefixes:
            if request.url.path.startswith(prefix):
                return await call_next(request)

        if "Authorization" not in request.headers:
            return JSONResponse(status_code=499, content={"message": "헤더에 토큰이 없습니다."})

        auth_header = request.headers["Authorization"]
        if not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=499, content={"message": "헤더에 토큰 형식이 잘못되었습니다."})

        token = auth_header.split(" ")[1]
        try:
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            request.state.user = decoded_token
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=499, content={"message": "토큰이 만료되었습니다."})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=499, content={"message": "잘못된 토큰입니다."})

        response = await call_next(request)
        return response


class BlockUndefinedRoutesMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allowed_routes, excluded_prefixes=None):
        super().__init__(app)
        self.allowed_routes = allowed_routes
        self.excluded_prefixes = excluded_prefixes or []

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            for prefix in self.excluded_prefixes:
                if request.url.path.startswith(prefix):
                    return await call_next(request)
            allowed = False
            for route in self.allowed_routes:
                if request.url.path == route or request.url.path.startswith(route + "/"):
                    allowed = True
                    break
            if allowed:
                return await call_next(request)

        for prefix in self.excluded_prefixes:
            if request.url.path.startswith(prefix):
                return await call_next(request)

        allowed = False
        for route in self.allowed_routes:
            if request.url.path == route or request.url.path.startswith(route + "/"):
                allowed = True
                break
        if not allowed:
            log.error(f"★★★★★허용되지 않은 경로★★★★★ : {request.url.path}")
            return JSONResponse(status_code=404, content={"message": f"허용되지 않은 url: {request.url.path}"})

        response = await call_next(request)
        return response