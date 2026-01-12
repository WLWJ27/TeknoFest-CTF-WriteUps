# 🏴‍☠️ Parley Under Weak Sails - Writeup

**Category:** Crypto  
**Difficulty:** Medium  
**Author:** Ateeb  
**Flag:** `Savvy{7h3_C0d3_1$_m0r3_wh47_y0ud_c411_gu1d311n3$_7h4n_4c7u41_ru13$_4rrr}`

---

## 📖 Challenge Description

*"Arrr, ye scurvy dog! A man-in-the-middle eavesdropper intercepted a key exchange between two pirates sharing a secret message about the Pirate's Code. The exchange was done with weak 'export-grade' parameters, making it vulnerable to attack."*

---

## 🔍 Understanding the Setup

This is a **classic Diffie-Hellman key exchange** with **dangerously small parameters**:

```
p (modulus) = 1000003    ← ONLY 1 million! (Tiny!)
g (generator) = 2
A (Alice's public key) = 497566
B (Bob's public key) = 44459
```

**How DH normally works:**
1. Alice picks secret `a`, sends `A = g^a mod p`
2. Bob picks secret `b`, sends `B = g^b mod p`  
3. Shared secret = `S = B^a mod p = A^b mod p`

**The problem:** `p` is so small we can **brute force** the secret exponents!

---

## 🚨 The Vulnerability

In 1990s, the U.S. government restricted "export-grade" crypto to use **small primes** (like 512 bits).  
This made it easy for attackers to break the encryption.

Here, `p = 1,000,003` (about 20 bits) is **ridiculously small** - we can try every possible exponent!

---

## ⚡ Solution (3 Methods)

### **Method 1: Brute Force (Simplest)**
```python
p = 1000003
g = 2
A = 497566
B = 44459

# Find Alice's secret 'a' (takes < 1 second!)
for a in range(1, p):
    if pow(g, a, p) == A:
        break

# Or find Bob's secret 'b'
for b in range(1, p):
    if pow(g, b, p) == B:
        break

# Calculate shared secret
S = pow(B, a, p)  # Should equal pow(A, b, p)
print(f"Shared secret S = {S}")  # 770016
```

### **Method 2: Baby-Step Giant-Step (Educational)**
This is faster than brute force for larger primes:
```python
from math import isqrt

def baby_step_giant_step(g, h, p):
    """Solve g^x ≡ h (mod p)"""
    n = isqrt(p) + 1
    baby_steps = {pow(g, i, p): i for i in range(n)}
    
    g_inv_n = pow(pow(g, n, p), -1, p)
    giant = h
    
    for j in range(n):
        if giant in baby_steps:
            return j * n + baby_steps[giant]
        giant = (giant * g_inv_n) % p
    return None

a = baby_step_giant_step(g, A, p)  # 486352
```

### **Method 3: Using SageMath (One-liner)**
```python
a = discrete_log(mod(A, p), mod(g, p))  # 486352
```

---

## 🔓 Decrypting the Message

Once we have `S = 770016`:

### Step 1: Generate keystream
The encryption is **XOR with repeating bytes of `str(S)`**:
```python
S = 770016
keystream_bytes = str(S).encode()  # b'770016'
# This repeats: 770016770016770016...
```

### Step 2: XOR with ciphertext
```python
cipher_hex = "6b50444041420f5901697b095c026d071c6655014005674e5005056941094d556d550c08096e5543095d0b0003580b1d67065a0256660c5205430c08674347070b1d670540444a44"
cipher_bytes = bytes.fromhex(cipher_hex)

# Generate enough keystream
keystream = (keystream_bytes * (len(cipher_bytes) // 6 + 2))[:len(cipher_bytes)]

# XOR decrypt
flag_bytes = bytes(c ^ k for c, k in zip(cipher_bytes, keystream))
print(flag_bytes.decode())
```

---

## 🎯 Complete Solve Script
```python
# === DIFFIE-HELLMAN BREAK ===
p = 1000003
g = 2
A = 497566
B = 44459

# Brute force Alice's secret (takes < 1 second)
for a in range(1, p):
    if pow(g, a, p) == A:
        break

# Calculate shared secret
S = pow(B, a, p)  # = 770016
print(f"Shared secret: {S}")

# === DECRYPTION ===
cipher = bytes.fromhex("6b50444041420f5901697b095c026d071c6655014005674e5005056941094d556d550c08096e5543095d0b0003580b1d67065a0256660c5205430c08674347070b1d670540444a44")

# Generate repeating keystream "770016770016..."
keystream = (str(S).encode() * (len(cipher)//6 + 2))[:len(cipher)]

# XOR decrypt
flag = bytes(c ^ k for c, k in zip(cipher, keystream))
print(f"Flag: {flag.decode()}")
```

**Output:**
```
Shared secret: 770016
Flag: Savvy{7h3_C0d3_1$_m0r3_wh47_y0ud_c411_gu1d311n3$_7h4n_4c7u41_ru13$_4rrr}
```

---

## 🎓 What We Learned

### **Security Lessons:**
1. **Never use small primes** in Diffie-Hellman
2. **"Export-grade" crypto** is intentionally weak
3. **Discrete logarithm** becomes easy when `p` is small

### **Technical Takeaways:**
- `p` should be **at least 2048 bits** for security
- Always use **safe primes** (`(p-1)/2` should also be prime)
- Brute force works up to ~2²⁰ operations (1 million)

---

## 📊 Why This Was "Medium" Difficulty

**Easy parts:**
- Straightforward brute force works
- Simple XOR encryption
- No fancy math required

**Medium parts:**
- Need to understand Diffie-Hellman
- Need to implement discrete log attack
- Need to handle repeating keystream

---

## 🏴‍☠️ Final Thoughts

This challenge demonstrates **real historical vulnerability** - the 1990s "export-grade" crypto restrictions actually allowed attackers to break encryption easily. Always use strong parameters!

**Flag:** `Savvy{7h3_C0d3_1$_m0r3_wh47_y0ud_c411_gu1d311n3$_7h4n_4c7u41_ru13$_4rrr}`

*"The code is more what you'd call 'guidelines' than actual rules... but this cipher be truly broken. Savvy?"* 🏴‍☠️

---
