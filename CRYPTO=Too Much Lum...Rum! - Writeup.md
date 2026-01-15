Too Much Lum...Rum! - Writeup

Challenge: Too Much Lum...Rum!
Category: Cryptography
Difficulty: Medium
Author: Ammara

Challenge Description
We're presented with a cryptic ciphertext recovered from a pirate wreck:
epcndkohllkwwfkzcllkoclivdckskvpkddcyoceipkvrcslkdhycbcscwcsc
Along with the clue:

"A pirate never follows the king's order — he writes like a scholar."

The flag format is Savvy{...}

Initial Analysis
The challenge title "Too Much Lum...Rum!" is our first major hint. Notice the play on words:

Lum → Rum
The letter L is replaced with R

This suggests that letters might be swapped or shifted in some way.
The clue about "the king's order" refers to QWERTY keyboard layout (the standard), while "writes like a scholar" hints at the alphabetical order (ABCDEF...).

Solution Steps

Step 1: Identify the Cipher
The clue points us toward a Keyboard Shift Cipher, where letters are mapped from alphabetical order to QWERTY keyboard layout.
Using a cipher identification tool like dCode.fr, we can test various ciphers. The Keyboard Change Cipher stands out as the most likely candidate.
Step 2: Decode with QWERTY Mapping
Decoding the ciphertext using ABC...Z → QWERTY mapping gives us:
theflagissavvyamessagesocrealacharrengetohackelsarinewelevele
Adding spaces back (since they were removed):
the flag is savvy a message so creal a charrenge to hackels a rine we levele
Step 3: The Rum Twist
Notice the garbled words:

frag → should be flag
creal → should be clear
charrenge → should be challenge
hackels → should be hackers
rine → should be line
levele → should be revere

The pattern? L and R are swapped! This ties back to the challenge title: "Too Much Lum...Rum!" — the pirate was too drunk and mixed up their L's and R's!
Step 4: Swap L ↔ R
Performing the letter swap:
the flag is savvy a message so clear a challenge to hackers a line we revere

Flag
Savvy{a message so clear a challenge to hackers a line we revere}