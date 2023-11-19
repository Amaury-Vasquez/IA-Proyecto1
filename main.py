from fastapi import FastAPI
from routes.fifteen_puzzle import puzzle_router
 
app = FastAPI()
app.include_router(puzzle_router)

@app.get("/")
def root():
  return {"message": "Hello World"}