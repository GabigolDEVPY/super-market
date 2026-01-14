import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .handlers import payment

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    secret = settings.STRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, secret)
    except Exception:
        return HttpResponse(status=400)
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session["metadata"]
        print("chamar payment")
        payment(metadata)
        return HttpResponse(status=200)
    return HttpResponse(status=200)
