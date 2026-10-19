// Pack Math engine - buying in whole packs, splitting evenly, and comparing two pack options.
// Mirrored by oracle.py; keep the op order identical.
// Counts are whole numbers from 1 to 1000000. Prices have up to 2 decimals, from 0.01 to 100000. Arithmetic is exact.

function _int(text, label, hi, lo) {
  lo = lo || 1;
  var t = typeof text === "string" ? text.trim() : "";
  var err = label + " must be a whole number from " + lo + " to " + hi;
  if (!/^[0-9]{1,8}$/.test(t)) throw new Error(err);
  var v = BigInt(t);
  if (v < BigInt(lo) || v > BigInt(hi)) throw new Error(err);
  return v;
}

function _price(text, label) {
  var t = typeof text === "string" ? text.trim() : "";
  var m = /^([0-9]+)(?:\.([0-9]{1,2}))?$/.exec(t);
  var err = label + " must be a positive number with at most 2 decimals, from 0.01 to 100000";
  if (!m) throw new Error(err);
  var h = BigInt(m[1]) * 100n + BigInt((m[2] || "") + "00".slice((m[2] || "").length));
  if (h < 1n || h > 10000000n) throw new Error(err);
  return h;
}

// Hundredths as text with 2 decimals.
function _money(h) {
  var f = String(h % 100n);
  while (f.length < 2) f = "0" + f;
  return (h / 100n) + "." + f;
}

function _packs(n) { return n + (n === 1n ? " pack" : " packs"); }
function _left(n) { return n === 0n ? "none left over" : n + " left over"; }

// The buy truth: whole packs for a need.
function buyTruth(need, size) {
  var n = _int(need, "need", 1000000), s = _int(size, "pack size", 1000000);
  var p = (n + s - 1n) / s, total = p * s;
  return "Needing " + n + " in packs of " + s + " takes " + _packs(p) + ", which is " + total + " in all with " + _left(total - n) + ".";
}

// The even truth: splitting a count among groups.
function evenTruth(count, groups) {
  var c = _int(count, "count", 1000000), g = _int(groups, "groups", 1000000, 2);
  var q = c / g, r = c % g;
  if (r === 0n) return c + " split among " + g + " groups gives " + q + " each, with none left over.";
  var add = g - r;
  var s = c + " split among " + g + " groups gives " + q + " each with " + r + " left over. Adding " + add + " (" + (c + add) + " in all) gives " + (q + 1n) + " each";
  if (q >= 1n) s += "; taking away " + r + " (" + (c - r) + " in all) gives " + q + " each";
  return s + ".";
}

// The compare truth: two pack options for the same need.
function compareTruth(need, sizeA, priceA, sizeB, priceB) {
  var n = _int(need, "need", 1000000);
  var sa = _int(sizeA, "pack A size", 1000000), pa = _price(priceA, "pack A price");
  var sb = _int(sizeB, "pack B size", 1000000), pb = _price(priceB, "pack B price");
  var qa = (n + sa - 1n) / sa, qb = (n + sb - 1n) / sb;
  var ca = qa * pa, cb = qb * pb;
  var line = function (tag, size, price, q, cost, total) {
    return tag + " (packs of " + size + " at " + _money(price) + ") takes " + _packs(q) + " for " + _money(cost) + ", with " + _left(total - n);
  };
  var verdict;
  if (ca === cb) verdict = "They cost the same.";
  else if (ca < cb) verdict = "A costs " + _money(cb - ca) + " less.";
  else verdict = "B costs " + _money(ca - cb) + " less.";
  return "Needing " + n + ": " + line("A", sa, pa, qa, ca, qa * sa) + "; " + line("B", sb, pb, qb, cb, qb * sb) + ". " + verdict;
}
