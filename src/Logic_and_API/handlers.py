from typing import Dict
from fastapi import HTTPException, Request, APIRouter
from Models.RespModels import ResponseModel
from Database.history_database import SessionDep, setup_db
from Logic_and_API.logic_funcs import get_text
from config import retell_prompt, client
from sqlalchemy.future import select
from sqlalchemy import delete
from pydantic import HttpUrl


router = APIRouter()


@router.post('/setup_history')
async def setup_history():
    await setup_db()
     
@router.get('/')
async def root():
     return{"message":"site-reteller"}


@router.get("/retell")
async def get_retell(url:HttpUrl, session:SessionDep, request:Request) -> Dict[str, str]: 
    url = str(url)
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

    new_resp = ResponseModel()
    new_resp.user_IP = user_ip_address
    new_resp.response = response
    new_resp.URL = url
    
    session.add(new_resp)
    await session.commit()
    
    return {"response":response}


@router.get("/history")
async def get_history(session:SessionDep, request:Request):
    ip_address = request.client.host
    result = await session.execute(select(ResponseModel).where(ResponseModel.user_IP==ip_address))
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

@router.post("/history")
async def del_history(session:SessionDep,request:Request):
    ip_address = request.client.host
    query = delete(ResponseModel).where(ResponseModel.user_IP==ip_address)

    await session.execute(query)
    
    await session.commit()

    return {"response":"history deleted"}

