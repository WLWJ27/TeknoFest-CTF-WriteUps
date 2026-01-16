# The Ground Truth

## Category

OSINT

## Difficulty

Easy

## Creator

HAFSAH ANWAAR ALI

---

## Challenge Description

A popular site for learning the web has something to hide. Its domain hides more than it shows.

Flag format: `Savvy{lat,lon}`

---

## Solution Walkthrough

### Step 1: Identify the Site

The clue "popular site for learning web" refers to:

```
w3schools.com
```

---

### Step 2: Domain Metadata Analysis

We find the metadata of the domain using `whois`:

```bash
whois w3schools.com
```

From the WHOIS data, we get the following registrant details:

* Registrant Street: PO Box 786
* Registrant City: Hayes
* Registrant State/Province: Middlesex
* Registrant Postal Code: UB3 9TR
* Registrant Country: GB
* Registrant Phone: +44.1

---

### Step 3: Find Geo-coordinates

Using the registrant address from WHOIS:

```
UB3 9TR, Hayes, England
```

We input this address into [GPS Coordinates](https://www.gps-coordinates.net) to extract the latitude and longitude.

---

### Step 4: Flag

The extracted coordinates give us the flag:

```
Savvy{51.503712,-0.414331}
```

---

### Key Takeaways

* WHOIS metadata can reveal hidden location information.
* Geo-coordinates can be derived from postal address details.
* OSINT challenges often require combining domain info with public tools like GPS mapping.
