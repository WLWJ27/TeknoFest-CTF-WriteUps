Step 1: Finding the Rules
I looked around the dashboard and saw a big button at the bottom: "Steal Captain's Rulebook (Download Source)".

I downloaded the zip file and extracted it. Inside, there were four Python files. The most interesting one was state_machine.py. This file basically contained the "laws" of the ship. It showed exactly what numbers you need to move from one rank to the next.

Step 2: Doing the Math
I read the code and realized I needed to build a "trace"—basically a history of my career as a pirate—and send it to the server. The server doesn't check when I did these things; it just checks if the numbers add up.

Here is the math I had to figure out to pass the checks:

Loyalty (KYC): To get past rank S1, I needed a score over 85. I picked 90.

Risk: The rules said Risk + Loyalty must equal 100 at the end. Since my Loyalty was 90, my Risk had to be 10.

Approvals: To get past rank S3, I needed at least 2 approvals. I gave myself 5 just to be safe.

The Final Gate: To reach the final rank (S6), the "Audit Depth" had to be exactly 1 higher than my "Appeals". Since I had 0 appeals, my Audit Depth needed to be 1.

Step 3: Faking the History (The Exploit)
Now that I had the magic numbers (90, 10, 5, 1), I had to construct a fake history. I created a JSON list that showed me going from S0 all the way to S6, step-by-step.

It looked something like this:

Step 1 (S0): I started with nothing.

Step 2 (S1): I suddenly had 90 Loyalty and 10 Risk.

Step 3 to Step 7: I kept those numbers the same for every step until I reached S6.

Step 4: Getting the Flag
I sent this JSON data to the /appeal endpoint using a tool called Postman (you can use curl too).

The server checked my math, saw that it followed all the rules, and replied:

"ACCEPTED"

It gave me a special cookie called compliance_auth. I went to the /flag page with that cookie, and there it was!

Flag: Savvy{W1WJ_X_73CN0_F3$T}
