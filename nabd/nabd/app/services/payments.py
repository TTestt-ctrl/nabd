import moyasar
from flask import current_app


def charge(amount_halalas, description, source_token):
    moyasar.api_key = current_app.config["MOYASAR_SECRET_KEY"]
    payment = moyasar.Payment.create(
        amount=amount_halalas,
        currency="SAR",
        description=description,
        source={"type": "token", "token": source_token},
    )
    return {"id": payment.id, "status": payment.status}
