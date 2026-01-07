from bs4 import BeautifulSoup
import httpx
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI
from fastapi import FastAPI, HTTPException, Query, Request
from typing import Dict
import logging
from sqlalchemy.future import select
from RespModels import ResponeModel
from database import SessionDep, setup_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = AsyncOpenAI(api_key="",
                base_url="https://openrouter.ai/api/v1")


retell_prompt = 'Your task is simply to paraphrase the text from this fragment taken from the website. Dont say anything like, "Okay, Ill do it now," JUST paraphrase it. If the website is just a registration page or some kind of bot protection, just say you wont be able to read the data and explain why.'


async def get_text(url):
    async with httpx.AsyncClient(timeout=30) as http_client:
        rs = await  http_client.get(url)
        soup = BeautifulSoup(rs.text, 'lxml')
        for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
        all_text = soup.get_text()
            
    
    return all_text[:3000]
        
@app.post('/setup_history')
async def setup_history():
    await setup_db()
     
@app.get('/')
async def root():
     return{"message":"site-reteller"}


@app.get("/retell")
async def get_retell(url, session:SessionDep, request:Request) -> Dict[str, str]: 
    text = await get_text(url)

    if not text:
         raise HTTPException(status_code=400,
                             detail="No text found at the provided URL")
    response = await client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",  
        messages=[
            {"role": "user", "content": f"{retell_prompt}:\n\n{text}"}
        ],
        timeout=40
    )
    response = response.choices[0].message.content
    user_ip_address = request.client.host
    new_resp = ResponeModel()
    new_resp.user_IP = user_ip_address
    new_resp.response = response
    new_resp.URL = url
    session.add(new_resp)
    await session.commit()
    return {"response":response}


@app.get("/history")
async def get_history(session:SessionDep, request:Request):
    ip_address = request.client.host
    result = await session.execute(select(ResponeModel).where(ResponeModel.user_IP==ip_address))
    hist_objects = result.scalars().all()
    hist_list = []
    for obj in hist_objects:
         hist_list.append({
              "URL":obj.URL,
              "retell":obj.response,
         })
    return {
        "response":hist_list
    } 





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")