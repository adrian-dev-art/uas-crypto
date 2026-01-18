"""
RSA Digital Signature System with QRIS
UAS Kriptografi - NPM: 202231310101
"""

import streamlit as st
import hashlib
import qrcode
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

from utils import (
    _202231310101_serialize_public_key,
    _202231310101_serialize_private_key,
    _202231310101_deserialize_public_key,
    _202231310101_encode_signature_data,
    _202231310101_decode_signature_data
)


# ============= CORE CRYPTOGRAPHY FUNCTIONS =============

def _202231310101_generate_rsa_keys():
    """Generate RSA key pair (public and private keys)"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def _202231310101_hash_message(message):
    """Hash message using SHA-256"""
    return hashlib.sha256(message.encode('utf-8')).digest()


def _202231310101_sign_message(message, private_key):
    """Create digital signature by encrypting hash with private key"""
    message_hash = _202231310101_hash_message(message)
    signature = private_key.sign(
        message_hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


def _202231310101_verify_signature(message, signature, public_key):
    """Verify digital signature by decrypting with public key"""
    message_hash = _202231310101_hash_message(message)
    try:
        public_key.verify(
            signature,
            message_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False


def _202231310101_generate_qris(data):
    """Generate QRIS (QR Code) from signature data"""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    # Convert to RGB PIL Image for Streamlit compatibility
    return img.convert('RGB')


def _202231310101_decode_qris(image):
    """Decode QR Code to extract signature data"""
    # Convert PIL Image to numpy array for OpenCV
    img_array = np.array(image.convert('RGB'))
    # Convert RGB to BGR for OpenCV
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    # Use OpenCV QR Code detector
    detector = cv2.QRCodeDetector()
    data, vertices, _ = detector.detectAndDecode(img_bgr)

    if data:
        return data
    return None


# ============= STREAMLIT UI =============

def _202231310101_main():
    """Main Streamlit application"""

    # Page configuration
    st.set_page_config(
        page_title="RSA Digital Signature System",
        page_icon="🔒",
        layout="wide"
    )

    # Custom CSS for better UI
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #666;
            text-align: center;
            margin-bottom: 2rem;
        }
        .success-box {
            padding: 1rem;
            background-color: #d4edda;
            border-left: 4px solid #28a745;
            border-radius: 4px;
            margin: 1rem 0;
        }
        .error-box {
            padding: 1rem;
            background-color: #f8d7da;
            border-left: 4px solid #dc3545;
            border-radius: 4px;
            margin: 1rem 0;
        }
        .info-box {
            padding: 1rem;
            background-color: #d1ecf1;
            border-left: 4px solid #17a2b8;
            border-radius: 4px;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<div class="main-header">Sistem Tanda Tangan Digital RSA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">UAS Kriptografi - NPM: 202231310101</div>', unsafe_allow_html=True)

    # Mode selection
    mode = st.sidebar.radio(
        "Pilih Mode",
        ["Pengirim Pesan (Sender)", "Penerima Pesan (Receiver)"]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Tentang Sistem")
    st.sidebar.info(
        "Sistem ini menggunakan:\n"
        "- **RSA 2048-bit** untuk enkripsi\n"
        "- **SHA-256** untuk hashing\n"
        "- **QR Code** untuk distribusi signature"
    )

    if mode == "Pengirim Pesan (Sender)":
        _202231310101_sender_interface()
    else:
        _202231310101_receiver_interface()


def _202231310101_sender_interface():
    """Sender interface for signing messages"""
    st.header("Pengirim Pesan - Digital Signature")

    # Generate keys section
    st.subheader("1. Generate RSA Key Pair")

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Generate Keys", type="primary"):
            private_key, public_key = _202231310101_generate_rsa_keys()
            st.session_state.private_key = private_key
            st.session_state.public_key = public_key
            st.session_state.public_key_pem = _202231310101_serialize_public_key(public_key)
            st.session_state.private_key_pem = _202231310101_serialize_private_key(private_key)
            st.success("Keys generated successfully!")

    # Display keys if generated
    if 'public_key_pem' in st.session_state:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("**Public Key (PEM Format)**")
        st.code(st.session_state.public_key_pem, language="text")
        st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("Show Private Key (Keep Secret!)"):
            st.code(st.session_state.private_key_pem, language="text")

        # Message signing section
        st.markdown("---")
        st.subheader("2. Sign Message")

        message = st.text_area(
            "Masukkan pesan yang akan ditandatangani:",
            height=150,
            placeholder="Ketik pesan Anda di sini..."
        )

        if st.button("Sign Message & Generate QRIS", type="primary"):
            if message.strip():
                # Hash the message
                message_hash = _202231310101_hash_message(message)
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.markdown("**SHA-256 Hash:**")
                st.code(message_hash.hex(), language="text")
                st.markdown('</div>', unsafe_allow_html=True)

                # Sign the message
                signature = _202231310101_sign_message(message, st.session_state.private_key)
                st.session_state.signature = signature

                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.markdown("**Digital Signature (Base64):**")
                import base64
                st.code(base64.b64encode(signature).decode('utf-8'), language="text")
                st.markdown('</div>', unsafe_allow_html=True)

                # Generate QRIS
                st.markdown("---")
                st.subheader("3. QR Code Generated (QRIS Format)")

                qr_data = _202231310101_encode_signature_data(
                    message,
                    signature,
                    st.session_state.public_key_pem
                )

                qr_image = _202231310101_generate_qris(qr_data)

                # Display QRIS
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(qr_image, caption="QR Code - Digital Signature (QRIS Format)", use_container_width=True)

                # Download button
                buf = BytesIO()
                qr_image.save(buf, format="PNG")
                buf.seek(0)

                st.download_button(
                    label="Download QRIS",
                    data=buf,
                    file_name="digital_signature_qris.png",
                    mime="image/png"
                )

                st.success("Message signed and QRIS generated successfully!")
            else:
                st.error("Please enter a message to sign!")
    else:
        st.warning("Please generate RSA keys first!")


def _202231310101_receiver_interface():
    """Receiver interface for verifying signatures"""
    st.header("Penerima Pesan - Signature Verification")

    st.subheader("1. Upload QRIS")

    uploaded_file = st.file_uploader(
        "Upload QRIS image containing digital signature:",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        # Display uploaded QRIS
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded QR Code", use_container_width=True)

        st.markdown("---")
        st.subheader("2. Decode & Verify Signature")

        if st.button("Verify Signature", type="primary"):
            try:
                # Decode QR Code
                qr_data = _202231310101_decode_qris(image)

                if qr_data:
                    # Extract data
                    data = _202231310101_decode_signature_data(qr_data)
                    message = data['message']
                    signature = data['signature']
                    public_key_pem = data['public_key']

                    # Display message
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.markdown("**Message Content:**")
                    st.text_area("", value=message, height=150, disabled=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Display public key
                    with st.expander("Show Public Key"):
                        st.code(public_key_pem, language="text")

                    # Verify signature
                    public_key = _202231310101_deserialize_public_key(public_key_pem)
                    is_valid = _202231310101_verify_signature(message, signature, public_key)

                    st.markdown("---")
                    st.subheader("3. Verification Result")

                    if is_valid:
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.markdown("### SIGNATURE VALID")
                        st.markdown("""
                        **Status:** Tanda tangan digital **VALID**
                        **Keaslian:** Pesan ini **ASLI** dan belum dimodifikasi
                        **Pengirim:** Terverifikasi dengan public key yang diberikan
                        """)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-box">', unsafe_allow_html=True)
                        st.markdown("### SIGNATURE INVALID")
                        st.markdown("""
                        **Status:** Tanda tangan digital **TIDAK VALID**
                        **Peringatan:** Pesan mungkin telah dimodifikasi atau signature tidak cocok
                        **Tindakan:** Jangan percaya keaslian pesan ini
                        """)
                        st.markdown('</div>', unsafe_allow_html=True)

                    # Display hash for verification
                    message_hash = _202231310101_hash_message(message)
                    with st.expander("Show Technical Details"):
                        st.markdown("**SHA-256 Hash of Message:**")
                        st.code(message_hash.hex(), language="text")
                        st.markdown("**Digital Signature (Base64):**")
                        import base64
                        st.code(base64.b64encode(signature).decode('utf-8'), language="text")

                else:
                    st.error("Failed to decode QRIS. Please upload a valid QR code image.")

            except Exception as e:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.markdown(f"### Error")
                st.markdown(f"**Error Message:** {str(e)}")
                st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    _202231310101_main()
