# The Gram Stalker

## Category

OSINT

## Difficulty

Medium

## Creator

HAFSAH ANWAAR ALI

---

## Challenge Description

One Instagram page is all you’re given. Four fragments form the truth. None are handed to you, all are noticed.

### 🕰️ Fragment One

This page has lived more than one life. Old names fade, but their initials remain. Three acronyms from the past still echo in its history. Find these acronyms to complete the final fragment.

### 👀 Fragment Two

Not everything important is posted. Some things are spoken by the agent around the page, not by it. Words left behind, often skimmed, often ignored, sometimes say more than the post itself. Stalk a little inside the feed and you'll find the second fragment.

### 🗓️ Fragment Three

Every page has a beginning and so does this page. Long before now, there was a first moment. Only the month name holds what you seek.

### 👑 Fragment Four

Follow your trail above the grounds. A royal name appears without a throne. It’s found among travelers’ luxuries where flights are planned and shelves shine. The Queen’s name is easy to spot — but her story doesn’t end there. The crown fell in a year the world quietly remembers. That year, not the name, is what the first fragment demands.

### 🏁 Final Assembly

Once all four fragments are uncovered, combine them in the order given. The flag follows this format:

```
Savvy{part1_part2_part3_part4}
```

Underscores matter. Order matters. Attention matters.

---

## Solution Walkthrough

### Step 1: Fragment One

Scan the page and look for logos and text in posts. Identify three initials from the past acronyms:

```
ACM
```

### Step 2: Fragment Two

Look through comments on posts. An anonymous account `agentblack` commented:

```
7h3Gr4m$741k3r
```

This forms the second fragment.

### Step 3: Fragment Three

Check the account creation date of the Instagram page. Navigate through the three-dot menu > About this account. The account was created in:

```
January 2025
```

Extract the month name for the third fragment:

```
January
```

### Step 4: Fragment Four

In the links section, find `https://tashi.preorder-shop.com`. Among the products, locate items named `Elizabeth`. Determine the year when Elizabeth died:

```
2022
```

### Step 5: Assemble the Flag

Combine all fragments with underscores in the given order:

```
Savvy{ACM_7h3Gr4m$741k3r_January_2022}
```

---

### Key Takeaways

* OSINT requires attention to **details in posts, comments, and metadata**.
* Fragmented clues often appear across **different parts of a page or website**.
* Proper assembly of all pieces is crucial to reveal the flag.
