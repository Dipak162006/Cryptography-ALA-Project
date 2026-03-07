from flask import Flask, render_template, request
import hashlib
import math
import hmac
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
import base64


app = Flask(__name__)

# -------------------------
# Helper Functions
# -------------------------

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime(min_val=10, max_val=50):
    import random
    while True:
        p = random.randint(min_val, max_val)
        if is_prime(p):
            return p

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_inverse(e, phi):
    """
    Computes the modular multiplicative inverse of e modulo phi using EEA.
    Finds d such that (d * e) % phi == 1.
    """
    gcd_val, x, y = extended_gcd(e, phi)
    if gcd_val != 1:
        return None  # Modular inverse does not exist
    else:
        # x might be negative, so we add phi to make it positive
        return (x % phi + phi) % phi

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ala1", methods=["GET"])
def ala1():
    return render_template("ala1.html")

@app.route("/generate_keys", methods=["POST"])
def generate_keys():
    print("--- KEY GENERATION STARTED ---")
    p = generate_prime(50, 100)
    q = generate_prime(50, 100)
    while p == q:
        q = generate_prime(50, 100)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose e
    e = 3
    while e < phi:
        if gcd(e, phi) == 1:
            break
        e += 1
        
    d = mod_inverse(e, phi)
    
    print(f"Prime p: {p}")
    print(f"Prime q: {q}")
    print(f"Modulus n: {n}")
    print(f"Public Key (e,n): ({e},{n})")
    print(f"Private Key (d,n): ({d},{n})")
    
    return {
        "p": p,
        "q": q,
        "n": n,
        "phi": phi,
        "e": e,
        "d": d
    }

@app.route("/sign", methods=["POST"])
def sign():
    message = request.form.get("message", "")
    d = int(request.form.get("d", 0))
    n = int(request.form.get("n", 0))
    
    print("\n--- SIGNING PROCESS ---")
    print(f"Original Message: {message}")
    
    # 1. Hash the message
    msg_hash = hashlib.sha256(message.encode()).hexdigest()
    print(f"SHA-256 Hash: {msg_hash}")
    
    # Convert hex hash to integer for RSA math
    # We take modulo n so it fits within the RSA block size for our small primes
    hash_int = int(msg_hash, 16) % n
    
    # 2. Sign using private key
    signature = pow(hash_int, d, n)
    # Return as hex for display
    hex_sig = hex(signature)[2:].upper()
    print(f"Digital Signature: {hex_sig}")
    
    return {
        "hash": msg_hash,
        "signature": hex_sig
    }

@app.route("/verify", methods=["POST"])
def verify():
    message = request.form.get("message", "")
    hex_sig = request.form.get("signature", "")
    e = int(request.form.get("e", 0))
    n = int(request.form.get("n", 0))
    
    print("\n--- VERIFICATION PROCESS ---")
    print(f"Message Used: {message}")
    
    # 1. Hash incoming message
    msg_hash = hashlib.sha256(message.encode()).hexdigest()
    print(f"Hash: {msg_hash}")
    hash_int = int(msg_hash, 16) % n
    
    # 2. Decrypt signature using public key
    try:
        signature = int(hex_sig, 16)
        decrypted_hash_int = pow(signature, e, n)
        
        is_valid = (hash_int == decrypted_hash_int)
        
        if is_valid:
            print("Verification Result: VALID - Authentic")
        else:
            print("Verification Result: FAILED - Tampered")
            
        return {
            "hash": msg_hash,
            "is_valid": is_valid
        }
    except Exception as ex:
        print("Verification Result: ERROR")
        return {
            "hash": msg_hash,
            "is_valid": False,
            "error": str(ex)
        }


@app.route("/ala2", methods=["GET"])
def ala2():
    return render_template("ala2.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    # 1. Input Section
    orig_msg = request.form.get("orig_message", "")
    mod_msg = request.form.get("mod_message", "")
    
    orig_bytes = orig_msg.encode()
    mod_bytes = mod_msg.encode()

    # 2. Hash Generation
    orig_sha1 = hashlib.sha1(orig_bytes).hexdigest()
    orig_sha256 = hashlib.sha256(orig_bytes).hexdigest()
    orig_sha512 = hashlib.sha512(orig_bytes).hexdigest()

    mod_sha1 = hashlib.sha1(mod_bytes).hexdigest()
    mod_sha256 = hashlib.sha256(mod_bytes).hexdigest()
    mod_sha512 = hashlib.sha512(mod_bytes).hexdigest()
    
    # 3. Avalanche Effect Analysis (SHA-256 text difference focus)
    diff_chars = 0
    total_chars = len(orig_sha256)
    
    # Compare hex character by character
    for i in range(total_chars):
        if orig_sha256[i] != mod_sha256[i]:
            diff_chars += 1
            
    pct_diff = (diff_chars / total_chars) * 100 if total_chars > 0 else 0
    is_avalanche = diff_chars > 0
    avalanche_result = "YES" if is_avalanche else "NO"

    # 13. Console Output (As requested)
    print("\n--- AVALANCHE EFFECT DEMONSTRATION ---")
    print(f"Original message: {orig_msg}")
    print(f"Modified message: {mod_msg}")
    print(f"SHA-1 hash (orig): {orig_sha1}")
    print(f"SHA-1 hash (mod):  {mod_sha1}")
    print(f"SHA-256 hash (orig): {orig_sha256}")
    print(f"SHA-256 hash (mod):  {mod_sha256}")
    print(f"SHA-512 hash (orig): {orig_sha512}")
    print(f"SHA-512 hash (mod):  {mod_sha512}")
    print(f"Avalanche effect result: {avalanche_result} ({pct_diff:.1f}% mutated)")

    return {
        "original": {
            "message": orig_msg,
            "sha1": orig_sha1,
            "sha256": orig_sha256,
            "sha512": orig_sha512,
            "length": len(orig_bytes)
        },
        "modified": {
            "message": mod_msg,
            "sha1": mod_sha1,
            "sha256": mod_sha256,
            "sha512": mod_sha512,
            "length": len(mod_bytes)
        },
        "avalanche": {
            "diff_chars": diff_chars,
            "total_chars": total_chars,
            "percentage": round(pct_diff, 1),
            "detected": avalanche_result
        }
    }

@app.route("/ala3", methods=["GET"])
def ala3():
    return render_template("ala3.html")

@app.route("/generate_mac", methods=["POST"])
def generate_mac():
    message = request.form.get("message", "")
    secret_key = request.form.get("key", "")
    
    msg_bytes = message.encode()
    key_bytes = secret_key.encode()

    import time
    start_time = time.time()
    
    mac = hmac.new(key_bytes, msg_bytes, hashlib.sha256).hexdigest()
    
    exec_time = (time.time() - start_time) * 1000
    
    print("\n--- MAC GENERATION PROCESS (SENDER SIDE) ---")
    print(f"Original Message: {message}")
    print(f"Secret Key: {secret_key}")
    print(f"HMAC (SHA-256): {mac}")
    
    return {
        "message": message,
        "mac": mac,
        "key_length": len(key_bytes) * 8,
        "mac_length": len(mac) * 4,
        "execution_time_ms": round(exec_time, 2)
    }

@app.route("/verify_mac", methods=["POST"])
def verify_mac():
    secret_key = request.form.get("key", "")
    received_message = request.form.get("message", "")
    received_mac = request.form.get("mac", "")
    
    import time
    start_time = time.time()
    
    recomputed_mac = hmac.new(
        secret_key.encode(),
        received_message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    exec_time = (time.time() - start_time) * 1000
    
    if hmac.compare_digest(received_mac, recomputed_mac):
        result = "✔ MAC Verified — Message Authentic"
        is_valid = True
    else:
        result = "✘ MAC Verification Failed — Message Tampered"
        is_valid = False
    
    print("Received MAC:", received_mac)
    print("Recomputed MAC:", recomputed_mac)
    print("Verification Result:", result)
    
    return {
        "recomputed_mac": recomputed_mac,
        "result": result,
        "is_valid": is_valid,
        "key_length": len(secret_key.encode()) * 8,
        "mac_length": 256,
        "execution_time_ms": round(exec_time, 2)
    }

if __name__ == "__main__":
    app.run(debug=True)
