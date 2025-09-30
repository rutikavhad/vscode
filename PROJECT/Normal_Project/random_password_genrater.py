#!/usr/bin/env python3
"""
pwtool.py
Secure password generator + SHA-256 hashing + reversible AES-GCM encryption (encode/decode).

Usage: run and follow prompts, or import functions into other code.
"""

import secrets
import string
import hashlib
import base64
from typing import Tuple
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ------------------------
# Password generator
# ------------------------
def generate_password(length: int = 24,
                      use_upper: bool = True,
                      use_digits: bool = True,
                      use_symbols: bool = True,
                      avoid_ambiguous: bool = True) -> str:
    if length < 8:
        raise ValueError("Use at least 8 characters for safety.")
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase if use_upper else ""
    digits = string.digits if use_digits else ""
    symbols = "!@#$%^&*()-_=+[]{};:,.<>?/|" if use_symbols else ""
    if avoid_ambiguous:
        # remove ambiguous characters like 0 O l 1 I
        for ch in "0O1Il":
            lower = lower.replace(ch, "")
            upper = upper.replace(ch, "")
            digits = digits.replace(ch, "")
    alphabet = "".join([s for s in (lower, upper, digits, symbols) if s])
    if not alphabet:
        raise ValueError("No character sets selected.")
    # ensure at least one of each selected class appears
    pw_chars = []
    if use_upper:
        pw_chars.append(secrets.choice(upper))
    if use_digits:
        pw_chars.append(secrets.choice(digits))
    if use_symbols:
        pw_chars.append(secrets.choice(symbols))
    # fill remaining
    while len(pw_chars) < length:
        pw_chars.append(secrets.choice(alphabet))
    # shuffle securely
    secrets.SystemRandom().shuffle(pw_chars)
    return "".join(pw_chars[:length])

# ------------------------
# SHA-256 hashing (one-way)
# ------------------------
def sha256_hash(text: str) -> str:
    b = text.encode("utf-8")
    digest = hashlib.sha256(b).hexdigest()
    return digest

# ------------------------
# AES-GCM encrypt/decrypt (reversible)
# Uses PBKDF2HMAC to derive a 256-bit key from a user password
# Format returned (base64): b64(salt(16) || nonce(12) || ciphertext || tag)
# ------------------------
def _derive_key(password: str, salt: bytes, iterations: int = 200_000) -> bytes:
    # PBKDF2 with SHA-256
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password.encode("utf-8"))

def encrypt_aes_gcm(plaintext: str, password: str) -> str:
    salt = secrets.token_bytes(16)           # store with ciphertext
    key = _derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = secrets.token_bytes(12)          # 96-bit nonce for AES-GCM
    ct = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), associated_data=None)
    blob = salt + nonce + ct
    return base64.urlsafe_b64encode(blob).decode("utf-8")

def decrypt_aes_gcm(token_b64: str, password: str) -> str:
    try:
        blob = base64.urlsafe_b64decode(token_b64.encode("utf-8"))
    except Exception as e:
        raise ValueError("Invalid token format / base64 decode failed.") from e
    if len(blob) < 16 + 12 + 16:
        # salt + nonce + at least a tag
        raise ValueError("Malformed token (too short).")
    salt = blob[:16]
    nonce = blob[16:28]
    ct = blob[28:]
    key = _derive_key(password, salt)
    aesgcm = AESGCM(key)
    try:
        pt = aesgcm.decrypt(nonce, ct, associated_data=None)
    except Exception as e:
        raise ValueError("Decryption failed. Wrong password or corrupted token.") from e
    return pt.decode("utf-8")

# ------------------------
# Simple CLI demo
# ------------------------
def demo_cli():
    print("Secure Password Generator + SHA-256 + AES-GCM encode/decode\n")
    while True:
        print("Choose an action:")
        print("  1) Generate a random password")
        print("  2) Hash (SHA-256) a string")
        print("  3) AES-GCM encrypt (encode) a string with passphrase")
        print("  4) AES-GCM decrypt (decode) a token with passphrase")
        print("  0) Exit")
        choice = input("Enter choice: ").strip()
        if choice == "0":
            break
        if choice == "1":
            L = input("Password length (default 24): ").strip()
            try:
                L = int(L) if L else 24
            except:
                L = 24
            pw = generate_password(length=L)
            print("\nGenerated password:\n", pw)
            print("SHA-256 hash:", sha256_hash(pw))
            print()
        elif choice == "2":
            s = input("String to hash: ")
            print("SHA-256:", sha256_hash(s))
            print()
        elif choice == "3":
            s = input("Plaintext to encrypt: ")
            p = input("Passphrase to derive key from (store securely): ")
            token = encrypt_aes_gcm(s, p)
            print("\nEncrypted token (copy/store this):\n", token)
            print()
        elif choice == "4":
            t = input("Token to decrypt (base64 token): ")
            p = input("Passphrase: ")
            try:
                pt = decrypt_aes_gcm(t, p)
                print("\nDecrypted plaintext:\n", pt)
            except Exception as e:
                print("Error:", e)
            print()
        else:
            print("Invalid choice, try again.\n")

if __name__ == "__main__":
    demo_cli()
