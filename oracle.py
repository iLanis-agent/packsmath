#!/usr/bin/env python3
# Pack Math oracle - mirrors engine.js, using brute-force pack counting (loop) for small needs and divmod otherwise.
import json, re

def _int(text, label, hi, lo=1):
    t = text.strip() if isinstance(text, str) else ""
    err = f"{label} must be a whole number from {lo} to {hi}"
    if not re.fullmatch(r"[0-9]{1,8}", t):
        raise ValueError(err)
    v = int(t)
    if v < lo or v > hi:
        raise ValueError(err)
    return v

def _price(text, label):
    t = text.strip() if isinstance(text, str) else ""
    m = re.fullmatch(r"([0-9]+)(?:\.([0-9]{1,2}))?", t)
    err = f"{label} must be a positive number with at most 2 decimals, from 0.01 to 100000"
    if not m:
        raise ValueError(err)
    h = int(m.group(1)) * 100 + int((m.group(2) or "").ljust(2, "0"))
    if h < 1 or h > 10000000:
        raise ValueError(err)
    return h

def money(h):
    return f"{h // 100}.{h % 100:02d}"

def packs_needed(n, s):
    if n <= 2000:  # brute force
        p = 0
        while p * s < n:
            p += 1
        return p
    return -(-n // s)

def packs(n): return f"{n} pack" + ("" if n == 1 else "s")
def left(n): return "none left over" if n == 0 else f"{n} left over"

def buy_truth(need, size):
    n = _int(need, "need", 1000000); s = _int(size, "pack size", 1000000)
    p = packs_needed(n, s)
    return f"Needing {n} in packs of {s} takes {packs(p)}, which is {p * s} in all with {left(p * s - n)}."

def even_truth(count, groups):
    c = _int(count, "count", 1000000); g = _int(groups, "groups", 1000000, 2)
    q, r = divmod(c, g)
    if r == 0:
        return f"{c} split among {g} groups gives {q} each, with none left over."
    add = g - r
    s = f"{c} split among {g} groups gives {q} each with {r} left over. Adding {add} ({c + add} in all) gives {q + 1} each"
    if q >= 1:
        s += f"; taking away {r} ({c - r} in all) gives {q} each"
    return s + "."

def compare_truth(need, size_a, price_a, size_b, price_b):
    n = _int(need, "need", 1000000)
    sa = _int(size_a, "pack A size", 1000000); pa = _price(price_a, "pack A price")
    sb = _int(size_b, "pack B size", 1000000); pb = _price(price_b, "pack B price")
    qa, qb = packs_needed(n, sa), packs_needed(n, sb)
    ca, cb = qa * pa, qb * pb
    def line(tag, size, price, q, cost):
        return f"{tag} (packs of {size} at {money(price)}) takes {packs(q)} for {money(cost)}, with {left(q * size - n)}"
    if ca == cb: v = "They cost the same."
    elif ca < cb: v = f"A costs {money(cb - ca)} less."
    else: v = f"B costs {money(ca - cb)} less."
    return f"Needing {n}: {line('A', sa, pa, qa, ca)}; {line('B', sb, pb, qb, cb)}. {v}"

FNS = {"buyTruth": buy_truth, "evenTruth": even_truth, "compareTruth": compare_truth}
CASES = [
    ("buyTruth", ["12", "8"]), ("buyTruth", ["16", "8"]), ("buyTruth", ["1", "1"]), ("buyTruth", ["1", "10"]), ("buyTruth", ["10", "1"]),
    ("buyTruth", ["2000", "7"]), ("buyTruth", ["2001", "7"]), ("buyTruth", ["1000000", "1000000"]), ("buyTruth", ["1000000", "999999"]), ("buyTruth", ["1000000", "1"]),
    ("buyTruth", ["25", "12"]), ("buyTruth", [" 9 ", " 4 "]), ("buyTruth", ["0", "5"]), ("buyTruth", ["5", "0"]), ("buyTruth", ["-5", "2"]),
    ("buyTruth", ["abc", "2"]), ("buyTruth", ["1000001", "2"]), ("buyTruth", ["5", "1.5"]), ("buyTruth", ["", "2"]),
    ("evenTruth", ["14", "4"]), ("evenTruth", ["12", "4"]), ("evenTruth", ["5", "8"]), ("evenTruth", ["1", "2"]), ("evenTruth", ["7", "2"]),
    ("evenTruth", ["100", "7"]), ("evenTruth", ["1000000", "1000000"]), ("evenTruth", ["999999", "1000000"]), ("evenTruth", ["30", "30"]), ("evenTruth", ["31", "30"]),
    ("evenTruth", ["10", "1"]), ("evenTruth", ["10", "0"]), ("evenTruth", ["x", "3"]), ("evenTruth", ["10", "1000001"]),
    ("compareTruth", ["24", "6", "4.50", "10", "7"]), ("compareTruth", ["24", "6", "4", "12", "8"]), ("compareTruth", ["12", "8", "3.99", "12", "3.99"]),
    ("compareTruth", ["12", "8", "3.99", "6", "2"]), ("compareTruth", ["1", "1", "0.01", "100", "100000"]), ("compareTruth", ["1000000", "1", "1", "1000000", "100000"]),
    ("compareTruth", ["30", "10", "5", "15", "2.50"]), ("compareTruth", ["50", "12", "9.99", "8", "6.50"]), ("compareTruth", ["8", "3", "1.10", "4", "1.50"]),
    ("compareTruth", ["24", "6", "0", "10", "7"]), ("compareTruth", ["24", "6", "4.5", "10", "100000.01"]), ("compareTruth", ["24", "0", "4.5", "10", "7"]),
    ("compareTruth", ["24", "6", "4.555", "10", "7"]), ("compareTruth", ["abc", "6", "4.5", "10", "7"]), ("compareTruth", ["24", "6", "4.5", "x", "7"]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
