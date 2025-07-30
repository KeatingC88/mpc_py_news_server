import os
import base64
from dotenv import load_dotenv

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from app.Services.get_sha256_key import Get_SHA256_Key

load_dotenv()

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
ENCRYPTION_IV = os.getenv("ENCRYPTION_IV")
ENCRYPTION_FORMAT = os.getenv("ENCRYPTION_FORMAT")

def Encryptor(value: str) -> str:
    if ENCRYPTION_KEY and ENCRYPTION_IV:
        key = Get_SHA256_Key(ENCRYPTION_KEY)
        iv = ENCRYPTION_IV.encode(ENCRYPTION_FORMAT)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = pad(value.encode(ENCRYPTION_FORMAT), AES.block_size)
        encrypted = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted).decode(ENCRYPTION_FORMAT)
    return "error"