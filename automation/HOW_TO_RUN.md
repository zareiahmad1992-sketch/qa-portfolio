# How to run this suite

Tested on macOS and Linux with Python 3.11+. Takes about two minutes the first time.

## 1. Get the code

```bash
git clone https://github.com/zareiahmad1992-sketch/qa-portfolio.git
cd qa-portfolio/automation
```

If you already have the folder, just:

```bash
cd qa-portfolio/automation
```

## 2. Create a virtual environment

Worth doing. It keeps this project's packages away from everything else on your machine.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

You'll see `(.venv)` at the start of your prompt. To leave it later: `deactivate`.

Windows, if you ever need it:

```
.venv\Scripts\activate
```

## 3. Install the dependencies

```bash
pip install -r requirements.txt
```

That pulls in Playwright and pytest. Nothing else.

## 4. Install the browser

```bash
playwright install chromium
```

Playwright manages its own browser builds, so this downloads a fresh Chromium into
`~/.cache/ms-playwright`. It does not touch the Chrome you use for browsing. About 130 MB.

If macOS blocks the download partway through, run it once with `sudo`:

```bash
sudo playwright install chromium
```

## 5. Run the tests

```bash
pytest
```

Expected result:

```
12 passed, 12 xfailed in ~21s
```

The six `xfail` results are not failures. They are the known bugs, written as tests. More
on that below.

## Useful commands

| What you want | Command |
|---|---|
| Run everything | `pytest` |
| Run one file | `pytest tests/test_flows.py` |
| Run one test | `pytest tests/test_flows.py::test_login_lands_on_the_product_list` |
| Run only the bug tests | `pytest -m bug` |
| Stop at the first failure | `pytest -x` |
| See why each bug test is expected to fail | `pytest -rx` |
| Watch it in a real browser window | `pytest --headed` |
| Slow it down so you can follow along | `pytest --headed --slowmo 500` |
| See the browser while debugging one test | `PWDEBUG=1 pytest tests/test_flows.py::test_checkout_form_keeps_what_i_typed` |

`--headed` is the one to start with if you want to see what's actually happening. Headless
is faster but it's just a black box until you know the tests work.

## What the two test files do

**`tests/test_flows.py` — 12 tests, all should pass.**

Login edge cases, name sorting, price sorting, add and remove from cart, the checkout form
keeping what you typed, validation messages, and completing an order. These describe how the
site is supposed to behave.

**`tests/test_known_bugs.py` — 12 test cases, all expected to fail.**

Each one is marked `@pytest.mark.xfail(strict=True, reason="...")`. The reason is a full
sentence, because a test that fails without saying why is just noise.

Two things this buys you:

- `strict=True` means if the bug ever gets fixed, pytest reports **XPASS** instead of quietly
  passing. You find out.
- A red run stays meaningful. If `pytest` goes red, something genuinely broke, rather than
  "oh that's one of the five".

Some of the bugs are parametrised, which is why five defects produce twelve test cases. Bug 3
and bug 4 each run against two accounts, and the sort bug runs against three options, because
"it does not sort" and "it does not sort for any option, on either account" are different
claims and only the second one is true.

To see the reasons next to the results:

```bash
pytest -rx
```

## If something fails

**`playwright: command not found`**
The venv isn't active, or the install didn't finish. Run `source .venv/bin/activate` then
`pip install -r requirements.txt` again.

**`Executable doesn't exist at .../chrome-headless-shell`**
The browser was never downloaded. Run `playwright install chromium`.

**Every test errors with `Target page, context or browser has been closed`**
Same cause. The browser binary is missing or broken. Reinstall it.

**Tests fail with a timeout on the first assertion**
Check your internet. The suite runs against the live saucedemo.com, not a local copy. If the
site is down or your connection is slow, everything times out.

**One or two tests fail and the rest pass**
That's worth looking at rather than re-running. Possibly saucedemo changed something. Open
the failure, read which assertion broke, and check the site by hand.

**`ModuleNotFoundError: No module named 'pages'`**
You're running pytest from the wrong folder. It has to be from inside `automation/`, which is
where `conftest.py` lives.

## Notes on the design

**Page objects in `pages/`.** Selectors live there, not in the tests. When saucedemo changes
a class name, I change one file instead of twelve.

**No hard-coded sleeps in test logic.** `base_page.py` and `inventory_page.py` have one
`wait_for_timeout(400)` after sorting, because that's a re-render with nothing to wait on.
Everywhere else waits on an actual element, which is both faster and less flaky.

**The `login` fixture in `conftest.py` waits properly** — for the URL, then for the list to be
visible. The earlier version didn't, and the first assertion failed intermittently because it
ran before the page settled. That was a bug in my test, not in the site, and it's the reason
`LoginPage` now has both `login()` and `login_and_wait()`.

**One browser per session, one context per test.** Fast, but each test still gets clean
cookies and storage, so test order doesn't matter.

## Running it in CI

The GitHub Actions file would be:

```yaml
name: tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r automation/requirements.txt
      - run: playwright install --with-deps chromium
      - run: pytest
        working-directory: automation
```

I didn't commit it because a scheduled job hitting someone else's demo site every day is
rude. Run it on demand instead.
