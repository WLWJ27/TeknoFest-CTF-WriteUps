MAP NO MAN CAN READ

Category

REVERSE



Difficulty

Medium



Creator

ABDUL WASAY KHAN



**Challenge Description**

YOU HOLD THE DIARY OF GALILEO, A MAP THAT NO MAN CAN READ. MOST WOULD LOOK AT THE INK ON THE PAGE AND CLAIM THEY’VE FOUND THE TREASURE, BUT A TRUE WOMAN OF SCIENCE KNOWS THAT THE SURFACE IS MERELY AN ILLUSION.



Solution Walkthrough

Step 1: Download the Calypso's Fury Zip file.



Step 2: Extract the contents; you will get access to five different files.



Step 3: Execute the \_packaged\_startup file. You will be asked to enter a PIN code and a phrase (WHY IS THE RUM GONE) to decrypt/find the PIN.



Step 4: The PIN can be solved by counting the letters of each word in the phrase: 32334.



Step 5: However, the PIN does not work to find the flag. Inspect the Python file included in the zip. You will notice around 1000 fake flags and a "real" flag written in plaintext within the code—these are all red herrings (fakes).



Step 6: The true flag is hidden in ciphered text within the hashlib file as {F im m Hvffzzuoal}.



Step 7: Decrypting this text yields the final correct flag.



FLAG: Savvy{I am a horologist}



Key Takeaways



Look beyond the executable: Interactive prompts (like the PIN code) can often be distractions or rabbit holes.



Inspect all files: Standard-looking library files (like hashlib) can be modified to hide data. Always verify that imported modules are legitimate.



Beware of Red Herrings: Large amounts of plaintext "flags" are usually fake. If it looks too easy to find in the code, it's likely a trap.



Crypto awareness: Keep an eye out for odd string patterns that look like substitution ciphers.

