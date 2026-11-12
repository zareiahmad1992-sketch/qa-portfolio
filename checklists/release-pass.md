# Release pass checklist

What I actually walk through before signing off a build. Short on purpose. A checklist
long enough to skip is worse than no checklist.

## Before I start

- [ ] I know which build I'm testing and where it's deployed
- [ ] I know what changed since the last build I tested
- [ ] I have the requirements or tickets for those changes open
- [ ] Test data I need exists, and I know how to reset it

## Smoke first, always

- [ ] The app loads at all
- [ ] I can log in
- [ ] The main screen shows real data, not an empty shell
- [ ] One full pass through the most important flow, start to finish

If any of these fail, I stop and say so. There's no point testing detail on a build that
can't get out of the gate.

## The changes

- [ ] Each changed item tested against its own acceptance criteria
- [ ] Each changed item tested a second time, starting over from a clean state
- [ ] The screens next to each changed screen still work
- [ ] Anything that shares data with a changed screen still reads that data correctly

## The things that break quietly

- [ ] Numbers on screen match the numbers in the database
- [ ] Totals add up
- [ ] What I typed is what's still in the field after I come back to it
- [ ] Saved data is still there after a refresh
- [ ] An action that should be refused is actually refused, and the message says why

## Before I sign off

- [ ] Every bug I filed has steps someone else could follow
- [ ] Nothing open is worth blocking the release for. If something is, I've said so
      in writing rather than in passing
- [ ] I've told the team what I did **not** test
