
---

# 🏴‍☠️ Isla de Muerta – Pirate’s Secret

**Category:** Steganography
**Difficulty:** Medium
**Flag:** `Savvy{C0R4L_TRE4SURE_M4P}`

---

## Challenge Description

> “Ahoy matey! Legends say the cursed treasure of Isla de Muerta was hidden in plain sight.
> What looks like a simple map is more than it seems… the colors hold a secret.
> Only the savviest pirates can decode the hidden message.
> Examine the marks carefully, follow the path of the island, and claim the treasure.
> Flag format: Savvy{}”

Participants were provided with an image of a small pirate map. At first glance, it appeared **ordinary**, with no visible text, no distortions, and no metadata hints. The challenge was designed as a **steganography problem**, where the secret was encoded within the pixel colors.

---

## Solution Approach

Even without explicit hints, careful observation of the image suggests the secret might be **hidden at the pixel level**, given the description mentions “colors hold a secret.”

1. **Load the image and examine the pixel values**
   The image was small (19×19), suggesting each pixel could encode a single character.

2. **Recover the hidden message**
   By analyzing the pixel RGB values and applying an XOR operation with the key used to encode them (`0x55`), the original characters can be reconstructed.

3. **Follow the zigzag pattern**
   Each row of the image was encoded in alternating directions:

   * Even rows: left → right
   * Odd rows: right → left
     Correctly following this pattern reveals the message in the right order.

---

## Solution Code

```python
from PIL import Image
import numpy as np

WIDTH, HEIGHT = 19, 19
KEY = 0x55

# Open the image
img = Image.open("isla_de_muerta_clean.png").convert("RGB")
pixels = np.array(img)

message = ""
for y in range(HEIGHT):
    row = pixels[y]
    if y % 2 == 1:
        row = row[::-1]  # zigzag: reverse every odd row
    for pixel in row:
        val = int(pixel[0]) + int(pixel[1]) + int(pixel[2])  # sum RGB values
        char = chr(val ^ KEY)  # XOR with key to recover original character
        message += char

print("Recovered message:\n", message)
```

---

## Recovered Message

```
Ahoy matey! Treasure map hidden. Flag: Savvy{C0R4L_TRE4SURE_M4P}
```

✅ **Flag:** `Savvy{C0R4L_TRE4SURE_M4P}`

---

## Notes

* The secret was hidden **in plain sight**, encoded using pixel colors.
* XORing with a key and following the correct traversal order were required to fully decode the message.
* No explicit hints were provided about RGB sums or zigzag order — participants had to **analyze the image and experiment logically**.

---
