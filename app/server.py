from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import sys
import uvicorn

app = Starlette(debug=True)

# A list of origins that should be permitted to make cross-origin requests
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:8080"])


@app.route("/")
async def homepage(request):
    return JSONResponse({"hello": "world"})


if __name__ == "__main__":
    if "serve" in sys.argv:
        uvicorn.run(app, host="0.0.0.0", port=8000)

