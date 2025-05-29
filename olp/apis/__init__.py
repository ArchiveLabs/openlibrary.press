
import stripe
import requests
from io import BytesIO
from internetarchive import session
from internetarchive import get_session
from olp.configs import IA_S3_KEYS

def download_book(item, filename):
    # Prevent BytesIO from being closed
    class UnclosableBytesIO(BytesIO):
        def close(self):
            pass  # override close to do nothing
    
    s = get_session({'s3': IA_S3_KEYS})
    book = s.get_item(item)
    file_obj = book.get_file(filename)
    file_stream = UnclosableBytesIO()
    success = file_obj.download(fileobj=file_stream)

    if not success:
        raise IOError(f"Download failed for {item_id}/{filename}")

    file_stream.seek(0)
    return file_stream


def stripe_fulfill(session_id):
    session = stripe.checkout.Session.retrieve(session_id)
    if session.payment_status != "paid":
        raise HTTPException(status_code=403, detail="Payment not completed")
    return session

def stripe_create_payment(domain, name, price, item, filename):
    return stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': name,
                    },
                    'unit_amount': price,
                },
                'quantity': 1,
                },
        ],
        mode='payment',
        success_url=f"{domain}/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{domain}/",
        metadata={
            "item": item,
            "filename": filename,
        }
    )    

