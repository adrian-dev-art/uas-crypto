# Testing Guide - RSA Digital Signature System

## NPM: 202231310101

## Quick Test Steps

### Testing Sender Flow
1. Run the application: `streamlit run app.py`
2. Select "Pengirim Pesan (Sender)" mode
3. Click "Generate Keys" button
4. Verify public and private keys are displayed
5. Enter a test message: "Ini adalah pesan rahasia untuk UAS Kriptografi"
6. Click "Sign Message & Generate QRIS"
7. Verify:
   - SHA-256 hash is displayed
   - Digital signature (Base64) is shown
   - QR Code image is generated and displayed
   - Download button appears
8. Download the QR code image

### Testing Receiver Flow
1. Switch to "Penerima Pesan (Receiver)" mode
2. Upload the QR code image you downloaded
3. Click "Verify Signature"
4. Verify:
   - Original message is displayed correctly
   - Public key is shown in expander
   - Signature verification shows "SIGNATURE VALID"
   - Technical details show matching hash

### Testing Invalid Signature (Optional)
1. Manually edit the QR code or message
2. Try to verify
3. Should show "SIGNATURE INVALID"

## All Functions with NPM Prefix (202231310101)

### Core Cryptography
- `_202231310101_generate_rsa_keys()` - Generate RSA key pair
- `_202231310101_hash_message()` - Hash message with SHA-256
- `_202231310101_sign_message()` - Create digital signature
- `_202231310101_verify_signature()` - Verify digital signature
- `_202231310101_generate_qris()` - Generate QR code
- `_202231310101_decode_qris()` - Decode QR code

### Utility Functions (utils.py)
- `_202231310101_serialize_public_key()` - Convert public key to PEM
- `_202231310101_serialize_private_key()` - Convert private key to PEM
- `_202231310101_deserialize_public_key()` - Load public key from PEM
- `_202231310101_deserialize_private_key()` - Load private key from PEM
- `_202231310101_encode_signature_data()` - Encode data to JSON for QR
- `_202231310101_decode_signature_data()` - Decode JSON from QR

### UI Functions
- `_202231310101_main()` - Main application
- `_202231310101_sender_interface()` - Sender UI
- `_202231310101_receiver_interface()` - Receiver UI

## Project Structure
```
streamlit_kripto/
├── app.py                          # Main Streamlit application
├── utils.py                        # Utility functions
├── requirements.txt                # Dependencies
├── extract_pdf.py                  # PDF extraction tool
├── 20260105-UAS-Kriptografi.pdf   # Original exam requirements
└── 20260105-UAS-Kriptografi.txt   # Extracted text
```

## Technical Implementation Summary

1. **RSA Key Generation**: 2048-bit keys using cryptography library
2. **Hashing**: SHA-256 for message integrity
3. **Signing**: RSA-PSS with MGF1(SHA-256) padding
4. **Verification**: Public key verification with same padding
5. **QR Code**: Contains JSON with message, signature (base64), and public key
6. **UI**: Streamlit with custom CSS for modern appearance
