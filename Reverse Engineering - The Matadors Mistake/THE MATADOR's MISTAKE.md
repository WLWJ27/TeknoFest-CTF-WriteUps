THE MATADOR's MISTAKE



Category

REVERSE



Difficulty

Medium



Creator

ABDUL WASAY KHAN



Challenge Description

I’VE GOT A JAR OF DIRT! I’VE GOT A JAR OF DIRT! AND GUESS WHAT’S INSIDE IT?



**Challenge Explanation**

The challenge provides a Linux shell script (a Makeself archive) that performs an integrity check before execution. Upon running the file, it fails to verify because the MD5 hash is incomplete, preventing the user from accessing the internal payload and the flag.



**Solution Walkthrough**

Step 1: Analyze the Script Header

Upon inspecting the challenge (1).sh file, you will notice it is a Makeself 2.5.0 archive. The script contains a section for checksums used to verify the file's integrity before extraction:



CRCsum="59052631"

MD5="..0685898551dca1e8399f60678e2038"



Step 2: Identify the Integrity Failure

When you execute the file, the system attempts to match the MD5 hash. However, the process fails because the first two characters (bits) of the MD5 hash are missing, represented as ...



Step 3: Bypassing the Corruption

Simply editing the file in a standard text editor or Ghidra to fix the hash might corrupt the binary offset of the archive, causing it to fail again. To fix this properly, you must replace the placeholders manually without shifting the file structure.



Step 4: Patching the Hash

Replace the .. in the MD5 string with the correct hex value: 7f.



The corrected line should look like this:



MD5="7f0685898551dca1e8399f60678e2038"



Step 5: Execute and Retrieve Flag

Once the integrity check matches, the script will successfully extract and run the internal startup script, revealing the final flag.



Flag

Savvy{3a50c5e41a1c3eee6dcddca9e04992e0}



Key Takeaways

Makeself Archives: Understanding that .sh files can be self-extracting archives is crucial. They often rely on hardcoded checksums in the header.



Hex/Text Editing Sensitivity: When dealing with self-extracting scripts, even a single byte shift in the text portion can lead to "Offset" errors or file corruption.



Integrity Checks: Checksums like MD5 and CRC are used to ensure the payload hasn't been tampered with; finding the missing "bits" of these hashes is a common reversing technique.





**PRO TIP:**

**You can solve and change the hashes through HxD application.**

