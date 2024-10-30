import requests
import os

from fastapi import HTTPException, status, Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware


from models.order import OrderBody, OrderResponse

URL_TOKEN = os.getenv("URL_TOKEN", "")
URL_ORDER = os.getenv("URL_ORDER", "")
URL_ORIGIN = os.getenv("URL_ORIGIN", "")
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
    allow_origins=[URL_ORIGIN],  # Or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def hello_world():
    return {
        "response": "API is working!"
    }


def get_access_token() -> str | None:
    print("get_access_token - start")
    token = requests.post(URL_TOKEN, data=data)
    access_token = None
    try:
        access_token = token.json()["access_token"]
    except:
        print("get_access_token - issue with getting the token")

    print("get_access_token - end")
    return access_token


def get_order_body(order: OrderBody, request: Request) -> dict:
    print("get_order_body - start")
    amount = order.amount
    currency = order.currency
    client_id = request.client.host

    order_body = {
        "continueUrl": URL_ORIGIN,
        "customerIp": client_id,
        "merchantPosId": "485425",
        "description": "Donation Marikate Polska",
        "currencyCode": currency.PLN.value,
        # has to be multiplied based on the PayU documentation
        "totalAmount": str(int(amount) * 100)
    }

    print(f"get_order_body - end, {order_body}")
    return order_body


@app.post('/create-order', response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderBody, request: Request):
    print("/create-order - start")
    access_token = get_access_token()
    if not access_token:
        raise HTTPException(status_code=404, detail="Cannot access token")

    order_body = get_order_body(order, request)
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    response = requests.post(URL_ORDER, headers=headers, json=order_body)
    print(response)
    if not response.ok:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    print("/create-order - end")
    return OrderResponse(payu_url=response.url)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
