# QA Portfolio — Ahmad Zarei

I'm a QA engineer in Yerevan. Five years of testing, most of it manual, on web, Android
and API products. This repo is where I keep work I can show publicly.

Everything here was tested on [saucedemo.com](https://www.saucedemo.com), a public demo shop
built for practice testing. I picked it because anyone can log in and reproduce what I found
in two minutes, so you don't have to take my word for any of it.

Nothing in here comes from an employer. The bug reports about banking work I mention in
interviews stay in interviews — that code and those systems aren't mine to publish.

## What's in here

```
bug-reports/     five bugs I found, written the way I'd file them in Jira
evidence/        screenshots taken while reproducing each one
test-plan/       a test plan for the checkout flow, written before testing it
checklists/      the checklist I actually work from during a release pass
automation/      Playwright + pytest suite against the same site
```

## The five bugs

Short version, so you can decide if this is worth your time:

| # | What breaks | Found as |
|---|---|---|
| 1 | Typing a last name puts it in the first name field | `problem_user` |
| 2 | Every product shows the same broken-image placeholder | `problem_user` |
| 3 | "Price (low to high)" doesn't sort anything | `problem_user`, `error_user` |
| 4 | The Remove button on the product list does nothing | `error_user` |
| 5 | Prices don't match the ones every other user sees | `visual_user` |

Bug 4 is my favourite. Remove fails on the product list but works fine from the cart page,
which tells you something specific about where the handler is wired up. That contrast is
the whole report.

## The automation

Python, pytest, Playwright, page objects. It runs against the live site, so it needs network.

```bash
cd automation
pip install -r requirements.txt
playwright install chromium
pytest -v
```

Two test files do different jobs:

- `tests/test_flows.py` — the happy paths. Login, browse, sort, add to cart, check out.
  These should all pass. If one fails, either the site changed or I broke something.
- `tests/test_known_bugs.py` — the five bugs above, written as tests and marked `xfail`.
  They fail because the bugs are real. When saucedemo fixes one, pytest will flag it as
  XPASS and I'll delete the test. That's the honest way to keep a known-bug list from
  rotting into a list of things that stopped being true.

I left the `xfail` reasons as proper sentences. A test that fails and doesn't say why is
just noise.

## What I'd do with more time

- Run the suite on a mobile viewport. I only looked at desktop here.
- Add a check that the cart survives a page refresh. I never tested persistence properly.
- Time the `performance_glitch_user` login against a baseline. I noticed it felt slow, but
  "felt slow" isn't evidence, and I'd rather measure it than guess.

## Contact

Ahmad Zarei — zarei.ahmad1992@gmail.com — [LinkedIn](https://www.linkedin.com/in/ahmad-zarei92)
