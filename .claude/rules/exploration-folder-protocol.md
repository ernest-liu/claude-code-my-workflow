# Exploration Folder Protocol

**All experimental work goes into a dedicated workspace first.** Never directly into production folders.

## Folder Structure

```
[exploration-workspace]/
├── README.md          # Goal, status, findings
├── R/                 # Code (use _v1, _v2 for iterations)
├── output/            # Results
└── SESSION_LOG.md     # Progress notes
```

## Lifecycle

1. **Create** -- set up an exploration workspace with README
2. **Develop** -- work entirely within the exploration workspace
3. **Decide:**

   - **Graduate to production** -- copy to main project folders; requires quality >= 80, tests pass, code clear
   - **Keep exploring** -- document next steps in README
   - **Abandon** -- archive with explanation

## Graduate Checklist

- [ ] Quality score >= 80
- [ ] All tests pass
- [ ] Results replicate within tolerance
- [ ] Code is clear without deep context
- [ ] README explains approach and findings
