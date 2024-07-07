
import os
import base64
import unittest
from secure_encryption.crypto_service import CryptoService


class TestCryptoService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.encryption_key = base64.b64encode(os.urandom(32)).decode('utf-8')
        cls.mac_key = base64.b64encode(os.urandom(32)).decode('utf-8')
        os.environ['CRYPTO_SERVICE_KEY'] = cls.encryption_key
        os.environ['CRYPTO_SERVICE_MAC_KEY'] = cls.mac_key

    def test_encryption_decryption(self):
        plaintext = "This is a secret message."
        encrypted = CryptoService.encrypt(plaintext)
        decrypted = CryptoService.decrypt(encrypted)
        self.assertEqual(plaintext, decrypted)

    def test_invalid_mac(self):
        plaintext = "This is a secret message."
        encrypted = CryptoService.encrypt(plaintext)
        tampered_message = encrypted[:-1] + ("A" if encrypted[-1] != "A" else "B")  # noqa: E501
        with self.assertRaises(ValueError) as context:
            CryptoService.decrypt(tampered_message)
        self.assertTrue("Invalid MAC" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
