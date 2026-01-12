
# Nothing Is Ever Just One Layer — Writeup

**Author:** Rabia Ishtiaq

---

## 📌 Challenge Summary
In this challenge, players are provided with an image that appears completely empty. However, as the title suggests, **the image is not what it seems**. The challenge is designed to teach players that secrets in forensics and steganography often exist in **layers**, and solving one layer unlocks the next.

---

## 🧠 Intended Logic (For Players)

The goal is to make players:
- Trust the hint given in the description
- Use automated forensic tools when nothing is visually obvious
- Recognize encoded data and decode it correctly
- Use the decoded output as a key for further extraction

Each step naturally leads to the next, rewarding logical thinking rather than guessing.

---

## 🔍 Step 1: Visual Inspection
Opening the image normally reveals:
- No visible text
- No suspicious artifacts
- No obvious hints

This indicates that the secret is **not in plain sight**, pushing players toward steganographic analysis.

---

## 🧪 Step 2: Steganography Scan with AperiSolve
Players are expected to upload the image to:

🔗 https://aperisolve.fr/

AperiSolve performs multiple automated checks (LSB, strings, bit planes, etc.).

### 🔎 Discovery:
A hidden encoded string is revealed:

```

9cvZhUap*

```

This confirms the image contains **hidden data** and that further decoding is required.

---

## 🔐 Step 3: Identifying and Decoding Base92
The extracted string does not match common encodings like Base64 or Base32. With trial and reasoning, players identify it as **Base92 encoding**.

After decoding:

```

9cvZhUap* → Conquer

````

### 🧠 Logic:
In CTFs, decoded words often act as:
- Passwords
- Passphrases
- Keys for the next step

So “Conquer” is not the flag, but a **tool**.

---

## 🗝️ Step 4: Extracting Hidden Data with Steghide
Given that the file is an image and a passphrase has been found, players attempt extraction using `steghide`.

```bash
steghide extract -sf Image.bmp
````

When prompted for a passphrase, enter:

```
Conquer
```

Steghide successfully extracts the hidden content.

---

## 🏴 Final Flag

The extracted data reveals the flag:

```
Savvy{d34d_m3n_7311_n0_7413$}
```

---

## 🎯 Key Takeaways

* Not all images reveal secrets visually
* Automated tools can expose hidden layers
* Encoded strings often act as keys, not answers
* Logical progression is more important than brute force

This challenge emphasizes a core CTF principle:

> **If something looks empty, it probably isn’t.**

Happy hacking! 🏴‍☠️
