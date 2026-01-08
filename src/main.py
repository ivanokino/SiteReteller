import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import logging
from Logic_and_API.handlers import router as api_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(api_router)

app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

        
if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", reload=True)