The Caribbean Mystery - Writeup

Category: Cryptography | Difficulty: Hard | Author: Ammara

Challenge Overview
Description:
The Pirate Lords use "The Brethren Code" cipher, but a careless pirate reused the same secret key to encrypt multiple messages. We have two intercepted ciphertexts:
C1 = 33000d070d080046100a41100a004505161c11100d45060e05090d010c020047
C2 = 370417121b1e1d09163a0a011b3a17031116043b0b163a00051100081f
Hint: One message is written in plain English (a common greeting). The other contains the flag.
Flag Format: Savvy{...}

Understanding XOR Key Reuse
This challenge exploits the XOR key reuse vulnerability. When the same key encrypts multiple messages:

C1 = P1 ⊕ Key
C2 = P2 ⊕ Key

XORing the ciphertexts eliminates the key:
C1 ⊕ C2 = P1 ⊕ P2

Solution
Step 1: XOR the Ciphertexts
pythonC1 = bytes.fromhex('33000d070d080046100a41100a004505161c11100d45060e05090d010c020047')
C2 = bytes.fromhex('370417121b1e1d09163a0a011b3a17031116043b0b163a00051100081f')

# XOR C1 and C2
xor_result = bytes(a ^ b for a, b in zip(C1, C2))
print(xor_result.hex())
Result: 04041a151616154f063b4b113b52060a001d350b063b060b001d011b14
Step 2: Known Plaintext Attack
The hint tells us one message is a "common greeting" in plain English. Let's try common phrases:

"Hello"
"Welcome"
"Greetings"

Since C1 ⊕ C2 = P1 ⊕ P2, if we know P1, we can recover P2:
python# Try "Welcome to the crypto challenge!" as P1
P1 = b"Welcome to the crypto challenge!"

# Recover P2 by XORing with our result
P2 = bytes(a ^ b for a, b in zip(xor_result, P1))
print(P2.decode())
```

**Output:**
```
Savvy{xor_key_reuse_is_fatal}
Step 3: Verify the Solution
We can verify by recovering the key and decrypting both messages:
python# Recover the key using C1 and P1
key = bytes(a ^ b for a, b in zip(C1[:len(P1)], P1))
print(f"Key (hex): {key.hex()}")  # deadbeef (repeated)

# Decrypt C2 to verify
P2_verify = bytes(a ^ b for a, b in zip(C2, key[:len(C2)]))
print(P2_verify.decode())  # Savvy{xor_key_reuse_is_fatal}

Complete Solution Script
pythonC1 = bytes.fromhex('33000d070d080046100a41100a004505161c11100d45060e05090d010c020047')
C2 = bytes.fromhex('370417121b1e1d09163a0a011b3a17031116043b0b163a00051100081f')

# XOR the two ciphertexts
xor_result = bytes(a ^ b for a, b in zip(C1, C2))

# Known plaintext (the greeting)
P1 = b"Welcome to the crypto challenge!"

# Recover P2 (the flag)
P2 = bytes(a ^ b for a, b in zip(xor_result, P1))
print(P2.decode())
```

---

## Flag
```
Savvy{xor_key_reuse_is_fatal}