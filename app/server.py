import aiohttp
import asyncio
import uvicorn
import sys

from pathlib import Path

from fastai.vision import *
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

# from starlette.requests import Request
# from starlette.schemas import SchemaGenerator


# schemas = SchemaGenerator(
#     {"openapi": "3.0.0", "info": {"title": "Example API", "version": "1.0"}}
# )

learner_file_url = "https://drive.google.com/open?id=1nkIHl2pttPFy8n0rv5Msv_C1I-d5Jd8o"
learner_file_name = "export.pkl"

classes = ["pochard", "chaffinch", "pigeon"]
path = Path(__file__).parent


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


# async def download_file(url, dest):
#     if dest.exists():
#         return
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             data = await response.read()
#             with open(dest, "wb") as f:
#                 f.write(data)


async def setup_learner():
    # await download_file(learner_file_url, path / learner_file_name)
    # try:
    learn = load_learner("../server")
    return learn


# except RuntimeError as e:
#     if len(e.args) > 0 and "CPU-only machine" in e.args[0]:
#         print(e)
#         message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
#         raise RuntimeError(message)
#     else:
#         raise


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


@app.route("/upload", methods=["POST"])
async def analyze(request):
    img_data = await request.form()
    img_bytes = await (img_data["image"].read())
    img = open_image(BytesIO(img_bytes))
    prediction = learn.predict(img)[0]
    return JSONResponse({"result": str(prediction)})


# @app.route("/upload", methods=["POST"])
# async def upload(request):
#     data = await request.form()
#     bytes = await (data["file"].read())
#     return predict_image_from_bytes(bytes)


# @app.route("/classify-url", methods=["GET"])
# async def classify_url(request):
#     bytes = await get_bytes(request.query_params["url"])
#     return predict_image_from_bytes(bytes)


# def predict_image_from_bytes(bytes):
#     img = open_image(BytesIO(bytes))
#     losses = img.predict(cat_learner)
#     return JSONResponse({
#         "predictions": sorted(
#             zip(cat_learner.data.classes, map(float, losses)),
#             key=lambda p: p[1],
#             reverse=True
#         )
#     })


@app.route("/")
async def homepage(request):
    return JSONResponse({"hello": "world"})


# @app.route("/schema", methods=["GET"], include_in_schema=False)
# def openapi_schema(request):
#     return schemas.OpenAPIResponse(request=request)


if __name__ == "__main__":
    if "serve" in sys.argv:
        uvicorn.run(app, host="0.0.0.0", port=5000)

