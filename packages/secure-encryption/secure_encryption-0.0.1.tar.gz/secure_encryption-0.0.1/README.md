```markdown
# Secure Encryption

A simple and secure encryption service for Python.

## Features

- AES-256-CTR encryption and decryption
- HMAC-SHA512 message authentication
- Secure environment variable handling for encryption and MAC keys

## Installation

Install the package using pip:

```bash
pip install secure-encryption
```

## Usage

### Setting Up Environment Variables

Before using the `CryptoService`, you need to set up environment variables for the encryption and MAC keys. These keys should be base64 encoded 32-byte keys (for AES-256).

```python
import os
import base64

# Generate random keys and encode them in base64
encryption_key = base64.b64encode(os.urandom(32)).decode('utf-8')
mac_key = base64.b64encode(os.urandom(32)).decode('utf-8')

# Set environment variables
os.environ['CRYPTO_SERVICE_KEY'] = encryption_key
os.environ['CRYPTO_SERVICE_MAC_KEY'] = mac_key
```

### Encrypting a Message

To encrypt a plaintext message:

```python
from secure_encryption.crypto_service import CryptoService

plaintext = "This is a secret message."
encrypted_message = CryptoService.encrypt(plaintext)
print(f"Encrypted: {encrypted_message}")
```

### Decrypting a Message

To decrypt an encrypted message:

```python
from secure_encryption.crypto_service import CryptoService

decrypted_message = CryptoService.decrypt(encrypted_message)
print(f"Decrypted: {decrypted_message}")
```

### Example

```python
import os
import base64
from secure_encryption.crypto_service import CryptoService

# Generate and set keys
encryption_key = base64.b64encode(os.urandom(32)).decode('utf-8')
mac_key = base64.b64encode(os.urandom(32)).decode('utf-8')

os.environ['CRYPTO_SERVICE_KEY'] = encryption_key
os.environ['CRYPTO_SERVICE_MAC_KEY'] = mac_key

# Encrypt a message
plaintext = "This is a secret message."
encrypted_message = CryptoService.encrypt(plaintext)
print(f"Encrypted: {encrypted_message}")

# Decrypt the message
decrypted_message = CryptoService.decrypt(encrypted_message)
print(f"Decrypted: {decrypted_message}")
```

## Running Tests

Unit tests are provided using the `unittest` framework. To run the tests, use the following command:

```bash
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

This README file covers the basic usage, setup, and additional information about your `secure-encryption` package.