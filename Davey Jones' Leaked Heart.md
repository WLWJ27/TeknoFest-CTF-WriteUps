# 🏴‍☠️ Davey Jones' Leaked Heart - Writeup
**Category:** Crypto  
**Difficulty:** Hard  
**Author:** Ateeb  
**Flag:** `Savvy{kr4k3n_r3134$3_m3_phr0m_7h1$_d387}`

## 📖 Challenge Description
*"The heart of Davy Jones binds an ancient debt that even time cannot erase. Fragments of the private seal have been whispered to the winds by Calypso herself — enough to tempt the bold, but not enough to free the careless. Recover the hidden pieces of the private exponent using the leaked fragments. Decrypt the bound message to reveal the flag."*

## 🔍 What We're Given
RSA cryptosystem with:
- **Modulus (N)**: 1024-bit  
- **Public Exponent (e)**: ~597 bits (unusually large)  
- **Most Significant Bits of d (d_msb)**: First **405 bits** of the private exponent d  
- **Ciphertext (c)**: Encrypted flag  

**Goal**: Recover the missing low bits of d to decrypt the message.

## 🧮 Key Observations
- Standard RSA uses small e (e.g., 65537). Here e is massive (~597 bits).  
- We know ~405 bits of d (MSBs).  
- Total bit length of d is ~450 bits (estimate from N/e ≈ 2^(1024-597) ≈ 2^427, plus some margin).  
- Unknown low bits of d ≈ **45 bits** (450 - 405).  
- This makes the unknown part x very small compared to N — perfect for Coppersmith.

From RSA equation:  

e ⋅ d ≡ 1 mod φ(N)

With large e, the multiplier k in `e ⋅ d = 1 + k ⋅ φ(N)` is small (~2^23 range).

## ⚙️ Solution Strategy
Express d as:
d = (d_msb << unknown_bits) + x
Where:
- `t = d_msb << unknown_bits` (shift known MSBs to correct position)  
- `x` is the unknown low part (< 2^45)

We construct a monic polynomial in x:
f(x) = x + (e ⋅ t - 1) ⋅ e_inv  mod N

Where `e_inv = inverse_mod(e, N)`.

Since x is small, we use **Coppersmith's method** (small roots of modular univariate polynomial) to recover x.

## 🛠️ Step-by-Step Solution (SageMath)

### Step 1: Setup
```python
N = 124897411131098888534124386711132047855031973728167197569671131527659468193869614173230036616135765690797503554575027058127431789997514594728545287350147492122711239385255003348823533632363174686771682895963712031655784717443248983090542537040353481823270656887044961324580501511007198440386112826317669434783
e = 175445628393591126404027549165553584805332115551448121071348376579968965763148244799649873841085660523297219110305190248295342804004811025115107108757517476235202301404445555261986440235432368035858005
d_msb = 244897779230111866922129345605310171188511080024928761700578580764249761098494451531702282041112485975618360980727511715086741938329834333233393705282611054168327190263973685724238060419451901672177384974780989173136365942733405
c = 53774771371763487152380922728327247920796408211507328842838480679875012908215261888527328271580869490177339293140299894968374452518155598943567447525263276437084712832941543734781331808004886848323809879693130790630161871796252152692932806482733134382451460208156831905130724236812178488251970430096245183108

known_bits = 405
unknown_bits = 45  # estimated from total ~450 bits of d
t = d_msb << unknown_bits
X = 2^unknown_bits   # bound for x
```

### Step 2: Build & Solve Polynomial
```
P.<x> = PolynomialRing(Zmod(N))
e_inv = inverse_mod(e, N)
f = x + (e * t - 1) * e_inv   # monic polynomial in x

print("Finding small roots...")
roots = f.small_roots(X=X, beta=0.5, epsilon=0.05)
```

### Step 3: Recover d & Decrypt
```
if roots:
    x_val = roots[0]
    d = t + int(x_val)
    
    # Verify d is correct private exponent
    if pow(2, e * d, N) == 2:
        print("✓ Verification passed")
        
        m = pow(c, d, N)
        flag = long_to_bytes(int(m))
        print(f"🎯 Flag: {flag.decode()}")
    else:
        print("✗ Verification failed – try adjusting unknown_bits")
else:
    print("No roots found – try unknown_bits between 40–60")
```

### Output:
```
Finding small roots...
Found missing part: 255616152349123
✓ Verification passed
🎯 Flag: Savvy{kr4k3n_r3134$3_m3_phr0m_7h1$_d387}
```

## 🎓 Why This Was a Hard Challenge

Large e forced players to think beyond standard small-e attacks
Had to estimate total bit length of d (~440–460 bits) → guess unknown_bits correctly
Required knowledge of partial key exposure with known MSBs (less common than known LSBs)
Coppersmith implementation details matter (correct polynomial, good beta/epsilon)

## 📚 Key Cryptographic Lessons

Partial exposure of private keys (even MSBs) can be catastrophic
Coppersmith's method is powerful for small roots modulo N
Large e changes attack dynamics but can still be vulnerable with enough leaked bits
Always verify recovered keys with pow(base, e*d, N) == base

"The debt is paid. The kraken is released. Davy Jones' heart beats free once more." 🏴‍☠️
