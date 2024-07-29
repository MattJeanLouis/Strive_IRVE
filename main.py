from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
public_key = os.getenv("STRIPE_PUBLIC_KEY")
base_url = os.getenv("BASE_URL")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "public_key": public_key})

@app.post("/create-checkout-session")
async def create_checkout_session():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': 'Recharge de véhicule électrique',
                },
                'unit_amount': 500,  # Montant en centimes (5,00 €)
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f'{base_url}/success',
        cancel_url=f'{base_url}/cancel',
    )
    return RedirectResponse(session.url, status_code=303)

@app.get("/success", response_class=HTMLResponse)
async def success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

@app.get("/cancel", response_class=HTMLResponse)
async def cancel(request: Request):
    return templates.TemplateResponse("cancel.html", {"request": request})
