import httpx
from bs4 import BeautifulSoup

async def get_text(url):
    async with httpx.AsyncClient(timeout=30) as http_client:
        rs = await  http_client.get(url)
        soup = BeautifulSoup(rs.text, 'lxml')
        for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
        all_text = soup.get_text()
            
    
    return all_text[:3000]
