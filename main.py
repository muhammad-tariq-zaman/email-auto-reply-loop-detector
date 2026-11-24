"""Detect auto-reply loops between mailboxes.

Usage: python3 main.py replies.csv
CSV columns: from_mailbox,to_mailbox,auto_replies,subject.
auto_replies is how many automatic replies went from
from_mailbox to to_mailbox for that subject. Verdicts:
- LOOP: auto-replies went BOTH ways between the two
  mailboxes, or one direction alone sent 5 or more.
- SUSPECT: 3 or 4 auto-replies in one direction with no
  reply back.
- OK: fewer than 3 auto-replies in one direction.
LOOP first (most auto-replies first), then SUSPECT, then OK.
Rows with a non-numeric auto_replies are reported as
skipped, not silently dropped.
"""
import argparse, csv, sys

VERDICT_ORDER = {"LOOP": 0, "SUSPECT": 1, "OK": 2}

def detect(rows):
    pairs = {}
    skipped = 0
    for row in rows:
        try:
            sender = row["from_mailbox"].strip()
            recipient = row["to_mailbox"].strip()
            count = int(row["auto_replies"])
            subject = row["subject"].strip()
            if not sender or not recipient or not subject:
                raise ValueError("missing value")
        except (KeyError, AttributeError, ValueError, TypeError):
            skipped += 1
            continue
        key = tuple(sorted((sender, recipient)))
        entry = pairs.setdefault(key, {"forward": 0, "back": 0})
        if (sender, recipient) == key:
            entry["forward"] += count
        else:
            entry["back"] += count
    out = []
    for (first, second), entry in pairs.items():
        total = entry["forward"] + entry["back"]
        both = entry["forward"] > 0 and entry["back"] > 0
        one_way = max(entry["forward"], entry["back"])
        if both or one_way >= 5:
            verdict = "LOOP"
            if both:
                detail = (f"{total} auto-replie(s) each way "
                          f"({first} -> {second} and back)")
            else:
                detail = f"{total} auto-replie(s) one way, no reply back"
        elif total >= 3:
            verdict = "SUSPECT"
            detail = f"{total} auto-replie(s), no reply back yet"
        else:
            verdict = "OK"
            detail = f"{total} auto-replie(s)"
        out.append((first, second, total, verdict, detail))
    out.sort(key=lambda r: (VERDICT_ORDER[r[3]], -r[2], r[0], r[1]))
    return out, skipped

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results, skipped = detect(list(csv.DictReader(f)))
    for sender, recipient, _, verdict, detail in results:
        print(f"{sender} <-> {recipient}: {verdict} - {detail}")
    counts = {v: sum(1 for *_, verdict, _ in results if verdict == v)
              for v in VERDICT_ORDER}
    print(f"{counts['LOOP']} loop(s), {counts['SUSPECT']} suspect, "
          f"{counts['OK']} ok out of {len(results)} mailbox pair(s).")
    if skipped:
        print(f"Skipped {skipped} invalid row(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
