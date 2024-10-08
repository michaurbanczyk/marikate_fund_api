from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

URL_TOKEN = os.getenv('URL_TOKEN', "")
URL_ORDER = os.getenv('URL_ORDER', "")
CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")

data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
}
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63343"],  # Or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.post('/create-order')
def create_order(request: Request):
    get_token = requests.post(URL_TOKEN, data=data)
    access_token = get_token.json()["access_token"]
    client_id = request.client.host

    create_order_body = {
        "continueUrl": "https://marikate-fund-modern-dev.vercel.app/success",
        "customerIp": client_id,
        "merchantPosId": "485425",
        "description": "RTV market",
        "currencyCode": "PLN",
        "totalAmount": "21000"
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(URL_ORDER, headers=headers, json=create_order_body)
    return {
        "payuUrl": response.url
    }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
