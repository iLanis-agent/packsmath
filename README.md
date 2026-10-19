# Pack Math

Whole-pack buying arithmetic. Need 12 and they come in 8s? You buy 16 and 4 are left over.

## What it computes

- **The buy truth** - whole packs for a need, the total that comes with them and what is left over.
- **The even truth** - a count split among groups: each share, the remainder, and the nearest ways to make it even (add or take away).
- **The compare truth** - two pack options (size and price) for the same need: packs, cost and leftovers for each, and the cost difference.

Counts are whole numbers from 1 to 1000000 (groups from 2). Prices have up to 2 decimals, from 0.01 to 100000. Arithmetic is exact with big integers; costs are exact to the cent.

## Boundary

Arithmetic only. It assumes the sizes and prices are what the store really charges and does not know about sales, coupons, tax or stock. Check those at the shelf or the checkout.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror (loops packs one by one for small needs) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (48 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/packsmath/
Repo: https://github.com/iLanis-agent/packsmath
