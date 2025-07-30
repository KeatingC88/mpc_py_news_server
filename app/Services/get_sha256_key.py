import os
import base64
from Crypto.Hash import SHA256
from dotenv import load_dotenv

load_dotenv()

ENCRYPTION_FORMAT = os.getenv("ENCRYPTION_FORMAT")

def Get_SHA256_Key(key: str) -> bytes:
    sha = SHA256.new()
    sha.update(key.encode(ENCRYPTION_FORMAT))
    return sha.digest()