from Crypto.Cipher import ARC4
from dotenv import load_dotenv


load_dotenv()

RC4_KEY = os.getenv("RC4_KEY")


class Encryptor:
    """
    Encryptor class that uses the ARC4 algorithm to encrypt and encode data.
    """

    def __init__(self, key: str = RC4_KEY) -> None:
        """
        Initializes the Encryptor with the given key.

        Args:
            key: The encryption key to use.
        """
        self.cipher = ARC4.new(key)

    def encrypt_encode(self, data: bytes) -> str:
        """
        Encrypts and encodes the given data using the initialized key.

        Args:
            data: The data to encrypt and encode.

        Returns:
            The encrypted and encoded data as a hexadecimal string.
        """
        return self.cipher.encrypt(data).hex()
