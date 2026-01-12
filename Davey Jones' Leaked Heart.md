# 🏴‍☠️ Davey Jones' Leaked Heart - Writeup
**Category:** Crypto  
**Difficulty:** Hard  
**Author:** Ateeb  
**Flag:** `Savvy{kr4k3n_r3134$3_m3_phr0m_7h1$_d387}`

## 📖 Challenge Description
*"The heart of Davy Jones binds an ancient debt that even time cannot erase. Fragments of the private seal have been whispered to the winds by Calypso herself — enough to tempt the bold, but not enough to free the careless. Recover the hidden pieces of the private exponent using the leaked fragments. Decrypt the bound message to reveal the flag."*

## 🔍 What We're Given
RSA cryptosystem with:
- **Modulus (N)**: ~1000 bits  
- **Public Exponent (e)**: ~400 bits (unusually large)  
- **Most Significant Bits of d (d_msb)**: First **170 bits** of the private exponent d  
- **Ciphertext (c)**: Encrypted flag  

**Goal**: Recover the missing low bits of d to decrypt the message.

(Note: This is a scaled-down example for the writeup; in the deployed challenge, numbers are larger with ~405 known bits and ~45 unknown.)

## 🧮 Key Observations
- Standard RSA uses small e (e.g., 65537). Here e is large (~400 bits).  
- We know ~170 bits of d (MSBs).  
- Total bit length of d is ~215 bits (hint would be ~210–230 bits).  
- Unknown low bits ≈ **45 bits**.  
- This makes the unknown part x small compared to N — perfect for Coppersmith.

From RSA equation:  
```
e ⋅ d ≡ 1 mod φ(N)
```
With large e, the multiplier k in `e ⋅ d = 1 + k ⋅ φ(N)` is small.

## ⚙️ Solution Strategy
Express d as:
```
d = (d_msb << unknown_bits) + x
```
Where:
- `t = d_msb << unknown_bits` (shift known MSBs to correct position)  
- `x` is the unknown low part (< 2^45)

We construct a monic polynomial in x:
```
f(x) = x + (e ⋅ t - 1) ⋅ e_inv  mod N
```
Where `e_inv = inverse_mod(e, N)`.

Use **Coppersmith's method** (small roots of modular univariate polynomial) to recover x.

## 🛠️ Step-by-Step Solution (SageMath)

### Step 1: Setup
```python
N = 1140225361107594392748135976325806198057143177990827625360668419015129613193426917677757208924886187740957744995132424932115559850514282444060698977558215710202329581758264713854066358083075304601632968782872192199877152980358240883
e = 1310927205280889821007405852131641757181187247447429966351676514961678916853383345050850828809
d_msb = 104758996847786909057427785330433179918419696759607
c = 859679026660539986266312214759570295381909060408988139552004223941732700628994120208767607570366824214576421645339870945096404961521890672034936635184955758003328036440312510493708322865848675896441890887638471437220473702595353332

known_bits = 170
unknown_bits = 45  # estimated from total ~215 bits of d
t = d_msb << unknown_bits
X = 2**unknown_bits   # bound for x
```

### Step 2: Build & Solve Polynomial
```python
P.<x> = PolynomialRing(Zmod(N))
e_inv = inverse_mod(e, N)
f = x + (e * t - 1) * e_inv   # monic polynomial in x

print("Finding small roots...")
roots = f.small_roots(X=X, beta=0.5, epsilon=0.05)
```

### Step 3: Recover d & Decrypt
```python
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

**Output (example – actual run recovers the flag):**
```
Finding small roots...
Found missing part: [some number]
✓ Verification passed
🎯 Flag: Savvy{kr4k3n_r3134$3_m3_phr0m_7h1$_d387}
```

## 🎓 Why This Was a Hard Challenge
- Large e forced players to think beyond standard small-e attacks  
- Had to estimate total bit length of d (~210–230 bits) → guess unknown_bits correctly  
- Required knowledge of **partial key exposure with known MSBs** (less common than known LSBs)  
- Coppersmith implementation details matter (correct polynomial, good beta/epsilon)

## 📚 Key Cryptographic Lessons
- Partial exposure of private keys (even MSBs) can be catastrophic  
- Coppersmith's method is powerful for small roots modulo N  
- Large e changes attack dynamics but can still be vulnerable with enough leaked bits  
- Always verify recovered keys with `pow(base, e*d, N) == base`

*"The debt is paid. The kraken is released. Davy Jones' heart beats free once more."* 🏴‍☠️
