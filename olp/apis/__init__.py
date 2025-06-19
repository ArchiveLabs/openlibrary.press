
import stripe
import re
import requests
from io import BytesIO
from urllib.parse import urlparse
from internetarchive import session
from internetarchive import get_session
from olp.configs import IA_S3_KEYS

def download_book(item, formats=("epub",)):
    # Prevent BytesIO from being closed
    class UnclosableBytesIO(BytesIO):
        def close(self):
            pass  # override close to do nothing
    s = get_session({'s3': IA_S3_KEYS})
    book = s.get_item(item)
    for fmt in formats:
        filename_generator = (
            file['name'] for file in book.files
            if file['name'].lower().endswith(f".{fmt}")
        )
        if (filename := next(filename_generator, None)):
            file_obj = book.get_file(filename)
            file_stream = UnclosableBytesIO()
            if file_obj.download(fileobj=file_stream):
                file_stream.seek(0)
                return file_stream
            raise IOError(f"Download failed for {item}/{filename}")
    raise IOError(f"No files available for download")

class Lenny:
    @classmethod
    def redirect(cls, callback_url):
        return f"{urlparse(callback_url).path}/read/{olid}"

    @classmethod
    def upload(cls, callback_url: str, olid: str, file_content: BytesIO, encrypted: bool=True):
        match = re.search(r"(?:OL)?(\d+)[A-Z]?", olid, re.IGNORECASE)
        olid = match.group(1) if match else olid
        data_payload = {
            'openlibrary_edition': olid,
            'encrypted': str(encrypted).lower()
        }
        files_payload = {
            'file': ('book.epub', file_content, 'application/epub+zip')
        }
        response = requests.post(
            callback_url,
            data=data_payload,
            files=files_payload,
            timeout=120,
            verify=False
        )
        file_content.seek(0) # make sure stream position rewound to start
        logger.info(f"Upload response (OLID: {olid}): {response.content}")
        response.raise_for_status()
        return response

def stripe_fulfill(session_id):
    session = stripe.checkout.Session.retrieve(session_id)
    if session.payment_status != "paid":
        raise HTTPException(status_code=403, detail="Payment not completed")
    return session

def stripe_create_payment(domain, name, price, item, olid, callback_url=None):
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
            "olid": olid,
            "callback_url": callback_url or "",
        }
    )    
