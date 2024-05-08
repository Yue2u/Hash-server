from fastapi import FastAPI, Request
from fastapi.responses import Response, JSONResponse
import hashlib


fastapi_app = FastAPI(
    title="Hash server api",
    description="API for hash server test task",
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url=None,
)


@fastapi_app.get("/healthcheck")
async def healthcheck():
    return Response(status_code=200)


@fastapi_app.post("/hash")
async def make_hash(request: Request):
    json_body = await request.json()
    if "string" not in json_body or not isinstance(json_body["string"], str):
        return JSONResponse(
            {"validation_errors": "field string is required"}, status_code=400
        )

    to_hash = json_body["string"].encode("UTF-8")
    return {"hash_string": hashlib.sha256(to_hash).hexdigest()}
