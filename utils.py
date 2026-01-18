"""
Utility functions for RSA Digital Signature System
NPM: 202231310101
"""
import base64
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


def _202231310101_serialize_public_key(public_key):
    """Serialize public key to PEM format string"""
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem.decode('utf-8')


def _202231310101_serialize_private_key(private_key):
    """Serialize private key to PEM format string"""
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return pem.decode('utf-8')


def _202231310101_deserialize_public_key(pem_string):
    """Deserialize public key from PEM format string"""
    return serialization.load_pem_public_key(
        pem_string.encode('utf-8'),
        backend=default_backend()
    )


def _202231310101_deserialize_private_key(pem_string):
    """Deserialize private key from PEM format string"""
    return serialization.load_pem_private_key(
        pem_string.encode('utf-8'),
        password=None,
        backend=default_backend()
    )


def _202231310101_encode_signature_data(message, signature, public_key_pem):
    """Encode message, signature and public key into JSON format for QR Code"""
    data = {
        'message': message,
        'signature': base64.b64encode(signature).decode('utf-8'),
        'public_key': public_key_pem
    }
    return json.dumps(data)


def _202231310101_decode_signature_data(qr_data):
    """Decode JSON data from QR Code to extract message, signature and public key"""
    try:
        data = json.loads(qr_data)
        return {
            'message': data['message'],
            'signature': base64.b64decode(data['signature']),
            'public_key': data['public_key']
        }
    except Exception as e:
        raise ValueError(f"Invalid QR Code data format: {str(e)}")
