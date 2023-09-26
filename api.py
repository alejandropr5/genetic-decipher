from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gencipher.model import GeneticDecipher
from gencipher_controller import router as gencipher_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.on_event("startup")
def load_model():
    gencipher = GeneticDecipher()
    print("Model loaded successfully!")
    app.state.model = gencipher


@app.on_event("shutdown")
def shutdown_event():
    print("Shutting down the application...")


app.include_router(gencipher_router, tags=["gencipher"], prefix="/gencipher")


@app.get("/hi")
def hi():
    return {"message": "Hello World from the API"}
