import os
import base64

from datetime import datetime, timezone
from dotenv import load_dotenv
from jose import jwt, JWTError

from app.Services.decryptor import Decryptor

load_dotenv()

JWT_ISSUER_KEY = os.getenv("JWT_ISSUER_KEY")
JWT_CLIENT_KEY = os.getenv("JWT_CLIENT_KEY")
JWT_CLIENT_ADDRESS = os.getenv("JWT_CLIENT_ADDRESS")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"

def Authenticate_JWT_Claims(token: str) -> bool:
    try:
        decoded_token = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={"verify_aud": False}
        )
        
        aud_encrypted = decoded_token.get("aud")

        if aud_encrypted:
            decrypted_aud = Decryptor(aud_encrypted)
            if decrypted_aud != JWT_CLIENT_KEY:
                return False

        iss_encrypted = decoded_token.get("iss")
        if iss_encrypted:
            decrypted_iss = Decryptor(iss_encrypted)
            if decrypted_iss != JWT_ISSUER_KEY:
                return False

        for key, value in decoded_token.items():
            if "webpage" in key.lower():
                if isinstance(value, str):
                    decrypted_webpage = Decryptor(value)
                    if decrypted_webpage != JWT_CLIENT_ADDRESS:
                        return False
                break

        exp = decoded_token.get("exp")
        if exp:
            now = datetime.now(timezone.utc).timestamp()
            if now >= exp:
                return False

        return True

    except JWTError as e:
        return False
    except Exception as e:
        return False