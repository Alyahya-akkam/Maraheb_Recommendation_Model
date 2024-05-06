# main.py
from fastapi import FastAPI
from recommendation_router import router as recommendation_router
app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "nigga"}


app.include_router(recommendation_router, prefix="")
