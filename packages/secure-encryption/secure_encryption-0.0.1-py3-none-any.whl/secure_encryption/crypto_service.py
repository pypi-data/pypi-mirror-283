import os
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from typing import Optional


class CryptoService:
    algorithm = 'aes-256-ctr'
    key_length = 32  # aes-256 requires a 32-byte key
    nonce_length = 16

    @staticmethod
    def get_key(key: Optional[str]) -> bytes:
        if key is None:
            raise ValueError("Key not set in environment variables.")
        buffer = base64.b64decode(key)
        if len(buffer) != CryptoService.key_length:
            raise ValueError(
                f"Invalid key length. Key must be {CryptoService.key_length} bytes long."  # noqa: E501
            )
        return buffer

    @staticmethod
    def encrypt(plaintext: str) -> str:
        encryption_key = CryptoService.get_key(os.getenv('CRYPTO_SERVICE_KEY'))
        mac_key = CryptoService.get_key(os.getenv('CRYPTO_SERVICE_MAC_KEY'))

        nonce = get_random_bytes(CryptoService.nonce_length)
        cipher = AES.new(encryption_key, AES.MODE_CTR, nonce=nonce)
        ciphertext = cipher.encrypt(plaintext.encode('utf-8'))

        mac = hashlib.sha512()
        mac.update(nonce + ciphertext)
        mac = mac_key + mac.digest()

        return base64.b64encode(mac + nonce + ciphertext).decode('utf-8')

    @staticmethod
    def decrypt(message: str) -> str:
        encryption_key = CryptoService.get_key(os.getenv('CRYPTO_SERVICE_KEY'))
        mac_key = CryptoService.get_key(os.getenv('CRYPTO_SERVICE_MAC_KEY'))

        decoded = base64.b64decode(message)
        mac = decoded[:64]
        nonce = decoded[64:80]
        ciphertext = decoded[80:]

        calc_mac = hashlib.sha512()
        calc_mac.update(nonce + ciphertext)
        calc_mac = mac_key + calc_mac.digest()

        if mac != calc_mac:
            raise ValueError("Invalid MAC")

        cipher = AES.new(encryption_key, AES.MODE_CTR, nonce=nonce)
        decrypted_data = cipher.decrypt(ciphertext)

        return decrypted_data.decode('utf-8')
