import base64
import json
import secrets
from base64 import urlsafe_b64encode
from urllib.parse import urlparse, urlunparse
from datetime import date

STANDARD_HEADERS = {
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,es;q=0.8',
    'browser': 'Chrome',

    'priority': 'u=1, i',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}


def generate_secure_base64_string(length):
    num_bytes = (length * 3) // 4
    random_bytes = secrets.token_bytes(num_bytes)
    base64_string = urlsafe_b64encode(random_bytes).decode('utf-8')

    # Return the string truncated to the desired length
    return base64_string[:length]


def remove_path_from_url(url):
    parsed_url = urlparse(url)
    # Reconstruct the URL without the path, params, query, and fragment
    return urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))


def _base64url_decode(input):
    input += '=' * (-len(input) % 4)
    return base64.urlsafe_b64decode(input)


def load_jwt(jwt):
    try:
        header_segment, payload_segment, crypto_segment = jwt.split('.', 2)

        header = json.loads(_base64url_decode(header_segment))
        payload = json.loads(_base64url_decode(payload_segment))
        signature = _base64url_decode(crypto_segment)

        return header, payload, signature
    except Exception as e:  # (ValueError, TypeError)
        raise Exception("Unable to parse token") from e


def format_date(d: date):
    return d.isoformat() + "T06:00:00.000Z"


def format_date_end(d: date):
    return d.isoformat() + "T05:59:59.999Z"
