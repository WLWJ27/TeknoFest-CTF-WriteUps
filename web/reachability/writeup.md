Step 1: Reconnaissance (The Broken Dashboard)
I started by accessing the web interface and was greeted by a pirate-themed login screen. Since I didn't have specific credentials, I tried standard guesses.

Input: Any string (e.g., admin / password or guest / guest)

Result: Success! I was logged in.

The Dashboard showed my current status as S0 (Landlubber). There was a visual map leading all the way to S6 (Pirate Lord), but there were no buttons to advance the workflow.

However, a warning message at the bottom gave me a critical lead:

"Automated transition failed. Manual intervention via /appeal API required."

Step 2: The Missing Link (Finding the Source Code)
While inspecting the dashboard for a way to use that API, I noticed a distinct section at the bottom labeled "Steal Captain's Rulebook (Download Source)".

I clicked it and downloaded a file named source_code.zip. This was the breakthrough I needed! instead of guessing blindly, I now had the actual Python logic the server uses to check my rank. Inside the zip, I found state_machine.py, which contained all the rules.

Step 3: Analyzing the Logic (The State Machine)
I opened state_machine.py to understand how the server verifies the "Appeal." I realized the server expects a Trace—a JSON list representing the history of my rank from S0 to S6.

The code enforced strict mathematical rules to move from one state to the next:

S0 → S1: Time (epoch) must increase.

S1 → S2: kyc_score must be ≥ 85.

S2 → S3: risk_score must be ≤ (100 - kyc_score).

S3 → S4: approvals must be ≥ 2.

S4 → S5: audit_depth must be < 3 AND appeals must be 0.

S5 → S6 (The Goal): audit_depth must equal appeals + 1 AND (kyc_score + risk_score == 100).

Step 4: Solving the Constraints (The Math)
This is basically a math puzzle. To reach S6, I had to pick specific numbers that satisfied all the previous rules at the same time. I worked backward from the goal:

Target (S6): I need kyc + risk == 100. Let's pick KYC=90 and Risk=10.

Audit Rule: I need audit == appeals + 1. Let's set Appeals=0. This means my Audit Depth must be 1.

Verification:

Does S5 allow Audit=1? Yes (1 < 3).

Does S3 allow Risk=10 if KYC is 90? Yes (100 - 90 = 10, and 10 ≤ 10).

Does S1 allow KYC=90? Yes (90 ≥ 85).

Step 5: The Exploit (Constructing the Trace)
With my numbers ready, I constructed a JSON payload containing the full history (S0 to S6).

The Payload:

[
  { "name": "S0", "epoch": 0, "kyc_score": 0, "risk_score": 0, "audit_depth": 0, "approvals": 0, "appeals": 0, "compliance_flags": 0 },
  { "name": "S1", "epoch": 1, "kyc_score": 90, "risk_score": 0, "audit_depth": 0, "approvals": 0, "appeals": 0, "compliance_flags": 0 },
  { "name": "S2", "epoch": 2, "kyc_score": 90, "risk_score": 0, "audit_depth": 0, "approvals": 0, "appeals": 0, "compliance_flags": 0 },
  { "name": "S3", "epoch": 3, "kyc_score": 90, "risk_score": 10, "audit_depth": 0, "approvals": 0, "appeals": 0, "compliance_flags": 0 },
  { "name": "S4", "epoch": 4, "kyc_score": 90, "risk_score": 10, "audit_depth": 0, "approvals": 5, "appeals": 0, "compliance_flags": 0 },
  { "name": "S5", "epoch": 5, "kyc_score": 90, "risk_score": 10, "audit_depth": 1, "approvals": 5, "appeals": 0, "compliance_flags": 0 },
  { "name": "S6", "epoch": 6, "kyc_score": 90, "risk_score": 10, "audit_depth": 1, "approvals": 5, "appeals": 0, "compliance_flags": 0 }
]

Step 6: Collecting the Loot
I sent this payload to the /appeal endpoint using curl (you can also use Burp Suite).

Server Response: {"result": "ACCEPTED", "status": "Compliance Verified"}

Cookie Received: compliance_auth=VALID_PROOF_SUBMITTED

Now that I had the session cookie proving I "passed the audit," I simply visited the flag URL:

Request: GET /flag (with the new Cookie)

Server Response:

{
 "flag": "Savvy{W1WJ_X_73CN0_F3$T}"
}
