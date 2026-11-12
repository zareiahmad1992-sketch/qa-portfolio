QA Portfolio: Ahmad Zarei

I'm a QA engineer in Yerevan. Five years of testing, most of it manual, on web, Android
and API products. This repo is where I keep work I can show publicly.

Everything here is on saucedemo.com, a public practice shop, so
you can reproduce any of it in a couple of minutes.
What's in here

text

bug-reports/     five bugs I found, written the way I'd file them in Jira
evidence/        screenshots taken while reproducing each one
test-plan/       a test plan for the checkout flow, written before testing it
checklists/      the checklist I actually work from during a release pass
automation/      Playwright + pytest suite against the same site

The five bugs

Short version, so you can decide if this is worth your time:
#	What breaks	Found as	Severity
1	Typing a last name puts it in the first name field, which blocks checkout completely	problem_user	Blocker
2	Every product shows the same broken-image placeholder	problem_user	Medium
3	Every sort option snaps the dropdown back to A-Z and never reorders	problem_user, error_user	Medium
4	The Remove button on the product list does nothing	error_user, problem_user	High
5	Prices don't match the ones every other user sees	visual_user	High

Bug 4 is my favourite. Remove fails on the product list but works fine from the cart page,
which tells you something specific about where the handler is wired up. That contrast is
the whole report.

Bug 3 taught me to check the control as well as the result. My first pass said "price sort does
not work". Then I read the select element's value and found it was reverting to A-Z after every
choice, on all four options, which is a different bug with a different cause.
The automation

Python, pytest, Playwright, page objects. It runs against the live site, so it needs network.

Bash

cd automation
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
pytest

automation/HOW_TO_RUN.md has the longer version, including failure modes and the
--headed flag if you want to watch it run.

Two test files do different jobs:

    tests/test_flows.py: the happy paths. Login, browse, sort, add to cart, check out.
    These should all pass. If one fails, either the site changed or I broke something.
    tests/test_known_bugs.py: the five bugs above, written as tests and marked xfail.
    They fail because the bugs are real. When saucedemo fixes one, pytest will flag it as
    XPASS and I'll delete the test. That's the honest way to keep a known-bug list from
    rotting into a list of things that stopped being true.

I left the xfail reasons as proper sentences. A test that fails and doesn't say why is
just noise.
What I'd do with more time

    Run the suite on a mobile viewport. I only looked at desktop here.
    Add a check that the cart survives a page refresh. I never tested persistence properly.
    Time the performance_glitch_user login against a baseline. I noticed it felt slow, but
    "felt slow" isn't evidence, and I'd rather measure it than guess.

Contact

Ahmad Zarei | zarei.ahmad1992@gmail.com | LinkedIn
