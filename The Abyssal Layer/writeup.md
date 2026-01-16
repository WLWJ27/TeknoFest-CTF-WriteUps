# The Abyssal Layers

## Category

Misc

## Difficulty

Hard

## Creator

Hafsah Anwaar Ali

---

## Challenge Description

Once a wise man said curiosity kills the cat. Be cautious, because you will become a curious cat while solving this challenge.

> "Master Turner, you'll find that this map is like a Vidalia onion from the East Indies—it has many skins, and the deeper you peel, the more it'll make your eyes water.
> Beneath the ink, beneath the parchment, and beneath the sea itself lies the flag of the Brethren Court."

This challenge required peeling multiple layers of clues hidden across images, metadata, riddles, and steganography.

---

## Provided Files

* `Dead_man_tell_no_tales.jpg`

---

## Objective

Uncover the hidden flag by following layered clues involving strings extraction, steganography, riddles, metadata analysis, and encoded links.

Flag format: `Savvy{}`

---

## Solution Walkthrough

### Step 1: Strings Analysis

We start by downloading the provided image and extracting readable strings from it:

```bash
strings Dead_man_tell_no_tales.jpg
```

This reveals a hidden link, which serves as the next clue.

---

### Step 2: Steganography with Zsteg

Visiting the link leads to another image file: `low_sea_bits.png`.

We analyze it using `zsteg`:

```bash
zsteg low_sea_bits.png
```

This reveals the following encoded string:

```
aHR0cHM6Ly9kcml2ZS5nb29nbGUuY29tL2ZpbGUvZC8xdXRKdnpKa0s5UVNUY2ZhcHVaTUNvOUt4M3FvenBRVmIvdmlldz91c3A9c2hhcmluZw==
```

Decoding this Base64 string gives us another Google Drive link.

---

### Step 3: Riddle & Password Discovery

The decoded link contains a file named `log_fragment.txt`, which includes a riddle:

> They were not made of gold, but of pocket lint, old corks, and silver trinkets—yet history remembers them by a singular, deceptive name.

The answer to this riddle is:

```
piecesofeight
```

* **All lowercase, no spaces**
* This serves as the password for the next layer.

---

### Step 4: Steghide Extraction

Using the password, we download `locked_locker.jpg` and extract its hidden contents:

```bash
steghide extract -sf locked_locker.jpg
```

This provides another clue containing a link.

---

### Step 5: Metadata Analysis (Exiftool)

The final link leads to the image `trust_meta_its_the_last.jpg`.
We inspect its metadata using:

```bash
exiftool trust_meta_its_the_last.jpg
```

Inside the **Comment field** of the metadata, the flag is revealed.

---

### Flag

```
Savvy{701d_y0u_kwr10$17y_k111$_7h3_c47}
```

---

### Key Takeaways

* Multi-layered challenges require **patience** and **structured analysis**.
* **Metadata** can be just as important as file contents.
* Steganography tools like `zsteg` and `steghide` are powerful when combined.
* Riddles often hint at **passwords indirectly**.
* Always think **meta** when solving MISC challenges.
