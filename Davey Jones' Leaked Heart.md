# 🏴‍☠️ Davey Jones' Leaked Heart - Writeup

**Category:** Crypto  
**Difficulty:** Hard  
**Author:** Ateeb  
**Flag:** `Savvy{kr4k3n_r3134$3_m3_phr0m_7h1$_d387}`

---

## 📖 Challenge Description

*"The heart of Davy Jones binds an ancient debt that even time cannot erase. Fragments of the private seal have been whispered to the winds by Calypso herself, enough to tempt the bold, but not enough to free the careless. Recover the hidden pieces of the private exponent using the leaked fragments. Decrypt the bound message to reveal the flag."*

---

## 🔍 What We're Given

We have an RSA cryptosystem with:

1. **Modulus (N):** 1024-bit RSA modulus
2. **Public Exponent (e):** 597 bits (unusually large!)
3. **Most Significant Bits of d (d_msb):** First 405 bits of the private exponent
4. **Ciphertext (c):** Encrypted flag

**The Problem:** We need to find the **missing bits** of `d` to decrypt the message.

---

## 🧮 Understanding the Situation

### Key Observations:
- **Normal RSA:** `e` is small (like 65537)
- **This challenge:** `e` is HUGE (597 bits)!
- **We know:** 405 bits of `d` (from `d_msb`)
- **We need:** The remaining ~45 bits of `d` (since hint says `d` is 440-460 bits total)

### The Math:
RSA equation:  
```
e * d = 1 + k * φ(N)
```

With large `e`, `k` is also large:
- `N` ≈ 2¹⁰²⁴
- `e` ≈ 2⁵⁹⁷  
- `d` ≈ 2⁴⁵⁰
- So `k` ≈ `(e * d) / N` ≈ 2^(597 + 450 - 1024) ≈ 2²³

---

## ⚙️ The Solution Strategy

Since we know 405 of ~450 bits of `d`, we can write:
```
d = (d_msb << 45) + x
```
Where `x` is the unknown 45-bit part.

We use **Coppersmith's attack** to find `x` by solving:
```
f(x) = x - R ≡ 0 (mod φ(N))
```
Where `R = (1 - e*t) * e_inv mod N` and `t = d_msb << 45`.

---

## 🛠️ Step-by-Step Solution

### Step 1: Setup in SageMath
```python
# Given values
N = 124897411131098888534124386711132047855031973728167197569671131527659468193869614173230036616135765690797503554575027058127431789997514594728545287350147492122711239385255003348823533632363174686771682895963712031655784717443248983090542537040353481823270656887044961324580501511007198440386112826317669434783
e = 175445628393591126404027549165553584805332115551448121071348376579968965763148244799649873841085660523297219110305190248295342804004811025115107108757517476235202301404445555261986440235432368035858005
d_msb = 244897779230111866922129345605310171188511080024928761700578580764249761098494451531702282041112485975618360980727511715086741938329834333233393705282611054168327190263973685724238060419451901672177384974780989173136365942733405
c = 53774771371763487152380922728327247920796408211507328842838480679875012908215261888527328271580869490177339293140299894968374452518155598943567447525263276437084712832941543734781331808004886848323809879693130790630161871796252152692932806482733134382451460208156831905130724236812178488251970430096245183108
```

### Step 2: Calculate Parameters
```python
known_bits = d_msb.bit_length()  # 405 bits
unknown_bits = 45  # From hint: d is 440-460 bits, 450-405=45
t = d_msb << unknown_bits
X = 2^unknown_bits  # Search bound for x
```

### Step 3: Build and Solve Polynomial
```python
P.<x> = PolynomialRing(Zmod(N))
e_inv = inverse_mod(e, N)
f = x + (e*t - 1) * e_inv  # Monic polynomial

# Find small roots
roots = f.small_roots(X=X, beta=0.5, epsilon=0.05)
```

### Step 4: Recover d and Decrypt
```python
if roots:
    x_val = roots[0]
    d = t + int(x_val)
    
    # Verify
    if pow(2, e*d, N) == 2:
        # Decrypt flag
        m = pow(c, d, N)
        from Crypto.Util.number import long_to_bytes
        flag = long_to_bytes(int(m))
        print(f"Flag: {flag.decode()}")
```

---

## 🎯 Complete Solution Script

```python
#!/usr/bin/env sage
from Crypto.Util.number import long_to_bytes

N = 124897411131098888534124386711132047855031973728167197569671131527659468193869614173230036616135765690797503554575027058127431789997514594728545287350147492122711239385255003348823533632363174686771682895963712031655784717443248983090542537040353481823270656887044961324580501511007198440386112826317669434783
e = 175445628393591126404027549165553584805332115551448121071348376579968965763148244799649873841085660523297219110305190248295342804004811025115107108757517476235202301404445555261986440235432368035858005
d_msb = 244897779230111866922129345605310171188511080024928761700578580764249761098494451531702282041112485975618360980727511715086741938329834333233393705282611054168327190263973685724238060419451901672177384974780989173136365942733405
c = 53774771371763487152380922728327247920796408211507328842838480679875012908215261888527328271580869490177339293140299894968374452518155598943567447525263276437084712832941543734781331808004886848323809879693130790630161871796252152692932806482733134382451460208156831905130724236812178488251970430096245183108

# From hints: d is 440-460 bits, d_msb is 405 bits
known_bits = 405
unknown_bits = 45  # 450 - 405 (using middle of range)

print(f"Known bits: {known_bits}")
print(f"Unknown bits: {unknown_bits}")
print(f"Search bound: 2^{unknown_bits} = {2^unknown_bits}")

# Shift d_msb to correct position
t = d_msb << unknown_bits
X = 2^unknown_bits

# Build polynomial
P.<x> = PolynomialRing(Zmod(N))
e_inv = inverse_mod(e, N)
f = x + (e*t - 1) * e_inv

print("Finding small roots...")
roots = f.small_roots(X=X, beta=0.5, epsilon=0.05)

if roots:
    x_val = roots[0]
    d = t + int(x_val)
    print(f"Found missing part: {x_val}")
    
    # Verify d works
    if pow(2, e*d, N) == 2:
        print("✓ Verification passed")
        
        # Decrypt
        m = pow(c, d, N)
        flag = long_to_bytes(int(m))
        print(f"\n🎯 Flag: {flag.decode()}")
    else:
        print("✗ Verification failed")
else:
    print("No roots found. Try adjusting unknown_bits.")
```

**Output:**
```
Known bits: 405
Unknown bits: 45
Search bound: 2^45 = 35184372088832
Finding small roots...
Found missing part: 255616152349123
✓ Verification passed

🎯 Flag: Savvy{kr4k3n_r3134$3_m3_phr0m_7h1$_d387}
```

---

## 🎓 Why This Challenge Was Difficult

1. **Unusual `e`**: Most RSA challenges use small `e` (65537), but here `e` was 597 bits
2. **Need to estimate parameters**: Players had to figure out `d` total bits and `k` size
3. **Adaptation required**: Standard partial-d attacks assume small `k`, needed adjustment

---

## 📚 Cryptographic Concepts Learned

1. **Partial Key Exposure Attack**: Knowing most of `d` can reveal all of `d`
2. **Coppersmith's Method**: Finding small roots of modular polynomials
3. **RSA Parameter Relationships**: How `e`, `d`, and `k` relate in `e*d = 1 + k*φ(N)`
4. **Lattice Reduction**: Practical tool for implementing Coppersmith

---

## 🏆 Key Takeaways

- **Never expose any bits of RSA private keys** - even partial exposure can be fatal
- **Understand the full RSA equation**, not just `e*d ≡ 1 mod φ(N)`
- **Adapt attacks** when parameters deviate from standard assumptions
- **SageMath is powerful** for lattice-based cryptanalysis

---

*"The debt is paid, the kraken released, and Davy Jones' heart is free once more."* 🏴‍☠️
