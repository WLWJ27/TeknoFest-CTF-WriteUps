
# Challenge Writeup: Black Pearl Printer

**Author:** Rabia Ishtiaq  
**Category:** Hardware / Forensics  

---

## Description

A network printer recovered from The Fray’s environment appears ordinary at first glance—routine logs, standard configurations, and years of operational noise. However, activity during a restricted maintenance window suggests something was generated and deliberately secured.

Explore the filesystem, correlate artifacts, and identify what was left behind. Not everything important announces itself, and not every document is meant to be opened without the right key.

**Flag Format:**  
`Savvy{...}`

---

## Investigation & Analysis

### 1. Exploring the Printer Filesystem

Players are provided with an archive named:

```

printer_fs.zip

```

After extracting the archive and recursively browsing the filesystem, a suspicious document is discovered at the following path:

```

printer_fs/printer_fs/usr/share/docs/service_log.pdf

```

Attempting to open `service_log.pdf` reveals that the file is **password-protected**, indicating that the document was intentionally secured.

---

### 2. Analyzing Logs for Clues

Given the challenge context, the next logical step is to inspect the available log files. Inside the filesystem, a log file named `system.log` contains entries related to maintenance activity.

One log entry stands out:

```

[2024-03-14 11:06:18] DEBUG: Maintenance token: 7nG36dM4ra4UXNf1W4E

```

The term **“Maintenance token”** combined with a seemingly encoded string strongly suggests that this value is not random noise, but a key piece of evidence.

---

### 3. Decoding the Maintenance Token

The token:

```

7nG36dM4ra4UXNf1W4E

```

appears to be Base64-encoded. Decoding it using a Base64 decoder reveals the following result:

```

FlyingDutchman

```

This decoded string matches the expected format of a password.

---

### 4. Unlocking the Secured Document

Using the decoded password:

```

FlyingDutchman

```

the `service_log.pdf` file can now be successfully opened.

Inside the PDF, the hidden message is revealed, containing the flag.

---

## Flag

```

Savvy{h1dd3n_l1k3_c4p741n5_l007}

```

---

## Key Takeaways

- Hardware and printer challenges often hide data in **unexpected filesystem paths**.
- Log files can contain **encoded secrets**, not just operational data.
- Recognizing common encodings like **Base64** is critical in forensic analysis.
- Not all artifacts are meant to be accessed directly—correlation is key.

🏴‍☠️ *Like a true pirate’s treasure, the prize was hidden in plain sight, guarded by a cipher and revealed only to those who knew where to look.*
