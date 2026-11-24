# email-auto-reply-loop-detector

Detect auto-reply loops between mailboxes: the input CSV lists from_mailbox, to_mailbox, auto_replies and subject — LOOP when auto-replies went BOTH ways between the two mailboxes, or one direction alone sent 5 or more, SUSPECT when 3 or 4 auto-replies went one way with no reply back, OK when fewer than 3 — LOOP first (most auto-replies first), then SUSPECT, then OK. Rows with a non-numeric auto_replies are reported as skipped, not silently dropped.

Sample input is included (sample.csv with seven rows, one invalid row).

## How to run

```sh
python3 main.py sample.csv
```

## Example output

```
helpdesk@company.pk <-> vendor@partner.com: LOOP - 6 auto-replie(s) one way, no reply back
admin@company.pk <-> it@company.pk: LOOP - 3 auto-replie(s) each way (admin@company.pk -> it@company.pk and back)
client@customer.com <-> noreply@company.pk: SUSPECT - 3 auto-replie(s), no reply back yet
hr@company.pk <-> support@company.pk: OK - 2 auto-replie(s)
info@company.pk <-> sales@company.pk: OK - 2 auto-replie(s)
2 loop(s), 1 suspect, 2 ok out of 5 mailbox pair(s).
Skipped 1 invalid row(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
