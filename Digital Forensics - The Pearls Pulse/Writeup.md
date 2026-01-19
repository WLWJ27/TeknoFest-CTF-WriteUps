# 🏴‍☠️ The Pearls Pulse

**Challenge Author: Aman Shahid**

## 🧠 Challenge Overview

This challenge hides a flag inside **ICMP Echo Request timings**.  
Rather than embedding data in packet payloads, the sender leaks information using **time delays between packets**, forming a **covert timing channel**.

Participants are given a CSV export of ICMP traffic and must recover the flag by analyzing **inter-packet timing patterns**.

---

## 🎯 Objective

Extract and decode the hidden flag from ICMP ping timestamps.


---

## 📁 Provided Artifact

- `icmp-5.csv`
  - Exported from Wireshark
  - Contains ICMP Echo Requests with timestamps
  - Relevant field: `Time`

---

## 🔍 Key Observation

Examining the `Time` column reveals two dominant timing values:

| Timing (seconds) | Meaning |
|------------------|---------|
| ~1.0s            | Binary `0` |
| ~2.0s            | Binary `1` |

This suggests a **binary encoding using time delays**:

- **Short delay (< 1.5s)** → `0`
- **Long delay (≥ 1.5s)** → `1`

Each ICMP packet represents **one bit**.

---

## 🧩 Decoding Strategy

1. Parse the CSV file
2. Convert each timestamp into a binary bit
3. Concatenate all bits into a bitstream
4. Group bits into bytes (8 bits)
5. Convert each byte into ASCII characters
6. Handle incomplete final byte correctly

---

## ⚠️ Important Pitfall

The total number of bits recovered is **not a multiple of 8**.

If the final byte is padded incorrectly, the decoded output produces:

- Garbled characters
- Wrong closing braces
- Incorrect ASCII symbols

### ✅ Correct Fix

The last partial byte must be **left-padded** with zeros (MSB-first encoding).

---

## 🛠️ Decoder Script

```python
import csv

CSV_FILE = "icmp-5.csv"
THRESHOLD = 1.5  # seconds

def time_to_bit(time_str):
    try:
        t = float(time_str)
        return '0' if t < THRESHOLD else '1'
    except:
        return None

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            byte = byte.rjust(8, '0')  # MSB padding
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def main():
    bits = ""

    with open(CSV_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bit = time_to_bit(row["Time"])
            if bit is not None:
                bits += bit

    print(f"[*] Bits recovered: {len(bits)}")
    decoded = bits_to_text(bits)
    print(f"Decoded flag: {decoded}")

if __name__ == "__main__":
    main()
```