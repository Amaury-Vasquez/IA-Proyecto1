from fastapi import FastAPI
from routes.fifteen_puzzle import puzzle_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Setting up CORS
origins = ["http://127.0.0.1:3000"]
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Including routes
app.include_router(puzzle_router)

@app.get("/")
def root():
  return {"message": "Hello World"}