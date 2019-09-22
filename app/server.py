import aiohttp
import asyncio
import uvicorn
import sys

# from fastai.vision import *
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

# from starlette.requests import Request
from starlette.schemas import SchemaGenerator


schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Example API", "version": "1.0"}}
)
app = Starlette(debug=True)

# A list of origins that should be permitted to make cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "https://bird-vue.onrender.com",
        "https://www.bird-vue.onrnender.com",
        "http://localhost:8081",
    ],
)


@app.route("/upload", methods=["POST"])
async def upload(request):
    img_data = await request.form()
    img_bytes = await (img_data["image"].read())
    img = BytesIO(img_bytes)
    # # prediction = learn.predict(img)[0]
    return JSONResponse({"result": str(list(img))})
    # return JSONResponse({"result": "Hello!"})


# bytes = await (data["file"].read())
# return predict_image_from_bytes(bytes)


@app.route("/")
async def homepage(request):
    return JSONResponse({"hello": "world"})


@app.route("/schema", methods=["GET"], include_in_schema=False)
def openapi_schema(request):
    return schemas.OpenAPIResponse(request=request)


if __name__ == "__main__":
    if "serve" in sys.argv:
        uvicorn.run(app, host="0.0.0.0", port=5000)

