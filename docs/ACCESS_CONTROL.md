# Personal access and request limits

Implemented 2026-10-15 under user requirements R22/R23. Deployment status is in
DEPLOYMENT.md. No emails are sent, and no mailbox verification occurs.

## Account flow

1. Register an email address on the service root page.
2. Save the personal token displayed once. No plaintext token is stored server-side.
3. Paste the token into the page to authorize account/usage access. Configure it
   separately as the agent's MCP Bearer token (SUPPLIER_ATLAS_TOKEN for Codex).
4. The page displays remaining daily/shared allowances and offers token revocation.

Email is normalized by trimming and case-folding; it is unverified metadata, not
an identity claim or recovery credential. Duplicate registration cannot reveal,
replace or reset an existing token. Revocation is permanent for that token;
lost-token recovery requires operator involvement, not an email-only endpoint.
There are no password, outbound email, OAuth, advertising or analytics services.

## Initial configurable defaults

These are conservative implementation choices, not user-mandated numbers or a
guaranteed cost calculation. All daily/monthly periods use UTC.

| Limit | Default |
|---|---:|
| Tool-call attempts per account per minute | 20 |
| Tool-call attempts per account per day | 100 |
| Tool-call attempts across all accounts per day | 1,000 |
| Tool-call attempts across all accounts per month | 10,000 |
| Storage-admitted HTTP requests per day | 3,000 |
| Storage-admitted HTTP requests per month | 20,000 |
| Registration attempts per day / month | 20 / 200 |
| Registered accounts, including revoked accounts | 200 |
| All HTTP requests per process, rolling minute | 120 |
| Registration requests per process, rolling minute | 5 |

The persistent limits come from Limits in src/supplier_atlas/access.py and can be
configured with SUPPLIER_ATLAS_LIMIT_<UPPERCASE_FIELD>. The final two burst limits
are additional in-memory gates, not the durable quota mechanism. No IP identity
is trusted: forwarded headers cannot bypass the global signup allowance.

Each authenticated POST with method tools/call reserves one tool allowance before
dispatch, even if the MCP tool/arguments later fail validation. MCP initialization,
notifications, tool listing and account status consume HTTP allowance but not tool
allowance. All three engineering tools retain their prior boundaries and outputs.
The existing owner credential is retained as the owner account and has the same
limits; it cannot bypass shared ceilings. Status and revocation consume HTTP too.

Requests that reach storage consume HTTP allowance even if an account is revoked,
a tool limit is exhausted or an email is already registered. Invalid signatures,
malformed requests, static assets, health and in-memory burst rejections require
no Firestore access. Global HTTP exhaustion is cached until its window resets.
429 responses have a compact error code and Retry-After; MCP success headers give
the account's remaining calls and reset time. Storage errors return 503 and never
fall back to unmetered access. Clients must not retry until the indicated delay.

## Storage and credentials

- Default Firestore Standard database, us-central1, same project/region as Cloud
  Run. Creation returned freeTier=true. No PITR, backups or TTL billing enabled.
- Server-side IAM only; no Firebase browser SDK, public database access or service
  account key files. Runtime uses supplieratlas-runtime with roles/datastore.user.
- supplieratlas_access/global: bounded current-period counters and account count.
- supplieratlas_access/token_<SHA256(token)>: stable account ID, email,
  email_verified=false, active flag, created timestamp and current-period counters.
- supplieratlas_access/email_<HMAC(email)>: account uniqueness index. The HMAC uses
  a separate domain prefix from token signatures. The owner uses a reserved record.
- Tokens contain 256 random bits and a domain-separated HMAC. Forged tokens are
  rejected before database access. The existing private cursor key supplies HMAC
  key material with separate domain prefixes; rotating it invalidates personal
  tokens and email indexes, so coordinate any rotation/migration with access state.
- Transactions read before writing; conditional quota checks and increments commit
  together. Commit contention uses SDK retries; read-time Aborted gets bounded
  whole-transaction retries. Uncertain commits are not blindly retried.
- SQLiteAccessStore is for local development/tests only. Hosted K_SERVICE processes
  reject SQLite and refuse to start without durable access storage.
- Browser keeps a token only in memory, uses Authorization headers, never query
  strings/localStorage/cookies, and sends no third-party assets or telemetry.

## Cost boundaries and evidence

Before this change, a bounded last-day Cloud Run log query returned 558 requests:
436 HTTP 200, 117 HTTP 202, five HTTP 401. This does not establish abuse. No
free-tier exhaustion or net charge was established by this request-log check.

Firestore free quota includes 50,000 document reads and 20,000 writes per day,
1 GiB storage, and one eligible database per project. Normal admitted traffic
with these defaults is below those operation allowances (two document reads and
one/two writes for an account request; three reads/three writes for registration,
plus transaction retries). This is an estimate, not a provider-enforced cost cap.
Firestore quota resets around midnight Pacific, unlike application UTC windows.
See https://firebase.google.com/docs/firestore/quotas and
https://firebase.google.com/docs/firestore/pricing.

Cloud Run still processes unauthenticated/static/rejected traffic. Application
limits are not an edge DDoS shield or a guaranteed zero-cost cap. No paid gateway,
load balancer or Cloud Armor was introduced. Retain scale-to-zero, service/revision
max 1, .5 CPU / 256 MiB and the existing $0.10 gross Cloud Run spend cap. That cap
does not cover Firestore charges. Repeated cold starts, transaction retries and
requests rejected after a persistent budget is exhausted can still read storage.
The local exhaustion cache reduces these reads; billing/usage monitoring remains
necessary. No billing cap or paid plan was increased.

## Validation and operation

- tests/test_access.py covers concurrency, persistence, minute/day/month boundaries,
  revocation, signature rejection before storage, duplicate registration, total
  account cap, HTTP budgets, fail-closed errors, host/origin checks, body limits
  and MCP dispatch accounting. Full local suite: 62 passing tests.
- scripts/check_access_firestore.py runs bounded real-store verification against
  an isolated random collection and cleans only its own documents. Concurrency,
  persistence and revocation passed; this caught a read-time Aborted retry gap.
- Browser registration displays the one-time token and usage; no email sent.
- Runtime 0.2.0a1 / supplieratlas-demo-00006-glh serves 100% traffic. CI 38767226888
  passed 62 tests and constrained container HTTP checks. Hosted fresh personal
  signup and six engineering calls passed, with exact counters, duplicate
  protection and revocation verified. Owner SDK and three native plugin calls pass.
- Existing gross Cloud Run cap read back CONFIGURED at $0.10 with credits excluded;
  no cap increase. Plugin alpha.3 release CI 38767368856 passed. Existing clients
  remain wire-compatible; a fresh alpha.3 installation has not been claimed.
- Deployment uses deploy/deploy.ps1 with an immutable public GHCR digest, preserving
  private secrets and adding Firestore configuration. Never publish access.sqlite,
  account exports, runtime.env.yaml, credentials or original supplier PDFs.

Operator emergency revocation: set active=false on the known account document
using authenticated Google Cloud tooling. Never grant recovery from possession
of an email string. Global HTTP exhaustion also blocks the account portal; an
operator can still revoke through private database administration. Do not reset
usage counters or increase limits just to make a test pass.
