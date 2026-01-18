# README - RSA Digital Signature System with QR Code

## Project Information
- **Mata Kuliah**: Kriptografi
- **NPM**: 202231310101
- **Dosen**: Deni Suprihadi, S.T, M.KOM, MCE
- **Tahun Akademik**: 2025-2026

## Overview
System tanda tangan digital berbasis RSA yang menggunakan SHA-256 untuk hashing dan QR Code (format QRIS) untuk distribusi signature. Aplikasi ini dibangun menggunakan Python dan Streamlit framework.

## Features
- Generate RSA key pair (2048-bit)
- Hash message using SHA-256
- Create digital signature with RSA private key
- Generate QR Code containing signature data
- Verify signature using RSA public key
- Modern and attractive Streamlit interface
- Separate sender and receiver interfaces

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Usage

### Sender Mode (Pengirim Pesan)
1. Click "Generate Keys" to create RSA key pair
2. Enter your message in the text area
3. Click "Sign Message & Generate QRIS"
4. Download the generated QR Code
5. Share the QR Code with the receiver

### Receiver Mode (Penerima Pesan)
1. Upload the QR Code image
2. Click "Verify Signature"
3. View the message and verification result
4. Check technical details if needed

## Technical Details

### Algorithms Used
- **RSA**: 2048-bit key size for public-key cryptography
- **SHA-256**: Cryptographic hash function for message integrity
- **RSA-PSS**: Probabilistic signature scheme for signing
- **QR Code**: Quick Response code for data encoding

### Security Features
1. **Authentication**: Confirms the sender's identity via public key
2. **Integrity**: Detects any changes to the message
3. **Non-repudiation**: Sender cannot deny sending the message

### Function Naming Convention
All functions are prefixed with NPM `202231310101_` as per exam requirements:
- `_202231310101_generate_rsa_keys()`
- `_202231310101_hash_message()`
- `_202231310101_sign_message()`
- `_202231310101_verify_signature()`
- `_202231310101_generate_qris()`
- `_202231310101_decode_qris()`
- And more...

## File Structure
```
streamlit_kripto/
├── app.py                  # Main Streamlit application
├── utils.py                # Utility functions for keys and data
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── TESTING_GUIDE.md       # Detailed testing instructions
```

## Dependencies
- `streamlit` - Web framework
- `cryptography` - RSA implementation
- `qrcode` - QR code generation
- `Pillow` - Image processing
- `pyzbar` - QR code decoding
- `numpy` - Array processing
- `PyPDF2` - PDF processing

## Screenshots
(Add screenshots here when creating documentation)

## License
Educational project for UAS Kriptografi

## Author
NPM: 202231310101
