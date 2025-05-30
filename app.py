from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import uvicorn

app = FastAPI()

class BatchRequest(BaseModel):
    batch_size: int
    query: str
    project_id: str

@app.post("/process-batch")
async def process_batch(request: BatchRequest):
    if request.batch_size < 50:
        return {"message": "initiated by fastapi"}
    
    # For batch_size >= 50, forward to n8n webhook
    n8n_webhook_url = "https://decibio-grazitti-abhay.app.n8n.cloud/webhook/profile-creator"
    
    headers = {
        "user-agent": 
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
"accept": 
"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",

        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "x-forwarded-for": "210.89.61.227, 172.68.214.85",
        "x-forwarded-host": "decibio-grazitti-abhay.app.n8n.cloud",
        "x-forwarded-port": "443",
        "x-forwarded-proto": "https",
        "x-forwarded-server": "traefik-prod-users-gwc-70-565db6c64f-d2bq9",
        "x-is-trusted": "yes",
        "x-real-ip": "210.89.61.227"
    }
    
    # Pass the same information as query parameters
    params = {
        "batch_size": request.batch_size,
        "query": request.query,
        "project_id": request.project_id
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            n8n_webhook_url,
            headers=headers,
            params=params
        )
        response.raise_for_status()
        return {"message": "initiated by n8n", "n8n_response": response.json()}

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",  # Allows external access
        port=8000,       # Port number
        reload=True      # Auto-reload on code changes
    )
