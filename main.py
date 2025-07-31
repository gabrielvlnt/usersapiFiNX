import uvicorn
from api.v1.endpoints.user import user_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.session import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://0.0.0.0:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
