# Test plan — checkout flow

Written before I ran a single test on it. I'm keeping it in that state, because the plan I
write up front is a different, more useful document than the one I'd write afterwards with
hindsight.

**Scope:** saucedemo.com, checkout from cart to order confirmation
**Accounts:** `standard_user`, plus `problem_user` and `error_user` for the same paths
**Browser:** Chromium, desktop 1280×800
**Out of scope:** payment processing (the demo doesn't charge anything), mobile layout,
performance under load

## Why this flow

Cart to confirmation is the shortest path from "customer wants something" to "customer has
paid". A defect anywhere along it costs money or trust, which is why it gets tested
properly and not just clicked through at the end of a sprint.

## What I'm going to test

**1. The happy path, end to end.**
One item, correct details, finish. Check the confirmation text and that the cart is empty
afterwards. This is the baseline — if this doesn't work, nothing else matters.

**2. Each field, on its own.**
Leave First Name empty and continue. Then Last Name. Then Postal Code. Each one should
block the step and name the field it wants. I want to read the actual error text, not just
see that something red appeared.

**3. Values that are accepted versus rejected.**
Postal code with letters in it. A name with an apostrophe (O'Brien) or a hyphen. A single
space in each field. I don't know yet what this app considers valid, so I'm going in
without assuming — whatever it does, I want to know whether it does it *consistently*.

**4. What the field actually keeps.**
Fill all three fields, then go back and read them. Not what I typed — what's still in the
boxes. On the payment and checkout forms I've tested at work, this is where things quietly
go wrong.

**5. Back and forward.**
Fill in the form, hit Cancel or the browser back button, then return to checkout. Are my
details still there, or blank, or half-filled? Any of those could be defensible, but it has
to be deliberate.

**6. The total.**
Item price plus tax should equal the total shown on the summary. I'll check this by hand
with a calculator rather than trusting the page, because a summary that adds up wrongly
looks completely normal.

**7. Empty cart.**
Remove everything, then try to reach checkout directly by URL. It should not let me buy
nothing.

**8. The problem accounts.**
Run the same happy path on `problem_user` and `error_user`. Anywhere they behave differently
from `standard_user` is worth writing down, even if I can't yet say which behaviour is the
correct one.

## What would make me stop and call someone

- A defect that lets an order complete with no name on it, or with someone else's details.
- Totals that don't reconcile.
- A form that silently drops a value I typed. Wrong data is worse than an error message,
  because the customer never finds out until the parcel arrives.

## How I'll record what I find

One file per bug, in the format I'd use in Jira: steps, expected, actual, how I reproduced
it. Screenshot attached where the words aren't enough. If I can't reproduce something twice,
I write down that I saw it once and say I couldn't repeat it — an unreproduced bug is still
information, it's just weaker information.

## What I expect to miss

Mobile entirely. Anything that only happens under real payment load. And any defect whose
symptom is "this number is wrong" — those only turn up if you go and check the number,
which is exactly why item 6 is in this plan.
